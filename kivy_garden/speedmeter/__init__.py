"""
SpeedMeter
==========

Defines the Kivy garden :class:`SpeedMeter` class, a versatile
gauge widget inspired by Andrea Gavana's SpeedMeter for wxPython,
which allows display and input of physical values.
"""

import os.path, sys

from math import atan2, cos, pi, radians, sin

from kivy.core.text import Label
from kivy.graphics import *
from kivy.properties import *
from kivy.uix.image import CoreImage, Image
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

__all__ = ('SpeedMeter', )

__version__ = '0.1.2'

_redraw = tuple('pos size min max'.split())
_redraw_background = tuple('sectors sector_width shadow_color'.split())
_redraw_full_cadran = tuple(
    'tick subtick cadran_color display_first '
    'display_last value_font_size'.split())
_redraw_label = tuple(
    'label label_radius_ratio label_angle_ratio '
    'label_icon label_icon_scale label_font_size'.split())
_redraw_needle = tuple('needle_color'.split())

_image_dir = os.path.join(os.path.dirname(__file__), 'images')

from kivy.graphics.instructions import *

_2pi = 2 * pi  # I trust multiplication by 2 even for floating points !
_halfPi = pi / 2

#
# Each part is stores in its own InstructionGroup, so as to minimize
# redrawing / recomputation when something is modified, except
# outerCadran and values that is really one function, but is split for
# the sake of understandability.
#

_ig = tuple('sectors shadow outerCadran values label needle'.split())


class SpeedMeter(Widget):

    """A versatile gauge widget which allows display and input of
    "physical" values."""

    min = NumericProperty(0)
    max = NumericProperty(100)

    tick = NumericProperty(10)
    subtick = NumericProperty(0)

    display_first = BooleanProperty(True)
    display_last = BooleanProperty(True)

    start_angle = NumericProperty(-90, min=-360, max=360)
    end_angle = NumericProperty(135, min=-360, max=360)

    cadran_color = StringProperty('#ffffff')

    label = StringProperty('')
    label_icon = StringProperty('')
    label_icon_scale = NumericProperty(0.5, min=0, max=1)
    label_font_size = NumericProperty(15, min=1)
    value_font_size = NumericProperty(15, min=1)

    label_radius_ratio = NumericProperty(0.3, min=-1, max=1)
    label_angle_ratio = NumericProperty(0.5, min=0, max=1)

    needle_color = StringProperty('#6bf2ff')
    needle_image = StringProperty('needle.png')

    sectors = ListProperty()
    sector_width = NumericProperty(0, min=0)
    thickness = NumericProperty(1.5, min=0)

    shadow_color = StringProperty('')

    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SpeedMeter, self).__init__(**kwargs)
        # In case on_value is called before _update
        self.a = self.b = self.r2 = self.r = self.centerx = self.centery = 0
        self._shadow = None
        self.rotate = _X
        self._labelRectangle = -1
        self._needle_image = os.path.join(_image_dir, 'needle.png')

        add = self.canvas.add
        for instructionGroupName in _ig:
            ig = InstructionGroup()
            setattr(self, '_%sIG' % instructionGroupName, ig)
            add(ig)

        self.extendedTouch = False
        bind = self.bind
        for eventList, fn in (
                (_redraw, self._redraw),
                (_redraw_background, self._draw_background),
                (_redraw_full_cadran, self._draw_full_cadran),
                (_redraw_label, self._draw_label),
                (_redraw_needle, self._draw_needle),
        ):
            for event in eventList:
                bind(**{event: fn})

    def value_str(self, n):
        """This is the method called to convert data n into the string
represented on the dial. It defaults to str(int(n)). If you want to
have more control over what's written on the dial, you can derive your
own class from SpeedMeter and override this function. See demo1 for an
example using fractions of PI."""
        # Override this if you want more control on the tick display
        return str(int(n))

    def _draw_sectors(self):
        self._sectorsIG.clear()
        add = self._sectorsIG.add
        l = self.sectors[:]
        if not l:
            return
        r = self.r
        centerx = self.centerx
        centery = self.centery
        d = r + r
        a = self.a
        b = self.b
        v0 = l.pop(0)
        a0 = -(a * v0 + b)
        sw = self.sector_width
        if sw:
            r -= sw
        else:
            centerx -= r
            centery -= r
            dd = (d, d)

        while l:
            color = l.pop(0)
            v1 = l.pop(0) if l else self.max
            a1 = -(a * v1 + b)
            add(Color(rgba=get_color_from_hex(color)))
            if sw:
                add(Line(circle=(centerx, centery, r, a0, a1),
                         width=sw, cap='none'))
            else:
                add(Ellipse(pos=(centerx, centery),
                            size=dd, angle_start=a0, angle_end=a1))
            a0 = a1

    def _set_shadow_value(self):
        if not self._shadow:
            return
        a0 = -(self.a * self.min + self.b)
        a1 = -(self.a * self.value + self.b)
        self._shadow.circle = (self.centerx, self.centery, self.r - 5, a0, a1)

    def _draw_shadow(self):
        self._shadowIG.clear()
        self._shadow = None
        if not self.shadow_color:
            return
        add = self._shadowIG.add
        add(Color(rgba=get_color_from_hex(self.shadow_color)))
        self._shadow = Line(width=5, cap='none')
        add(self._shadow)
        self._set_shadow_value()

    def _draw_outer_cadran(self):
        self._outerCadranIG.clear()
        add = self._outerCadranIG.add
        centerx = self.centerx
        centery = self.centery
        r = self.r
        theta0 = self.start_angle
        theta1 = self.end_angle
        add(Color(rgba=get_color_from_hex(self.cadran_color)))
        if theta0 == theta1:
            add(Line(circle=(centerx, centery, r), width=1.5))
        else:
            rt0 = radians(theta0)
            rt1 = radians(theta1)
            add(Line(points=(
                centerx + r * sin(rt0),
                centery + r * cos(rt0),
                centerx, centery,
                centerx + r * sin(rt1),
                centery + r * cos(rt1),
            ),
                     width=1.5,
            ))
            add(Line(circle=(centerx, centery, r, theta0, theta1), width=1.5))

    # I'm using theta for the angle, as to not confuse it with
    # transparency (alpha as in in rgba)

    def _draw_values(self):
        self._valuesIG.clear()
        add = self._valuesIG.add
        centerx = self.centerx
        centery = self.centery
        r = self.r
        value_str = self.value_str
        values = [
            Label(value_str(i), bold=True, font_size=self.value_font_size)
            for i in range(self.min, self.max + 1, self.tick)]
        if len(values) <= 1:
            # Tick is bigger than max - min
            return
        for _ in values:
            _.refresh()

        theta0 = self.start_angle
        theta1 = self.end_angle
        if theta0 == theta1:
            theta1 += 360
        deltaTheta = radians((theta1 - theta0) / float(len(values) - 1))
        theta = radians(theta0)
        r_10 = r - 10
        r_20 = r - 20
        subtick = int(self.subtick)
        if subtick:
            subDeltaTheta = deltaTheta / subtick
        else:
            subDeltaTheta = None
        # Should be more efficient on texture allocation
        for value in values:
            first = value is values[0]
            last = value is values[-1]
            c = cos(theta)
            s = sin(theta)
            r_1 = r - 1
            if (
                    not first and not last
                    or first and self.display_first
                    or last and self.display_last):
                # Draw the big tick
                add(Line(points=(
                    centerx + r_1 * s, centery + r_1 * c,
                    centerx + r_10 * s, centery + r_10 * c,
                ), width=2))
                # Numerical value
                t = value.texture
                tw, th = t.size
                add(Rectangle(
                    pos=(centerx + r_20 * s - tw / 2,
                         centery + r_20 * c - th / 2),
                    size=t.size,
                    texture=t))
            # Subtick
            if subDeltaTheta and not last:
                subTheta = theta + subDeltaTheta
                for n in range(subtick):
                    subc = cos(subTheta)
                    subs = sin(subTheta)
                    add(Line(points=(
                        centerx + r * subs, centery + r * subc,
                        centerx + r_10 * subs, centery + r_10 * subc),
                             width=0.75))
                    subTheta += subDeltaTheta
            theta += deltaTheta

    def _draw_label(self, *t):
        self._labelIG.clear()
        if not self.label and not self.label_icon:
            return

        theta = self.start_angle + (
            self.label_angle_ratio * (self.end_angle - self.start_angle))
        c = cos(radians(theta))
        s = sin(radians(theta))
        r = self.r
        r1 = r * self.label_radius_ratio
        if self.label_icon:
            label = CoreImage(self.label_icon)
            t = label.texture
            iconSize = max(t.size)
            scale = r * self.label_icon_scale / float(iconSize)
            tw, th = t.size
            tw *= scale
            th *= scale
        else:
            label = Label(text=self.label, markup=True, bold=True,
                          font_size=self.label_font_size)
            label.refresh()
            t = label.texture
            tw, th = t.size
        self._labelIG.add(
            Rectangle(
                pos=(self.centerx + r1 * s - tw / 2,
                     self.centery + r1 * c - th / 2),
                size=(tw, th),
                texture=t))

    def on_needle_image(self, *t):
        self._needle_image = self.needle_image
        full_path = os.path.join(_image_dir, self._needle_image)
        if os.path.isfile(full_path):
            self._needle_image = full_path
        self._draw_needle(*t)

    def _draw_needle(self, *t):
        self._needleIG.clear()
        add = self._needleIG.add
        add(PushMatrix())
        self.rotate = Rotate(origin=(self.centerx, self.centery))
        add(self.rotate)

        if self.value < self.min:
            self.value = self.min
        elif self.value > self.max:
            self.value = self.max
        needleSize = self.r
        s = needleSize * 2
        add(Color(rgba=get_color_from_hex(self.needle_color)))
        add(Rectangle(
            pos=(self.centerx - needleSize, self.centery - needleSize),
            size=(s, s),
            source=self._needle_image))
        add(PopMatrix())
        self.on_value()

    def _draw_background(self, *t):
        self._draw_sectors()
        self._draw_shadow()

    def _draw_full_cadran(self, *t):
        self._draw_outer_cadran()
        self._draw_values()

    def _redraw(self, *args):
        diameter = min(self.size)
        sa = self.start_angle
        ea = self.end_angle

        r = self.r = diameter / 2
        self.r2 = r * r
        x, y = self.pos
        width, height = self.size
        self.centerx = x + width / 2
        self.centery = y + height / 2

        #
        # compute value -> angle mapping
        #

        theta0 = sa
        theta1 = ea
        if theta0 == theta1:
            theta1 += 360
        self.a = (float(theta0) - theta1) / (self.max - self.min)
        self.b = -theta0 - self.a * self.min

        #
        # Reverse mapping
        #
        self.startTheta = _halfPi - radians(sa)
        self.endTheta = _halfPi - radians(ea)
        self.direct = self.startTheta < self.endTheta

        self.ra = (self.max - self.min) / ((self.endTheta - self.startTheta)
                                           if sa != ea else _2pi)
        self.rb = self.min - self.ra * self.startTheta

        #
        # Draw
        #
        self._draw_background()
        self._draw_full_cadran()
        self._draw_label()
        self._draw_needle()

    def on_value(self, *t):
        self.rotate.angle = self.a * self.value + self.b
        self._set_shadow_value()

    def get_value(self, pos):
        c = self.center
        x = pos[0] - c[0]
        y = pos[1] - c[1]
        r2 = x * x + y * y
        if r2 > self.r2:
            return
        theta = atan2(y, x)
        theta_ = theta

        min_, max_ = ((self.startTheta, self.endTheta)
                      if self.direct
                      else (self.endTheta, self.startTheta))
        if theta < min_:
            theta += _2pi
        elif theta > max_:
            theta -= _2pi

        v = self.ra * theta + self.rb
        if v >= self.min and v <= self.max:
            return v
        if not self.extendedTouch:
            return
        # Should make distinction between min and max here

    def collide_point(self, x, y):
        return self.get_value(*(x, y)) is not None

    def on_start_angle(self, *t):
        if self.end_angle - self.start_angle > 360:
            self.start_angle = self.end_angle - 360
        self._redraw()

    def on_end_angle(self, *t):
        if self.end_angle - self.start_angle > 360:
            self.end_angle = self.start_angle + 360
        self._redraw()


class _X:
    pass
