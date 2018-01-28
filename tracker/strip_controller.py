from time import sleep
from collections import defaultdict
import threading
import neopixel
from . import color


def _tracker_color_to_neopixel_color(tracker_color):
    return neopixel.color(
        tracker_color.red, tracker_color.green, tracker_color.blue
    )

def _get_transition_color(old_color, new_color, step, total_steps):
    return color.TrackerColor(
        _get_single_channel_transition_color(
            old_color.red, new_color.red, step, total_steps
        ),
        _get_single_channel_transition_color(
            old_color.green, new_color.green, step, total_steps
        ),
        _get_single_channel_transition_color(
            old_color.blue, new_color.blue, step, total_steps
        )
    )

def _get_single_channel_transition_color(old, new, step, total_steps):
    diff = old - new
    color_step_size = diff / total_steps
    return int(new + color_step_size * (total_steps - (step + 1)))


class StripController(object):

    def __init__(
        self,
        strip,
        commands=[]
    ):
        self._keep_looping = True
        self._strip = strip
        self.set_lights(commands)
        self._current_state = defaultdict(lambda: color.TrackerColor(0, 0, 0))
        self._hold_interval = 2
        self._transition_step_count = 20
        self._transition_time = 0.5

        self._strip.begin()

    def set_lights(self, commands):
        sorted_commands = defaultdict(list)
        for light, color in commands:
            sorted_commands[light].append(color)
        self._commands = sorted_commands

    def start(self):
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()

    def _loop(self):
        while(self._keep_looping):
            self._apply_commands_to_strip()
            sleep(self._hold_interval)

    def _apply_commands_to_strip(self):
        end_state = self._get_target_state()
        self._transition_to_new_state(end_state)
        self._current_state = end_state

    def _transition_to_new_state(self, new_state):
        total_steps = self._transition_step_count
        step_size = 1 / total_steps
        for step in range(total_steps):
            for light in range(self._strip.numPixels):
                old_led_state = self._current_state[light]
                new_led_state = new_state[light]
                if new_led_state == old_led_state:
                    continue
                transition_state = _get_transition_color(
                    old_led_state, new_led_state, step, total_steps
                )
                self._strip.setPixelColor(
                    light,
                    _tracker_color_to_neopixel_color(transition_state)
                )
            self._strip.show()
            sleep(self._transition_time/total_steps)

    def _get_target_state(self):
        target_state = defaultdict(lambda: color.TrackerColor(0, 0, 0))
        for light, color_set in self._commands:
            to_color = color_set.pop(0)
            color_set.append(to_color)
            target_state[light] = to_color
