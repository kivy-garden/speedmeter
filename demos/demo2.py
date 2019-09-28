from kivy.config import Config
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 775)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.factory import Factory
from kivy.properties import *

from kivy_garden.speedmeter import SpeedMeter

class Demo2(App):

    currentColor = StringProperty('')

    def on_start(self):
        self.sm = self.root.ids['sm']
        self.sm.bind(on_touch_down=self._touch_down)
        self.field2Set = False # Dirty

    def _setVectorColor(self, hex_color):
        sm = self.sm
        if not sm.sectors:
            sm.sectors = [sm.min]
        if self.lastPick <= sm.sectors[-1]: return
        sm.sectors = sm.sectors + [hex_color, self.lastPick]
        self.root.ids['sector_width'].disabled = False

    def _setCadranColor(self, hex_color):
        self.sm.cadran_color = hex_color

    def _setShadowColor(self, hex_color):
        self.sm.shadow_color = hex_color

    def _setNeedleColor(self, hex_color):
        self.sm.needle_color = hex_color

    def _touch_down(self, sm, motionEvent):
        if motionEvent.button == 'left':
            v = sm.get_value(motionEvent.pos)
            if v is None: return
            sm.value = v
        else:
            self.lastPick = sm.get_value(motionEvent.pos)
            if self.sm.sectors and self.lastPick <= self.sm.sectors[-1]: return
            self.colorPicker = Factory.ColorPickerDialog()
            self.colorPicker._exampleCallback = self._setVectorColor
            self.colorPicker.open()

    def setLabelControlState(self, modal):
        #if modal.field2Set != 'label_icon_scale': return
        w = self.root.ids
        w['label_icon_scale'].disabled = not self.sm.label_icon
        sm = self.sm
        disabled = not sm.label and not sm.label_icon
        w['label_radius_ratio'].disabled = disabled
        w['label_angle_ratio'].disabled = disabled

        disabled = not sm.label or sm.label_icon
        w['label_font_size'].disabled = disabled

Demo2().run()
