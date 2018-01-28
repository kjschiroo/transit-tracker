class ArrivalPattern(object):

    def __init__(
        self,
        light_numbers,
        time_color,
        light_time_map,
        arrival_func,
        to_direction,
        station_color,
        outer_station_light
    ):
        self._light_numbers = light_numbers
        self._time_color_func = time_color_func
        self._light_time_map = light_time_map
        self._arrival_func = arrival_func
        self._to_direction = to_direction
        self._station_color = station_color
        self._outer_station_light = outer_station_light

    def run(self):
        commands = []
        arrival_times = self._arrival_func()
        for i, (low, high) in enumerate(self._light_time_map):
            times = [t for t in arrival_times if low < t and t <= high]
            if len(times) == 0:
                continue
            commands.append(
                (self._get_light_number(i), self._time_color_func(min(times)))
            )
        commands.append((self._get_inner_station_light(), self._station_color))
        commands.append((self._outer_station_light, self._station_color))
        return commands

    def _get_light_number(self, light_index):
        dir_coef = 1
        start = 0
        if self._direction.lower() == 'left':
            dir_coef = -1
            start = len(self._light_numbers) - 1
        return start + (dir_coef * light_index)

    def _get_inner_station_light(self):
        end = len(self._light_numbers) - 1
        if self._direction.lower() == 'left':
            end = 0
        return end
