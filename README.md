Repressive - remotely impressive
--------------------------------

Repressive is an extension to the presentation tool [Impressive](http://impressive.sourceforge.net/), which allows you to control your impressive presentation from another device like a mobile phone. You are able to see the next slides in advance and do not need to look behind you to see the current slide on the beamer image.

Dependencies
------------

Repressive needs a slightly patched version of Impressive, which supports an event queue, to enable other threads to execute their events in the main thread.
A patched version of Impressive and the needed patch are included.

Further you need to install the dependencies for Impressive and additionally the web framework [Flask](http://flask.pocoo.org/).

For Debian:

- Impressive: python-opengl, python-pygame, python-imaging, poppler-utils | xpdf-utils (>= 3.02-2)
- Flask: python-flask

Usage
-----

Run ``repressive.py`` with the usual options for Impressive. Then point a web browser i.e. on your mobile phone to ``http://hostname:5000``.
You can now control the presentation using the web interface on another device.
