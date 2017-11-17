#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("SecNumber.html")
    def post(self):
        secret_number = 13
        guess = int(self.request.get("guess"))

        result = 0

        if secret_number == guess:
            result = "Čestitam, %s je skrito število! Nagrado dobite pri izhodu." % secret_number
        elif guess > 20:
            result = "Vnešeno število je večje od 20."
        elif secret_number != guess:
            result = "Žal %s ni skrito število." % guess

        params = {"result": result}

        return self.render_template("guess.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),

], debug=True)
