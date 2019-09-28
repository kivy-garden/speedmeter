from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from math import exp

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory

from kivy_garden.speedmeter import SpeedMeter

class NoValueSpeedMeter(SpeedMeter):

    def value_str(self, n): return ''

_displayed = { 
    0: '0',
    30: u'\u03a0 / 6', 60: u'\u03a0/3', 90: u'\u03a0/2', 120: u'2\u03a0/3',
    150: u'5\u03a0/6',
    180: u'\u03a0', 210: u'7\u03a0/6', 240: u'4\u03a0/3'
    }

class PiValueSpeedMeter(SpeedMeter):

    def value_str(self, n):
        return _displayed.get(n, '')

class Demo1(App):

    def __init__(self):
        App.__init__(self)
        self.clockRunning = True

    def tick(self, *t, **kw):
        ids = self.root.ids

        if self.clockRunning:
            clock = ids.clock
            clock.value += 0.2
            if clock.value > clock.max - 0.001: clock.value = clock.min

        fuel = ids.fuel
        fuel.value -= 0.02 * ids.rpm.value
        if fuel.value < fuel.min: fuel.value = fuel.min

        speed_value = ids.speed_value
        if fuel.value <= fuel.min and speed_value.value > speed_value.min:
            speed_value.value = speed_value.value * 0.9 - 3
            if speed_value.value <= speed_value.min:
                speed_value.value = speed_value.min
                speed_value.disabled = True
        
    def set_speed(self):
        ids = self.root.ids
        fuel = ids.fuel
        ids.rpm.value = exp(ids.speed_value.value / 200.0) * 4.5 - 4.5

    def set_temp(self, temperature, motion):
        v = temperature.get_value(motion.pos)
        if not v: return
        temperature.value = v
        self.root.ids.temperature_display.text = '%.2f' % v

    def set_pi(self):
        ids = self.root.ids
        try: v = float(self.root.ids.pi_text.text)
        except: return
        if v < 0 or v > 240: return
        ids.pi.value = v

example = Demo1()
Clock.schedule_interval(example.tick, 0.5)
example.run()
