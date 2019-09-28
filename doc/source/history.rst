History
#######

I need (a lot of) different gauges for a `robotic project
<https://tronche.com/wiki/Almabraxas/3B>`_ I'm doing, to monitor
voltage, current, motors rpm and many other parameters related to the
inner thinking of the robot. When troubleshooting, the robot console
has to run on a "device", and I was undecided when starting which kind
of device it would be, PC, tablet or other. So I just started writing
the console using the (excellent) wxPython, meaning using a PC as the
console in the field. I used Andrea Gavana SpeedMeter for the gauges
and was very happy with it, in particular its flexibility in
representing various range of data.

However, I finally decided that, in the field, a tablet was better
suited to be able to "travel lightly", so to speak. This ruled out
wxPython, and I started to use Kivy for its ability to run both under
Linux and Android, which I must say has been very satisfactory so
far. However, in switching to Kivy I lost my beloved speedmeter, so I
took a few weeks to rewrite it under Kivy, learning Kivy along the
way. I saw that Kivy graphical model was based on GL, and I had used
it back in the 90s (not openGL, the original GL on Silicon Graphics
workstations), so I wasn't in completely unknown territory.
