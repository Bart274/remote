"""
homeassistant.components.remote.firetv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides functionality to interact with FireTV devices.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/remote.firetv/
"""
import logging
import requests

from homeassistant.const import (
    STATE_PLAYING, STATE_PAUSED, STATE_IDLE, STATE_OFF,
    STATE_UNKNOWN, STATE_STANDBY)

from homeassistant.components.remote import (
    RemoteDevice,
    SUPPORT_BUTTON_HOME, SUPPORT_BUTTON_VOLUME_UP, SUPPORT_BUTTON_VOLUME_DOWN,
    SUPPORT_BUTTON_POWER, SUPPORT_BUTTON_PLAY_PAUSE, SUPPORT_BUTTON_NEXT,
    SUPPORT_BUTTON_PREVIOUS, SUPPORT_BUTTON_PLAY, SUPPORT_BUTTON_PAUSE,
    SUPPORT_BUTTON_UP, SUPPORT_BUTTON_DOWN, SUPPORT_BUTTON_LEFT,
    SUPPORT_BUTTON_RIGHT, SUPPORT_BUTTON_ENTER, SUPPORT_BUTTON_BACK,
    SUPPORT_BUTTON_MENU, SUPPORT_TURN_ON, SUPPORT_TURN_OFF)

SUPPORT_FIRETV = SUPPORT_PAUSE | \
    SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_PREVIOUS_TRACK | \
    SUPPORT_NEXT_TRACK | SUPPORT_VOLUME_SET

SUPPORT_FIRETV = SUPPORT_BUTTON_HOME | SUPPORT_BUTTON_VOLUME_UP | \
    SUPPORT_BUTTON_VOLUME_DOWN | SUPPORT_BUTTON_POWER | \
    SUPPORT_BUTTON_PLAY_PAUSE | SUPPORT_BUTTON_NEXT | \
    SUPPORT_BUTTON_PREVIOUS | SUPPORT_BUTTON_PLAY | SUPPORT_BUTTON_PAUSE | \
    SUPPORT_BUTTON_UP | SUPPORT_BUTTON_DOWN | SUPPORT_BUTTON_LEFT | \
    SUPPORT_BUTTON_RIGHT | SUPPORT_BUTTON_ENTER | SUPPORT_BUTTON_BACK | \
    SUPPORT_BUTTON_MENU | SUPPORT_TURN_ON | SUPPORT_TURN_OFF

DOMAIN = 'firetv'
DEVICE_LIST_URL = 'http://{0}/devices/list'
DEVICE_STATE_URL = 'http://{0}/devices/state/{1}'
DEVICE_ACTION_URL = 'http://{0}/devices/action/{1}/{2}'

_LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Sets up the FireTV platform. """
    host = config.get('host', 'localhost:5556')
    device_id = config.get('device', 'default')
    try:
        response = requests.get(DEVICE_LIST_URL.format(host)).json()
        if device_id in response['devices'].keys():
            add_devices([
                FireTVDevice(
                    host,
                    device_id,
                    config.get('name', 'Amazon Fire TV')
                )
            ])
            _LOGGER.info(
                'Device %s accessible and ready for control', device_id)
        else:
            _LOGGER.warning(
                'Device %s is not registered with firetv-server', device_id)
    except requests.exceptions.RequestException:
        _LOGGER.error('Could not connect to firetv-server at %s', host)


class FireTV(object):
    """ firetv-server client.

    Should a native Python 3 ADB module become available, python-firetv can
    support Python 3, it can be added as a dependency, and this class can be
    dispensed of.

    For now, it acts as a client to the firetv-server HTTP server (which must
    be running via Python 2).
    """

    def __init__(self, host, device_id):
        self.host = host
        self.device_id = device_id

    @property
    def state(self):
        """ Get the device state. An exception means UNKNOWN state. """
        try:
            response = requests.get(
                DEVICE_STATE_URL.format(
                    self.host,
                    self.device_id
                    )
                ).json()
            return response.get('state', STATE_UNKNOWN)
        except requests.exceptions.RequestException:
            _LOGGER.error(
                'Could not retrieve device state for %s', self.device_id)
            return STATE_UNKNOWN

    def action(self, action_id):
        """ Perform an action on the device. """
        try:
            requests.get(
                DEVICE_ACTION_URL.format(
                    self.host,
                    self.device_id,
                    action_id
                    )
                )
        except requests.exceptions.RequestException:
            _LOGGER.error(
                'Action request for %s was not accepted for device %s',
                action_id, self.device_id)


class FireTVDevice(RemoteDevice):
    """ Represents an Amazon Fire TV device on the network. """

    # pylint: disable=abstract-method

    def __init__(self, host, device, name):
        self._firetv = FireTV(host, device)
        self._name = name
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        """ Get the device name. """
        return self._name

    @property
    def should_poll(self):
        """ Device should be polled. """
        return True

    @property
    def supported_commands(self):
        """ Flags of commands that are supported. """
        return SUPPORT_FIRETV

    @property
    def state(self):
        """ State of the device. """
        return self._state

    def update(self):
        """ Update device state. """
        self._state = {
            'idle': STATE_IDLE,
            'off': STATE_OFF,
            'play': STATE_PLAYING,
            'pause': STATE_PAUSED,
            'standby': STATE_STANDBY,
            'disconnected': STATE_UNKNOWN,
        }.get(self._firetv.state, STATE_UNKNOWN)

    def turn_on(self):
        """ Turns on the device. """
        self._firetv.action('turn_on')

    def turn_off(self):
        """ Turns off the device. """
        self._firetv.action('turn_off')

    def button_media_play(self):
        """ Send play command. """
        self._firetv.action('media_play')

    def button_media_pause(self):
        """ Send pause command. """
        self._firetv.action('media_pause')

    def button_media_play_pause(self):
        """ Send play/pause command. """
        self._firetv.action('media_play_pause')

    def button_volume_up(self):
        """ Send volume up command. """
        self._firetv.action('volume_up')

    def button_volume_down(self):
        """ Send volume down command. """
        self._firetv.action('volume_down')

    def button_media_previous_track(self):
        """ Send previous track command (results in rewind). """
        self._firetv.action('media_previous')

    def button_media_next_track(self):
        """ Send next track command (results in fast-forward). """
        self._firetv.action('media_next')

    def button_home(self):
        """ Send home command """
        self._firetv.action('home')

    def button_up(self):
        """ Send up action """
        self._firetv.action('up')

    def button_down(self):
        """ Send down action. """
        self._firetv.action('down')

    def button_left(self):
        """ Send left action. """
        self._firetv.action('left')

    def button_right(self):
        """ Send right action. """
        self._firetv.action('right')

    def button_enter(self):
        """ Send enter action. """
        self._firetv.action('enter')

    def button_back(self):
        """ Send back action. """
        self._firetv.action('back')

    def button_menu(self):
        """ Send menu action. """
        self._firetv.action('menu')
