class MapPattern(object):

    def __init__(
        self,
        station_light_map,
        active_station_func,
        color
    ):
        self._station_light_map = station_light_map
        self._active_station_func = active_station_func
        self._color = color

    def run(self):
        commands = []
        active_stations = self._active_station_func()
        return [
            (self._station_light_map[station], self._color)
            for station in active_stations
        ]
