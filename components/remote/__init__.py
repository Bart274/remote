"""
homeassistant.components.remote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Component to interface with various remotes.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/remote/
"""
import logging
import os

from homeassistant.components import discovery
from homeassistant.config import load_yaml_config_file
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.const import (
    STATE_OFF, STATE_UNKNOWN, STATE_PLAYING, STATE_IDLE,
    ATTR_ENTITY_ID, ATTR_ENTITY_PICTURE, SERVICE_TURN_OFF, SERVICE_TURN_ON,
    SERVICE_TOGGLE)

DOMAIN = 'remote'
SCAN_INTERVAL = 10

ENTITY_ID_FORMAT = DOMAIN + '.{}'

DISCOVERY_PLATFORMS = {
}

SERVICE_BUTTON_HOME = 'button_home'
SERVICE_BUTTON_VOLUME_UP = 'button_volume_up'
SERVICE_BUTTON_VOLUME_DOWN = 'button_volume_down'
SERVICE_BUTTON_POWER = 'button_power'
SERVICE_BUTTON_PLAY_PAUSE = 'button_play_pause'
SERVICE_BUTTON_NEXT = 'button_next'
SERVICE_BUTTON_PREVIOUS = 'button_previous'
SERVICE_BUTTON_PLAY = 'button_play'
SERVICE_BUTTON_PAUSE = 'button_pause'
SERVICE_BUTTON_UP = 'button_up'
SERVICE_BUTTON_DOWN = 'button_down'
SERVICE_BUTTON_LEFT = 'button_left'
SERVICE_BUTTON_RIGHT = 'button_right'
SERVICE_BUTTON_ENTER = 'button_enter'
SERVICE_BUTTON_BACK = 'button_back'
SERVICE_BUTTON_MENU = 'button_menu'

ATTR_SUPPORTED_COMMANDS = 'supported_commands'

SUPPORT_BUTTON_HOME = 1
SUPPORT_BUTTON_VOLUME_UP = 2
SUPPORT_BUTTON_VOLUME_DOWN = 4
SUPPORT_BUTTON_POWER = 8
SUPPORT_BUTTON_PLAY_PAUSE = 16
SUPPORT_BUTTON_NEXT = 32
SUPPORT_BUTTON_PREVIOUS = 64
SUPPORT_BUTTON_PLAY = 128
SUPPORT_BUTTON_PAUSE = 256
SUPPORT_BUTTON_UP = 512
SUPPORT_BUTTON_DOWN = 1024
SUPPORT_BUTTON_LEFT = 2048
SUPPORT_BUTTON_RIGHT = 4096
SUPPORT_BUTTON_ENTER = 8192
SUPPORT_BUTTON_BACK = 16384
SUPPORT_BUTTON_MENU = 32768

SUPPORT_TURN_ON = 65536
SUPPORT_TURN_OFF = 131072

SERVICE_TO_METHOD = {
    SERVICE_TURN_ON: 'turn_on',
    SERVICE_TURN_OFF: 'turn_off',
    SERVICE_TOGGLE: 'toggle',
    SERVICE_BUTTON_HOME: 'button_home',
    SERVICE_BUTTON_VOLUME_UP: 'button_volume_up',
    SERVICE_BUTTON_VOLUME_DOWN: 'button_volume_down',
    SERVICE_BUTTON_POWER: 'button_power',
    SERVICE_BUTTON_PLAY_PAUSE: 'button_play_pause',
    SERVICE_BUTTON_NEXT: 'button_next',
    SERVICE_BUTTON_PREVIOUS: 'button_previous',
    SERVICE_BUTTON_PLAY: 'button_play',
    SERVICE_BUTTON_PAUSE: 'button_pause',
    SERVICE_BUTTON_UP: 'button_up',
    SERVICE_BUTTON_DOWN: 'button_down',
    SERVICE_BUTTON_LEFT: 'button_left',
    SERVICE_BUTTON_RIGHT: 'button_right',
    SERVICE_BUTTON_ENTER: 'button_enter',
    SERVICE_BUTTON_BACK: 'button_back',
    SERVICE_BUTTON_MENU: 'button_menu',
}

ATTR_TO_PROPERTY = [
    ATTR_SUPPORTED_COMMANDS,
]


def is_on(hass, entity_id=None):
    """ Returns true if specified remote entity_id is on.
    Will check all remotes if no entity_id specified. """
    entity_ids = [entity_id] if entity_id else hass.states.entity_ids(DOMAIN)
    return any(not hass.states.is_state(entity_id, STATE_OFF)
               for entity_id in entity_ids)


def turn_on(hass, entity_id=None):
    """ Will turn on specified remote or all. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_TURN_ON, data)


def turn_off(hass, entity_id=None):
    """ Will turn off specified remote or all. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_TURN_OFF, data)


def toggle(hass, entity_id=None):
    """ Will toggle specified remote or all. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_TOGGLE, data)


def button_home(hass, entity_id=None):
    """ Send the remote command for home button. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_HOME, data)

def button_volume_up(hass, entity_id=None):
    """ Send the remote command for volume up. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_VOLUME_UP, data)

def button_volume_down(hass, entity_id=None):
    """ Send the remote command for volume down. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_VOLUME_DOWN, data)

def button_power(hass, entity_id=None):
    """ Send the remote command for power. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_POWER, data)

def button_play_pause(hass, entity_id=None):
    """ Send the remote command for play/pause. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_PLAY_PAUSE, data)

def button_next(hass, entity_id=None):
    """ Send the remote command for next. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_NEXT, data)

def button_previous(hass, entity_id=None):
    """ Send the remote command for previous. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_PREVIOUS, data)

def button_play(hass, entity_id=None):
    """ Send the remote command for play. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_PLAY, data)

def button_pause(hass, entity_id=None):
    """ Send the remote command for pause. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_PAUSE, data)

def button_up(hass, entity_id=None):
    """ Send the remote command for up. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_UP, data)

def button_down(hass, entity_id=None):
    """ Send the remote command for down. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_DOWN, data)

def button_left(hass, entity_id=None):
    """ Send the remote command for left. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_LEFT, data)

def button_right(hass, entity_id=None):
    """ Send the remote command for right. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_RIGHT, data)

def button_enter(hass, entity_id=None):
    """ Send the remote command for enter. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_ENTER, data)

def button_back(hass, entity_id=None):
    """ Send the remote command for back. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_BACK, data)

def button_menu(hass, entity_id=None):
    """ Send the remote command for menu. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    hass.services.call(DOMAIN, SERVICE_BUTTON_MENU, data)


def setup(hass, config):
    """ Track states and offer events for remote. """
    component = EntityComponent(
        logging.getLogger(__name__), DOMAIN, hass, SCAN_INTERVAL,
        DISCOVERY_PLATFORMS)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def remote_service_handler(service):
        """ Maps services to methods on RemoteDevice. """
        target_remotes = component.extract_from_service(service)

        method = SERVICE_TO_METHOD[service.service]

        for remote in target_remotes:
            getattr(remote, method)()

            if remote.should_poll:
                remote.update_ha_state(True)

    for service in SERVICE_TO_METHOD:
        hass.services.register(DOMAIN, service, remote_service_handler,
                               descriptions.get(service))

    return True


class RemoteDevice(Entity):
    """ ABC for remotes. """
    # pylint: disable=too-many-public-methods,no-self-use

    # Implement these for your remote

    @property
    def state(self):
        """ State of the device. """
        return STATE_UNKNOWN

    @property
    def supported_commands(self):
        """ Flags of commands that are supported. """
        return 0

    def turn_on(self):
        """ turn the device on. """
        raise NotImplementedError()

    def turn_off(self):
        """ turn the device off. """
        raise NotImplementedError()

    # No need to overwrite these.
    @property
    def support_button_home(self):
        """ presses home button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_HOME)

    @property
    def support_button_volume_up(self):
        """ presses volume up button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_VOLUME_UP)

    @property
    def support_button_volume_down(self):
        """ presses volume down button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_VOLUME_DOWN)

    @property
    def support_button_power(self):
        """ presses power button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_POWER)

    @property
    def support_button_play_pause(self):
        """ presses play/pause button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_PLAY_PAUSE)

    @property
    def support_button_next(self):
        """ presses next button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_NEXT)

    @property
    def support_button_previous(self):
        """ presses previous button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_PREVIOUS)

    @property
    def support_button_play(self):
        """ presses play button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_PLAY)

    @property
    def support_button_pause(self):
        """ presses pause button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_PAUSE)

    @property
    def support_button_up(self):
        """ presses up button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_UP)

    @property
    def support_button_down(self):
        """ presses down button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_DOWN)

    @property
    def support_button_left(self):
        """ presses left button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_LEFT)

    @property
    def support_button_right(self):
        """ presses right button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_RIGHT)

    @property
    def support_button_enter(self):
        """ presses enter button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_ENTER)

    @property
    def support_button_back(self):
        """ presses back button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_BACK)

    @property
    def support_button_menu(self):
        """ presses menu button """
        return bool(self.supported_media_commands & SUPPORT_BUTTON_MENU)

    def toggle(self):
        """ Toggles the power on the device. """
        if self.state in [STATE_OFF, STATE_IDLE]:
            self.turn_on()
        else:
            self.turn_off()

    def button_volume_up(self):
        """ volume_up remote. """
        if self.volume_level < 1:
            self.set_volume_level(min(1, self.volume_level + .1))

    def button_volume_down(self):
        """ volume_down remote. """
        if self.volume_level > 0:
            self.set_volume_level(max(0, self.volume_level - .1))

    def button_play_pause(self):
        """ play_pause remote. """
        if self.state == STATE_PLAYING:
            self.button_pause()
        else:
            self.button_play()

    @property
    def state_attributes(self):
        """ Return the state attributes. """
        if self.state == STATE_OFF:
            state_attr = {
                ATTR_SUPPORTED_COMMANDS: self.supported_commands,
            }
        else:
            state_attr = {
                attr: getattr(self, attr) for attr
                in ATTR_TO_PROPERTY if getattr(self, attr) is not None
            }

        return state_attr
