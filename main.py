#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2
import urllib2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env= jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


#art_key = db.Key.from_path('ASCIIChan', 'arts')

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


"""IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return"""



class Art(db.Model):
    latt = db.TextProperty(required = True)
    longi = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

 

class MainPage(Handler):

    def render_front(self, latt="", longi="", error=""):
        
        arts = db.GqlQuery("SELECT * FROM Art "
                            
                                "ORDER BY created DESC"
                                )
        self.render("index.html", latt=latt, longi=longi, error=error, arts=arts)

    def get(self):
        self.render_front()

    def post(self):
        latt = self.request.get("latt")
        longi = self.request.get("longi")

        if latt and longi:
            a = Art(latt = latt, longi = longi)
            a.put()

            #self.write("thanks!")

            self.redirect("/")

        else :
            error = "we need both a title and some artwork!"
            self.render_front(latt, longi, error)

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
