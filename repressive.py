#!/usr/bin/python
#
# Repressive, a remote control for Impressive
# Copyright (C) 2015 Alexander Schier <allo -at- laxu -dot- de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import impressive
import sys
import thread
import time
import traceback
import base64

from flask import Flask, Response, render_template, redirect, url_for
from StringIO import StringIO


def repressive_mainthread():
    app = Flask(__name__)

    def page_image(page):
        try:
            tmp = StringIO()
            if page == 0 or page > impressive.PageCount:
                img = impressive.DummyPage()  # impressive.OverviewImage
            else:
                img = impressive.RenderPDF(page, not impressive.ZoomMode,
                                           impressive.ZoomMode)
            img.save(tmp, "png")
            return Response(tmp.getvalue(), mimetype="image/png")
        except Exception, e:
            traceback.print_exc()

    @app.route("/page/current")
    def current_page():
        return page_image(impressive.Pcurrent)

    @app.route("/page/prev")
    def prev_page():
        return page_image(impressive.Pcurrent - 1)

    @app.route("/page/next")
    def next_page():
        return page_image(impressive.Pcurrent + 1)

    @app.route("/page/<int:number>")
    def page(number):
        return page_image(number)

    @app.route("/goto/<int:number>")
    def goto(number):
        try:
            impressive.ActionQueue.append((
                impressive.TransitionTo,
                [number, False]
            ))
            impressive.Platform.ScheduleEvent("$queue-action", 1)
            return redirect(url_for('main'))
        except Exception, e:
            traceback.print_exc()

    @app.route("/goto/next")
    def goto_next():
        return goto(impressive.GetNextPage(impressive.Pcurrent, 1))

    @app.route("/goto/prev")
    def goto_prev():
        return goto(impressive.GetNextPage(impressive.Pcurrent, -1))

    @app.route("/")
    def main():
        return render_template(
            "main.html",
            prev=(impressive.Pcurrent -1),
            next=(impressive.Pcurrent +1)
        )

    app.run(host="0.0.0.0", threaded=True)
LOGO = """
iVBORw0KGgoAAAANSUhEUgAAAQAAAABACAAAAADQNvZiAAALZElEQVR42u1beVgURxavGWa4hkME
FQ/I4rHeBwQMRo1447lRE9YYL1jvJRLjGlfNZ7w1ajafxou4rrdG4xFWjSKKAqsbb9cc7nqbbIx3
1CCiMPP2vao5unt6Bhr49vsUfn8wr35d772q6qpXr7sLxipQgQpU4PnB4A0T9KU2Ehxd+Xnt/ycA
0L+UNgxLzPDk7eez/4FmHIBRpTTyAdqAW8/nAIQUYtOrls6Gx0MagAe653MEhp3eWq+UJqKp/3Cg
/IbR4XwAppTfAZjJB6CJuypeSqKSt3pFP/9SG9EFmuhHbygWrRGqLtdQ/y8p2e4frSQYGeu3Jxdu
LKtp3zN6f3YpH+D+7iGegvAevohqmkzJmXkAj/cnGUpgxBqOuq0+j1Ht0TfT467faVYE3W0ON75y
okO/q6AW90LZNGoxL8xv4dYl4iANwMcKchafFnCVtToqpBsi1OgGXwIbLsbw1h3jhZ8G3rHx39bT
bESg83mQ4D339Cwbsdyu/6G9Uk3mec4mX3HnknCRyNcUA/CTqHtsK8j8BO+WtuXXKKQaC9ks4X+u
qdUIR4rUBkAf9/QPNiLR3ugrNqogiL1iVzjjxiXHE6TueCgGYJOk/oOcR/h3MrLV+TCar2UfvcWv
fIdqgT/aK97MPvKAC7u0GuE3WkySfxy8+IxLtdzSbLPNsiN6rbcyj5IYq/KztXC1lWuXHFWIWe0U
GULrWz3cG+vLqu8r2IQxLICm1cMPwuh6+xO22+FZn0cRONGGUoneV0lurNUI4giKGbw3VRajeIq5
pRkLb968+XWAXElnwnuTvU5Gkj1jMb/J7xamc+OS42UiXlcJjl/zpm+rJuIQ/VmC5bN1rJe51c+4
mEEVJ1ofScLuY2GCdiNGDHMw29qbr+BZPHNHC/jj6jgsazRNx9FC3ILiOObOpcDrWM7zde6/Zz5N
6n4Spjm6u/+SIwejW8MDDM37VDs/UVIqvhHmkUtDlXdsxYhII/PpFGHbAdRpgTi8tEDGrERmN5eG
orRf59alwFgsp7lIEDODpMynyOReteMGFrOIb4DCj45dvi0W12k2wtjf7fHiSc7vHfPaBc0xAdk3
ZUxfGi0fFOr+CnC3RhEuORZgOUllAMY48TfBCZ8TPwSFvzDZAMzSbISxoJMS7oJtxrqiOb5A6iUZ
E1CAVHdcOccdK921S461OD8qu8iPZOlhoLMdmE4XlqKQwmS7cYJmI7SU4rdctpOHHDmgOk3AGHhb
0ezDWGkpY3PxZ2XRLgn9C58NUMsav5cHWDHT702Ug0f7k8KnFRG/oKKvZiO6tu3oxxQ9cGYObfz5
Ip90QQtUsy94JotA11h7rHvBVIRLG6qGqPU/ANWyZUx1GrpGzjW9aX++FWwt+ZyULIjiG6GY/YZN
TqBKIe5ogZ5Ynqqw04yndf/FZCimKJfu0QG1FsoY/W2kzlW3p/ORg7ryna8Vn1R7xQi0+w9lggGa
jdBmfNrWufH2FzQuaCtmIBGvbDj2HX6RPt66cmlblAnj2ipt9Nx67MQ11PrhBOL43k5WegnPslYN
6BDTddBHWY+x0Jfod8Wyur1wSK9knnHmxWo3MoXo+4tHdoztOZnnDuLOuqDrrsgmq/fowYOE9N6O
xv9VNCfHsfJcuLRuy5SvD5b3v7MiYhy3Lbl7ylgySJnwEh52K4GRLxVkFs/mXNABTnH9gqP1/UTm
/RtJqFB3KXCWypvkAzBbUX2N7UJLhaVdtOEyCtEZDvJkvZIYOSUn1/qIyup0rFNU3ymZ0rQRguwd
r7pLe5QCGC8fgJiLhZLat9Y7NsnQNfk22nx2cax4LUlPnLrk24L+55u6khhhQy+nbcmzsk93vmqr
q06bDjyRdejOllDFRqi4paouBehR+4hX8WNjUO+piz6dPLRLUz/7Sw9xe727jJ+R8ka1EhoRr5P6
jJ2zfP6EzoGsOLQ2uHCJYzNlwdule8s0zUUmWW6wFwegTjnuvwcGmBsGj3Lae/0c24up/M3l+JOC
QGB5HIAFku2/XM6ACEx3OTIXVmUVqEAFKlCBCrjJGVt3be5E1uzSpaZa5Z43bo4sU+9lblA76ubD
ZqcDbfMB2qlVngsQV6bey9ygdrS3wDynWbELCn+rlmOnQWH9Mk3ay9pgCTARYIiS8/0eMk1qlb1N
vmXrvQwNejWJCq7ak1ZuUK9x8XXsnHfr4X3DGNM1T+zf2v6KJaDHqO616SWRV7M0sAyI4O+LHHp1
cFn4NYmqy58mfVHQ232EqRslkgV3GBsX6rIxjPm0fSfOKJPIoF9klPAfGhUVptDQgjgLzHxijmRh
qyz0EJBaw8rRBwFz73oHiExvw6vWSOVVVtfiNRBbsKcKvXnheWCmr0e6pQDL9XYf89WNIvnHDVSy
TPR20Rhdnwv0xSRcKpHByALIojNMPkfxVsg0tGECP4MR0uW69TEoPcTK8bfRN8TvXppwHa9Z2cwI
9j4X5jMm00N2qNcxgPZYu9lTyI5w+EhUNzrB8fz1iU69Mf3FkZK1eolEBitdAnNDxr9lbjTINLSB
zmGk9umQD5aPu76WdBpgBufMyS0H0RmV9ITI2RYw444XnQ+wLiF6agHAMl38CoAdwyJZS6mebiNV
XMXPExjSAJIdPswt1I2S9/QRrYecAD5vVBpjOgvmMaMKYJ+XQ+IGDV/xLSfgDJibypqhDZ5f06dQ
/+Ng7knF8FxI8yTuD1j4E/BYa9gPlmjmdwwsyTSl+5khqzJ9ln+HOesVBNOVZYz1MMN2b4ePghBV
o0SmVkI2+BuAMaqNafgU/+jqNQ1nDokbpFf14xlLBphbWaqhcQCq5sJuH5pGOxNGI4b/Cw6akDvo
J16QLKPNbS8UNmCDABbxmOONQ96ALQVLLFPqPYYvjaxFAWzz8DkC5iiJjzRPVaNI7qvE60ynr19q
jcHACntHBokQa5W4QdaFLAWfh4MhMg2NA/ByIVrR75S8C9rjhdxqnXhBMkj0ODtAv52mMb+fOVBY
w3AACqsr9aIL6dxYpcuQ6TcCYJ5O4mM5UzNKpPWj3zg6C6PWGI/VPEaOwjGzS9wgq/0EthknAQyX
a2gcgCSayt6npR999Eni+B6mNXirMfjnwQ6j1ykoqMI1quVCum/gZVqKznopOLnx3rb9N2QES328
y9SMskSAjrwKhg9LjGpjmCGR7x2NmEPiBpnPGTjU8DJs95JraByAJWBpxXy+BXPfllbUIK41XjJh
WkOT9hUzLOFV+Edp3UKAObQe1zEVvVZYYw62AiwDZT5eVTVKx11EpIx9BvtMqo0hl3S2so1E4gZ5
zD0A5hgVjeIDYxFOZY/dANNofnZduiHFSFwNseY+p5RmFLWSqqRiDqJPMcOhqqwH/7Kr0MsgW4zW
JsB6g9yHqlEkIYPSnpjvaAWoNSbl7t3hTL8DR98uNRT1xHkoCkxyDW0D4H8R9uF2PJBOQg2bhGvJ
0pa4dC9b+oJI5fHuLayyffT0HOABd4aYu3K9S7g2GF+bFOCkPtJ9VY3607HW7D+/txE3+NWeqo3B
1OLwGEyVNhgcEjeINloWAmSFKpuhDTSVceyM62wfGxM4t57G831xbtWYCYXoxfg3a5XseCZuCXOh
h2sTJsl9rNepGm3w1L50V/mpN6aB+HCaESGRbLZCcq1HB2Ua2tANJw9/jkukz+KWOQ0k3AYR9wOu
ULzDTifSqdGsKRTcfM7BYT9XetHPYE+A0oeq0Xjcwz+kz86739K7aAz7Hc2S+UFSyVbPeAh2iQP9
Mo2SIrRdRFHrp1ZcbX2Ret6HRLgrBqYBdGKG+lG13Bk1NmrkqZRK1vz/E8YALC3efyzptoG58Qv3
qiz8qghMxXmoPwOH/V+0/uvXUFJfPNTMgy9evA/R/pVMxf2XPZ2/q39WKkP8D2MNVqSPMgFDAAAA
AElFTkSuQmCC
"""

impressive.ParseOptions(sys.argv[1:])
thread.start_new_thread(repressive_mainthread, tuple())
impressive.LOGO = LOGO
impressive.run_main()
