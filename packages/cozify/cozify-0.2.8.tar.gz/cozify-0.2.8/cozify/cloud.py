"""Module for handling Cozify Cloud API operations

Attributes:
    cloudBase(str): API endpoint including version

"""

import json, requests, logging

from . import config as c
from . import hub

from .Error import APIError, AuthenticationError

cloudBase='https://cloud2.cozify.fi/ui/0.2/'

def authenticate(trustCloud=True, trustHub=True, remote=False, autoremote=True):
    """Authenticate with the Cozify Cloud and Hub.

    Interactive only when absolutely needed, mostly on the first run.
    By default authentication is run selectively only for the portions needed.
    Hub authentication lives in the Cloud module since the authentication is obtained from
    the cloud.

    Authentication is a multistep process:
        - trigger sending OTP to email address
        - perform email login with OTP to acquire cloud token
        - acquire hub information and authenticate with hub with cloud token
        - store hub token for further use

    Args:
        trustCloud(bool): Trust current stored state of cloud auth. Default True.
        trustHub(bool): Trust current stored state of hub auth. Default True.
        remote(bool): Treat a hub as being outside the LAN, i.e. calls will be routed via the Cozify Cloud remote call system. Defaults to False.
        autoremote(bool): Autodetect hub LAN presence and flip to remote mode if needed. Defaults to True.

    Returns:
        bool: True on authentication success. Failure will result in an exception.
    """

    if 'email' not in c.state['Cloud'] or not c.state['Cloud']['email']:
         c.state['Cloud']['email'] = _getEmail()
         c.stateWrite()
    email = c.state['Cloud']['email']

    if _needRemoteToken(trustCloud):
        try:
            _requestlogin(email)
        except APIError:
            resetState() # a bogus email will shaft all future attempts, better to reset
            raise

        # get OTP from user, not stored anywhere since they have a very short lifetime
        otp = _getotp()
        if not otp:
            message = "OTP unavailable, authentication cannot succeed. This may happen if running non-interactively (closed stdin)."
            logging.critical(message)
            raise AuthenticationError(message)

        try:
            remoteToken = _emaillogin(email, otp)
        except APIError:
            logging.error('OTP authentication has failed.')
            resetState()
            raise

        # save the successful remoteToken
        c.state['Cloud']['remoteToken'] = remoteToken
        c.stateWrite()
    else:
        # remoteToken already fine, let's just use it
        remoteToken = c.state['Cloud']['remoteToken']

    if _needHubToken(trustHub):
        localHubs = _lan_ip() # will only work if we're local to the Hub, otherwise None
        # TODO(artanicus): unknown what will happen if there is a local hub but another one remote. Needs testing by someone with multiple hubs. Issue #7
        hubkeys = _hubkeys(remoteToken) # get all registered hubs and their keys from the cloud.
        if not hubkeys:
            logging.critical('You have not registered any hubs to the Cozify Cloud, hence a hub cannot be used yet.')

        # evaluate all returned Hubs and store them
        logging.debug('Listing all hubs returned by cloud hubkeys query:')
        for hubId, hubToken in hubkeys.items():
            logging.debug('hub: {0} token: {1}'.format(hubId, hubToken))
            hubInfo = None
            hubIp = None

            # if we're remote, we didn't get a valid ip
            if not localHubs:
                logging.info('No local Hubs detected, attempting authentication via Cozify Cloud.')
                hubInfo = hub._hub(remoteToken=remoteToken, hubToken=hubToken)
                # if the hub wants autoremote we flip the state
                if hub.autoremote and not hub.remote:
                    logging.info('[autoremote] Flipping hub remote status from local to remote.')
                    hub.remote = True
            else:
                # localHubs is valid so a hub is in the lan. A mixed environment cannot yet be detected.
                # _lan_ip cannot provide a map as to which ip is which hub. Thus we actually need to determine the right one.
                # TODO(artanicus): Need to truly test how multihub works before implementing ip to hub resolution. See issue #7
                logging.debug('data structure: {0}'.format(localHubs))
                hubIp = localHubs[0]
                hubInfo = hub._hub(host=hubIp)
                # if the hub wants autoremote we flip the state
                if hub.autoremote and hub.remote:
                    logging.info('[autoremote] Flipping hub remote status from remote to local.')
                    hub.remote = False

            hubName = hubInfo['name']
            if hubId in hubkeys:
                hubToken = hubkeys[hubId]
            else:
                logging.error('The hub "{0}" is not linked to the given account: "{1}"'.format(hubName, c.state['Cloud']['email']))
                resetState()
                return False

            # if hub name not already known, create named section
            hubSection = 'Hubs.' + hubId
            if hubSection not in c.state:
                c.state[hubSection] = {}
            # if default hub not set, set this hub as the first as the default
            if 'default' not in c.state['Hubs']:
                c.state['Hubs']['default'] = hubId

            # store Hub data under it's named section
            c.state[hubSection]['hubToken'] = hubToken
            c.state[hubSection]['host'] = hubIp
            c.state[hubSection]['hubName'] = hubName
            c.stateWrite()
    return True

def resetState():
    """Reset stored cloud state.

    Any further authentication flow will start from a clean slate.
    Hub state is left intact.
    """

    c.state['Cloud'] = {}
    c.stateWrite()

def ping():
    """Test cloud token validity.

    Returns:
        bool: validity of stored token.

    """

    try:
        _hubkeys(c.state['Cloud']['remoteToken']) # TODO(artanicus): see if there's a cheaper API call
    except APIError as e:
        if e.status_code == 401:
            return False
        else:
            raise
    else:
        return True

def refresh():
    """Renew current cloud token and store new token in state.

    This call will only succeed if the current cloud token is still valid.
    A new refreshed token is requested from the API and stored in state.

    Returns:
        bool: Success of refresh attempt.
    """
    try:
        newRemoteToken = _refreshsession(c.state['Cloud']['remoteToken'])
    except APIError as e:
        if e.status_code == 401:
            # too late, our token is already dead
            return False
        else:
            raise
    else:
        c.state['Cloud']['remoteToken'] = newRemoteToken
        c.stateWrite()
        return True



def _needRemoteToken(trust=True):
    """Validate current remote token and decide if we'll request it during authentication.

    Args:
        trust(bool): Set to False to always decide to renew. Defaults to True.

    Returns:
        bool: True to indicate a need to request token.
    """

    # check if we've got a remoteToken before doing expensive checks
    if trust and 'remoteToken' in c.state['Cloud']:
        if c.state['Cloud']['remoteToken'] is None:
            return True
        else: # perform more expensive check
            return not ping()
    return True

def _needHubToken(trust=True):
    """Validate current hub token and decide if we'll request it during authentication.

    Args:
        trust(bool): Set to False to always decide to renew. Defaults to True.

    Returns:
        bool: True to indicate a need to request token.
    """
    if not trust:
        logging.debug("hub_token not trusted so we'll say it needs to be renewed.")
        return True

    # First do quick checks, i.e. do we even have a token already
    if 'default' not in c.state['Hubs'] or 'hubtoken' not in c.state['Hubs.' + c.state['Hubs']['default']]:
        logging.debug("We don't have a valid hubtoken or it's not trusted.")
        return True
    else: # if we have a token, we need to test if the API is callable
        ping = hub.ping()
        logging.debug("Testing hub.ping() for hub_token validity: {0}".format(ping))
        return not ping

def _getotp():
    try:
        return input('OTP from your email: ')
    except EOFError: # if running non-interactive or ^d
        return None

def _getEmail():
    return input('Enter your Cozify account email address: ')

def _getAttr(attr):
    """Get cloud state attributes by attr name
    
    Args:
        attr(str): Name of cloud state attribute to retrieve
    Returns:
        str: Value of attribute or exception on failure
    """
    section = 'Cloud'
    if section in c.state and attr in c.state[section]:
        return c.state[section][attr]
    else:
        logging.warning('Cloud attribute {0} not found in state.'.format(attr))
        raise AttributeError

def token():
    """Get currently used cloud_token.

    Returns:
        str: Cloud remote authentication token.
    """
    return _getAttr('remotetoken')
        
def _requestlogin(email):
    """Raw Cloud API call, request OTP to be sent to account email address.

    Args:
        email(str): Email address connected to Cozify account.
    """

    payload = { 'email': email }
    response = requests.post(cloudBase + 'user/requestlogin', params=payload)
    if response.status_code is not 200:
        raise APIError(response.status_code, response.text)

def _emaillogin(email, otp):
    """Raw Cloud API call, request cloud token with email address & OTP.

    Args:
        email(str): Email address connected to Cozify account.
        otp(int): One time passcode.

    Returns:
        str: cloud token
    """

    payload = {
            'email': email,
            'password': otp
    }

    response = requests.post(cloudBase + 'user/emaillogin', params=payload)
    if response.status_code == 200:
        return response.text
    else:
        raise APIError(response.status_code, response.text)

def _lan_ip():
    """1:1 implementation of hub/lan_ip

    This call will fail with an APIError if the requesting source address is not the same as that of the hub, i.e. if they're not in the same NAT network.
    The above is based on observation and may only be partially true.

    Returns:
        list: List of Hub ip addresses.
    """
    response = requests.get(cloudBase + 'hub/lan_ip')
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise APIError(response.status_code, response.text)

def _hubkeys(remoteToken):
    """1:1 implementation of user/hubkeys

    Args:
        remoteToken(str) Cloud remote authentication token.

    Returns:
        dict: Map of hubId: hubToken pairs.
    """
    headers = {
            'Authorization': remoteToken
    }
    response = requests.get(cloudBase + 'user/hubkeys', headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise APIError(response.status_code, response.text)

def _refreshsession(remoteToken):
    """1:1 implementation of user/refreshsession

    Args:
        remoteToken(str) Cloud remote authentication token.

    Returns:
        str: New cloud remote authentication token. Not automatically stored into state.
    """
    headers = {
            'Authorization': remoteToken
    }
    response = requests.get(cloudBase + 'user/refreshsession', headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise APIError(response.status_code, response.text)

def _remote(cloud_token, hub_token, apicall, put=False):
    """1:1 implementation of 'hub/remote'

    Args:
        cloud_token(str): Cloud remote authentication token.
        hub_token(str): Hub authentication token.
        apicall(str): Full API call that would normally go directly to hub, e.g. '/cc/1.6/hub/colors'

    Returns:
        requests.response: Requests response object.
    """

    headers = {
            'Authorization': cloud_token,
            'X-Hub-Key': hub_token
    }
    if put:
        response = requests.put(cloudBase + 'hub/remote' + apicall, headers=headers)
    else:
        response = requests.get(cloudBase + 'hub/remote' + apicall, headers=headers)

    return response
