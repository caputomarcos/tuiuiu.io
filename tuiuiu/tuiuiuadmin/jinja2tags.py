from __future__ import absolute_import, unicode_literals

import jinja2
from jinja2.ext import Extension

from .templatetags.tuiuiuuserbar import tuiuiuuserbar


class TuiuiuUserbarExtension(Extension):
    def __init__(self, environment):
        super(TuiuiuUserbarExtension, self).__init__(environment)

        self.environment.globals.update({
            'tuiuiuuserbar': jinja2.contextfunction(tuiuiuuserbar),
        })


# Nicer import names
userbar = TuiuiuUserbarExtension
