from time import sleep
import neopixel
from tracker.strip_controller import StripController
from tracker.color import TrackerColor
from tracker.tracker import Tracker
from tracker.arrival_pattern import ArrivalPattern
import tracker.data_gather as dg
from tracker.strip_controller import StripController
from tracker.map_pattern import MapPattern

high = 255
med = 60
low = 10
dark = 0

# Setup the neopixel strip
LED_COUNT = 50
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = neopixel.ws.WS2811_STRIP_GRB

strip = neopixel.Adafruit_NeoPixel(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    LED_STRIP
)

patterns = {}

# Setup arrival pattern
lights = [i for i in range(43, 50)]
light_times = [
    (0, 120),
    (120, 240),
    (240, 330),
    (330, 390),
    (390, 450),
    (450, 540),
    (540, 700)
]

def time_color_func(time):
    if time < 330:
        return TrackerColor(med, dark, dark)
    if time < 360:
        return TrackerColor(med, med, dark)
    if time < 450:
        return TrackerColor(dark, high, dark)
    return TrackerColor(dark, low, dark)

arrival_func = dg.get_arrival_func('902', dg.WEST, 'HMUN')

to_direction = 'left'
station_color = TrackerColor(med, med, med)
outer_station_light = 20

patterns['arrival'] = ArrivalPattern(
    lights,
    light_times,
    time_color_func,
    arrival_func,
    to_direction,
    station_color,
    outer_station_light
)


# Setup map patterns
green_blue_stations_coord_map = {
    'TF22': (44.983454, -93.278563),
    'TF12': (44.982736, -93.277117),
    'WAR2': (44.983454, -93.278563),
    '5SNI': (44.982736, -93.277117),
    'GOVT': (44.983454, -93.278563),
    'USB2': (44.982736, -93.277117),
}

blue_stations_coord_map = {
    'CDRV': (44.968304, -93.250985),
    'FRHI': (44.962653, -93.247116),
    'LAHI': (44.948343, -93.238866),
    '38HI': (44.934725, -93.229500),
    '46HI': (44.920878, -93.219964),
    '50HI': (44.912306, -93.209999),
    'VAMC': (44.903026, -93.202371),
    'FTSN': (44.893273, -93.198062),
    'LIND': (44.880916, -93.205610),
    'HHTE': (44.874105, -93.224121),
    'AM34': (44.858723, -93.223163),
    'BLCT': (44.856370, -93.226433),
    '28AV': (44.855756, -93.231688),
    'MAAM': (44.854280, -93.238857),
}
blue_stations_coord_map.update(green_blue_stations_coord_map)

green_stations_coord_map = {
    'WEBK': (44.971945, -93.246249),
    'EABK': (44.973671, -93.231104),
    'STVI': (44.974752, -93.222862),
    'PSPK': (44.971723, -93.215258),
    'WGAT': (44.967480, -93.206473),
    'RAST': (44.963069, -93.195434),
    'FAUN': (44.956399, -93.178742),
    'SNUN': (44.955682, -93.166995),
    'HMUN': (44.955703, -93.156844),
    'LXUN': (44.955725, -93.146635),
    'VIUN': (44.955725, -93.136505),
    'UNDA': (44.955721, -93.126284),
    'WEUN': (44.955761, -93.116144),
    'UNRI': (44.955705, -93.105144),
    'ROST': (44.954011, -93.097458),
    '10CE': (44.950596, -93.097532),
    'CNST': (44.946178, -93.092275),
    'UNDP': (44.948189, -93.086793),
}
green_stations_coord_map.update(green_blue_stations_coord_map)

red_stations_coord_map = {
    'APVY': (44.725670, -93.217764),
    'CE47': (44.735674, -93.217670),
    'CE14': (44.747151, -93.217649),
    'CGTR': (44.812497, -93.218207),
    'MAAM': (44.854280, -93.238857),
}

station_light_map = {
    'CDRV': 37,
    'FRHI': 35,
    'LAHI': 33,
    '38HI': 31,
    '46HI': 29,
    '50HI': 27,
    'VAMC': 25,
    'FTSN': 23,
    'LIND': 21,
    'HHTE': 19,
    'AM34': 17,
    'BLCT': 15,
    '28AV': 13,
    'TF22': 41,
    'TF12': 41,
    'WAR2': 42,
    '5SNI': 40,
    'GOVT': 39,
    'USB2': 38,
    'WEBK': 36,
    'EABK': 34,
    'STVI': 32,
    'PSPK': 30,
    'WGAT': 28,
    'RAST': 26,
    'FAUN': 24,
    'SNUN': 22,
    'HMUN': 20,
    'LXUN': 18,
    'VIUN': 16,
    'UNDA': 14,
    'WEUN': 12,
    'UNRI': 10,
    'ROST': 8,
    '10CE': 6,
    'CNST': 4,
    'UNDP': 1,
    'APVY': 3,
    'CE47': 5,
    'CE14': 7,
    'CGTR': 9,
    'MAAM': 11,
}

## East-bound Green line
active_stations_func = dg.get_active_stations_func(
    '902', dg.EAST, green_stations_coord_map
)

patterns['e-green'] = MapPattern(
    station_light_map,
    active_stations_func,
    TrackerColor(med, med, dark)
)

## West-bound Green line
active_stations_func = dg.get_active_stations_func(
    '902', dg.WEST, green_stations_coord_map
)

patterns['w-green'] = MapPattern(
    station_light_map,
    active_stations_func,
    TrackerColor(dark, med, dark)
)

## South-bound Blue line
active_stations_func = dg.get_active_stations_func(
    '901', dg.SOUTH, blue_stations_coord_map
)

patterns['s-blue'] = MapPattern(
    station_light_map,
    active_stations_func,
    TrackerColor(med, dark, med)
)

## North-bound Blue line
active_stations_func = dg.get_active_stations_func(
    '901', dg.NORTH, blue_stations_coord_map
)

patterns['n-blue'] = MapPattern(
    station_light_map,
    active_stations_func,
    TrackerColor(dark, dark, med)
)

## South-bound Red line
active_stations_func = dg.get_active_stations_func(
    '903', dg.SOUTH, red_stations_coord_map
)

patterns['s-red'] = MapPattern(
    station_light_map,
    active_stations_func,
    TrackerColor(med, 0.5*med, dark)
)

## North-bound Red line
active_stations_func = dg.get_active_stations_func(
    '903', dg.NORTH, red_stations_coord_map
)

patterns['n-red'] = MapPattern(
    station_light_map,
    active_stations_func,
    TrackerColor(med, dark, dark)
)

# Startup the tracker
t = Tracker(patterns, StripController(strip))
t.start()
while(True):
    continue
