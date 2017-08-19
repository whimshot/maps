"""Maps for a kivy app."""
import configparser
import logging
import logging.handlers
import pprint

import kivy.app
import kivy.clock
import kivy.config
import kivy.core.window
import kivy.garden.mapview
import kivy.uix.boxlayout
import kivy.uix.relativelayout

kivy.config.Config.set('graphics', 'resizable', 0)
kivy.config.Config.set('graphics', 'width', 800)
kivy.config.Config.set('graphics', 'height', 480)
kivy.core.window.Window.size = (800, 480)

config = configparser.ConfigParser()
config.read('maps.conf')

pp = pprint.PrettyPrinter(indent=4)

MAXLOGSIZE = config.getint('Logging', 'maxlogsize')
ROTATIONCOUNT = config.getint('Logging', 'rotationcount')
LOGGERNAME = config.get('Logging', 'loggername')

# create logger
logger = logging.getLogger(LOGGERNAME)
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
logger_fh = logging.handlers.RotatingFileHandler(LOGGERNAME + '.log',
                                                 maxBytes=MAXLOGSIZE,
                                                 backupCount=ROTATIONCOUNT)
logger_fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
logger_ch = logging.StreamHandler()
logger_ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
logger_formatter = logging.Formatter('%(asctime)s'
                                     + ' %(levelname)s'
                                     + ' %(name)s[%(process)d]'
                                     + ' %(message)s')
logger_fh.setFormatter(logger_formatter)
logger_ch.setFormatter(logger_formatter)
# add the handlers to the logger
logger.addHandler(logger_fh)
logger.addHandler(logger_ch)


class OurMapSource(kivy.garden.mapview.MapSource):
    """A map source with what we want."""

    def __init__(self, **kwargs):
        """Put together MapLayout."""
        super().__init__(**kwargs)
        try:
            self.logger = logging.getLogger(LOGGERNAME + '.' + __name__ + '.'
                                            + self.__class__.__name__)

            self.logger.info('Instantiating %s.', self.__class__.__name__)
            _useless = ['osm', 'osm-hot', 'osm-de', 'osm-fr', 'cyclemap',
                        'thunderforest-cycle', 'thunderforest-transport',
                        'thunderforest-landscape',
                        'thunderforest-outdoors']
            openstreetmap = self.providers['osm']
            for _map in _useless:
                self.logger.debug('deleting %s', _map)
                del self.providers[_map]
            self.providers['Open Street Map'] = openstreetmap
            for mymap in ['transport', 'landscape',
                          'outdoors', 'cycle',
                          'transport-dark']:

                map_base = mymap + '_base'
                map_cache = mymap + '_cache_key'
                map_name_key = mymap + '_name'

                BASE = config.get('Thunderforest', map_base)
                APIKEY = config.get('Thunderforest', 'apikey')
                URL = BASE + 'apikey=' + APIKEY
                ATTRIBUTION = config.get('Thunderforest', 'attribution')
                CACHE_KEY = config.get('Thunderforest', map_cache)
                MAP_NAME = config.get('Thunderforest', map_name_key)
                self.map_name = MAP_NAME
                self.logger.info('Setting up map source: {0}'.format(URL))
                self.providers[MAP_NAME] = (0, 0, 17, URL, ATTRIBUTION)
        except Exception:
            self.logger.exception(
                'Failed to instantiate {}.'.format(self.__class__.__name__))
        finally:
            providers = '\n\n' + pp.pformat(self.providers)
            self.logger.info(providers)


class OurMapView(kivy.garden.mapview.MapView):
    """docstring for OurMapView."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_source = OurMapSource()
        self.lat = 42.291351
        self.lon = -71.123314
        self.zoom = 14
        self.house = kivy.garden.mapview.MapMarker(
            lat=42.291351,
            lon=-71.123314,
            source='house.png')
        self.add_marker(self.house)


class MapBar(kivy.uix.boxlayout.BoxLayout):
    """MapBar for a map."""

    def __init__(self, **kwargs):
        """Put together MapBar."""
        super().__init__(**kwargs)
        try:
            self.logger = logging.getLogger(LOGGERNAME + '.' + __name__ + '.'
                                            + self.__class__.__name__)

            self.logger.debug('Setting up {0}.'.format(
                self.__class__.__name__))
        except Exception:
            self.logger.exception(
                'Failed to instantiate {}.'.format(self.__class__.__name__))
        finally:
            pass

    def center_map(self):
        """Bring the map back home."""
        self.parent.ourmap.center_on(42.291351, -71.123314)
        self.parent.ourmap.set_zoom_at(14, 42.291351, -71.123314)


class MapLayout(kivy.uix.relativelayout.RelativeLayout):
    """A layout for our maps that includes a toolbar."""

    mapsource = OurMapSource()

    def __init__(self, **kwargs):
        """Put together MapLayout."""
        super().__init__(**kwargs)
        try:
            self.logger = logging.getLogger(LOGGERNAME + '.' + __name__ + '.'
                                            + self.__class__.__name__)

            self.logger.debug('Setting up {0}.'.format(
                self.__class__.__name__))
        except Exception:
            self.logger.exception(
                'Failed to instantiate {}.'.format(self.__class__.__name__))
        finally:
            pass


class MapsApp(kivy.app.App):
    """The Apps the thing."""

    def __init__(self, **kwargs):
        """Build that InforMaticApp."""
        super().__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger(LOGGERNAME
                                  + self.__class__.__name__)

            self.logger.info("Creating an instance of " + __name__)
        except Exception:
            self.logger.exception("Caught exception.")
        finally:
            pass

    def build(self):
        """Build the app."""
        ml = MapLayout()
        return ml


if __name__ == '__main__':
    MapsApp().run()
