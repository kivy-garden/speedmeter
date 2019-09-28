API
###

.. currentmodule: speedmeter

.. class:: SpeedMeter

Physical values and their representation
****************************************

.. attribute:: value
      
    The physical value. Setting it moves the hand.

    :attr:`value` is a :kprop:`NumericProperty`, float values are ok,
    and default to 0. If :attr:`value` is lower than :attr:`min` or
    greater than :attr:`max`, behavior is undefined (it's up to you to
    catch the value and apply some behaviour if you're so inclined).

.. attribute:: min
      
    The minimum physical value.

    :attr:`min` is a :kprop:`NumericProperty`, must be an integer and
    defaults to 0.

.. attribute:: max

    The maximum physical value.

    :attr:`max` is a :kprop:`NumericProperty`, must be an integer and defaults to 100.

    Note that you must have :attr:`min` < :attr:`max`, or undefined results will occur.

.. attribute:: tick

    :attr:`tick` is the physical value between ticks. So for example,
    if :attr:`tick` is 15, with :attr:`min` = 0 and :attr:`max` = 100,
    the values represented on the dial will be 0, 15, 30, 45, 60, 75
    and 90. Note that, since in this case 15 doesn't evenly divide the
    0..100 interval, the last value isn't represented, so it is
    preferable if there is a coherence between :attr:`min`,
    :attr:`max` and :attr:`tick`, but it won't prevent the widget from
    working otherwise.

    :attr:`tick` is a :kprop:`NumericProperty`, must be an integer and defaults to 10.

.. attribute:: subtick

    :attr:`subtick` is the number of sub-divisions between 2 ticks
    (without label), thus it is the number of divisions, not a
    physical value. If it is 0 or 1, there are no subticks.

    :attr:`subtick` is a :kprop:`NumericProperty`, must be an integer and defaults to 0 (no subtick).

.. attribute:: display_first

    If ``True`` (the default), :attr:`min` label isn't drawn on the
    dial. This is useful mainly if you draw a (real) clock where :attr:`min` =
    0 and :attr:`max` = 12, but you draw only 12 on the clock face and don't
    want it to be cluttered by the 0.

    You could get a similar result by overriding :attr:`value_str`,
    but drawing clocks is common enough to deserve this convenience
    value.

    :attr:`display_first` is a :kprop:`BooleanProperty` and defaults to ``True``.

.. attribute:: display_last

    If ``True`` (the default), the label isn't drawn on the dial. This
    function exists mostly by symmetry with :attr:`display_first`.

    :attr:`display_last` is a :kprop:`BooleanProperty`, and defaults
    to ``True``.

.. attribute:: start_angle
.. attribute:: end_angle

    These are the angle at which the dial starts and ends. The basis
    for the frame is Kivy's, that is the angles go from 0 to 360
    (actually -360 to 360), 0 is up, 90 is right 180 is down and so
    on, like a map. If :attr:`start_angle` < :attr:`end_angle`, the
    physical values increase clockwise, they increase
    counter-clockwise if :attr:`end_angle` > :attr:`start_angle`. So
    for example, if :attr:`start_angle` = -90 and :attr:`end_angle` =
    90, the dial is a half-circle on the upper half, and values are
    increasing clockwise. If :attr:`start_angle` = 270 (same position
    as -90 geometrically) and :attr:`end_angle` = 90, the dial is a
    half-circle on the lower half, and values are increasing
    counter-clockwise (since :attr:`start_angle` >
    :attr:`end_angle`). You can play with :ref:`demo2` to get a
    feeling of how things influence each others and find the value
    suiting your needs if you find reasoning on the value too tedious.

    :attr:`start_angle` = :attr:`end_angle` is a special case. In that
    case, the dial is a full circle, and the values increase
    clockwise. There is no way to have counter-clockwise value
    increases yet !

    :attr:`start_angle` and :attr:`end_angle` are :kprop:`NumericProperty`. :attr:`start_angle` defaults to -90 and :attr:`end_angle` defaults to 135.

.. attribute:: value_font_size

    Quite self-explanatory. Most likely, you don't want to change this.

    :attr:`value_font_size` is a :kprop:`NumericProperty`, and defaults to 15.

Indication on the dial
**********************

  .. attribute:: label
   
    If set, the corresponding text is drawn on the dial. By default,
    the text is at equal distance from :attr:`min` and :attr:`max` and at
    about 1/3 in the dial. This can be changed with
    :attr:`label_radius_ratio` and :attr:`label_angle_ratio`.

    label is a :kprop:`StringProperty` and defaults to '' (nothing to display).

.. attribute:: label_font_size

    Quite self-explanatory. 

    :attr:`label_font_size` is a :kprop:`NumericProperty`, and defaults to 15.

.. attribute:: label_icon

    If set, this is the name of an image (file or atlas part) put on
    the dial. By default, the text is at equal distance from
    :attr:`min` and :attr:`max` and at about 1/3 in the dial. This can
    be changed with :attr:`label_radius_ratio` and :attr:`label_angle_ratio`.

    By default, the icon size is half the '''radius''' of the
    dial. This can be changed with :attr:`label_icon_scale`.

    If both :attr:`label` and :attr:`label_icon` are set, :attr:`label_icon` takes precedence.

    :attr:`label_icon` is a :kprop:`StringProperty` and defaults to ''
    (nothing to display).

.. attribute:: label_icon_scale

    The ratio between the radius of the dial and the size of the
    icon. Default to 0.5, which is more or less balanced. Useful
    values run from 0 (icon reduced to a single point) to 2.0 (icon
    covers the surface of the dial).

    :attr:`label_icon_scale` is a :kprop:`NumericProperty` and
    defaults to 0.5 (icon is half of the radius).

.. attribute:: label_radius_ratio

    The position of the icon or label from the center of the dial. 0
    means the center of the icon is at the center of the dial, 1 that
    the icon is on the border of the dial, -1 on the border of the
    dial in the opposite direction. Defaults to 0.3, which puts the
    icon at a readable place on the dial.

    :attr:`label_radius_ratio` is a :kprop:`NumericProperty` and defaults to 0.3.

.. attribute:: label_angle_ratio

    The position of the icon or :attr:`label` between the :attr:`min`
    and :attr:`max` position. Defaults to 0.5, meaning that the icon
    is at equal distance from the :attr:`min` and :attr:`max` labels
    (number on the dial). 0 means the icon is on the min label, 1 that
    it is on the max label. You can't use this property to go outside
    of the dial, but you can use a negative :attr:`label_radius_ratio`
    for that purpose.

    :attr:`label_angle_ratio` is a :kprop:`NumericProperty` and defaults to 0.5.

.. attribute:: needle_color

    The hand ("needle") color. This is a *string* interpreted as an hex_color.

    :attr:`needle_color` is a :kprop:`StringProperty` and defaults to
    #6bf2ff, which is close to a slider default color on Linux.

.. attribute:: needle_image

    The hand ("needle") image.

    :attr:`needle_image` is a :kprop:`StringProperty` and defaults to
    'needle.png', a needle picture liberally stolen from the original
    kivy speedmeter widget ! The widget comes with 2 other images
    ``needle2`` and ``needle3``.

.. attribute:: shadow_color

    If present, this is the #RGB description of the color of the
    "shadow" (an arc of circle marking the position of the needle). If
    it's not present, there is no shadow. Currently, the shadow width
    can't be specified.

Sectors
*******

Color sectors can be drawn on the dial, for example to symbolize the
cool, warm and overheat part of a dial. This is driven by the :attr:`sectors`
and :attr:`sector_width` properties described below.

.. attribute:: sectors

    This is a list of alternating values and colors. The values are
    expressed in "physical" terms (a value between min and max),
    colors are expressed as hex_color strings. If the last value is
    omitted, it defaults to :attr:`max`. So for example, if your
    physical values represent the body of human temperature with
    min=34, max=44, a white arc for hypothermia between 34 and 36° C,
    green arc between 36 and 38, red between 38 and 42, and nothing
    after 42 to mean death (!), you do it by putting ``[34, '#ffffff',
    36, '#00ff00', 38, '#ff0000', 42]`` in :attr:`sectors`. The
    physical values must be between :attr:`min` and :attr:`max`
    included, must be sorted in increasing order, and don't have to be
    integer values.

    :attr:`sectors` is a :kprop:`ListProperty` and defaults to ``[]``, meaning no sector is drawn.

.. attribute:: sector_width

    This is the width of the sectors. The special value 0 (default)
    means the whole sector is drawn. Other values indicate the width
    of the arc, in that case only an arc is drawn.

    :attr:`sector_width` is a :kprop:`NumericProperty` and defaults to 0.

Other Methods
*************

.. method:: get_value(pos)
    
    :param pos: a pair (x, y).
    :return: the corresponding physical value

    The x,y position has to be inside the dial or ``None`` is
    returned. For example, if you get a ``MotionEvent``, you can find
    the corresponding physical value (in the :attr:`min`.. :attr:`max`
    range) with ``get_value(*motionevent.pos)``.

.. method:: collide_point(x, y)

    This standard widget function is implemented.

.. method:: value_str(n)
    
    :param int n:

    This is the method called to convert data n into the string
    represented on the dial. It defaults to str(int(n)). If you want
    to have more control over what's written on the dial, you can
    derive your own class from SpeedMeter and override this
    function. See :ref:`demo1` for an example using fractions of PI.
