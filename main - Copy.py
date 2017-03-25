#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import WineData

winepy_dir = os.path.join(os.path.dirname(__file__), "winepy")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(winepy_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        wines = WineData.query().fetch()
        params = {"wines": wines}
        return self.render_template("winepy-list.html", params=params)


class AddWineHandler(BaseHandler):
    def get(self):
        return self.render_template("winepy-add.html")

    def post(self):
        getcategory = self.request.get("category")
        getcolor = self.request.get("color")
        getsweetness = self.request.get("sweetness")
        getcountry = self.request.get("country")
        getregion = self.request.get("region")
        getwinery = self.request.get("winery")
        getname = self.request.get("name")
        getvine = self.request.get("vine")
        getyear = int(self.request.get("year"))
        getamount = int(self.request.get("amount"))
        getunit = self.request.get("unit")
        gettried = True if self.request.get("tried") == "True" else False
        #getimage

        wine = WineData(    category=getcategory,
                            color = getcolor,
                            sweetness = getsweetness,
                            country = getcountry,
                            region = getregion,
                            winery = getwinery,
                            name = getname,
                            vine = getvine,
                            year = getyear,
                            amount = getamount,
                            unit = getunit,
                            tried = gettried,
                            #getimage
                        )
        wine.put()

        wines = WineData.query().fetch()
        params = {"wines": wines}
        return self.render_template("winepy-list.html", params=params)


class DetailsWineHandler(BaseHandler):
    def get(self, dbobject_id):
        #image
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy-details.html", params=params)


class DeleteWineHandler(BaseHandler):
    def get(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy-list.html", params=params)

    def post(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        wine.key.delete()
        return self.redirect_to("winepy-list")


class EditWineHandler(BaseHandler):
    def get(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy-edit.html", params=params)

    def post(self, dbobject_id):
        getnewcategory = self.request.get("newcategory")
        getnewcolor = self.request.get("newcolor")
        getnewsweetness = self.request.get("newsweetness")
        getnewcountry = self.request.get("newcountry")
        getnewregion = self.request.get("newregion")
        getnewwinery = self.request.get("newwinery")
        getnewname = self.request.get("newname")
        getnewvine = self.request.get("newvine")
        #getnewyear = int(self.request.get("newyear"))
        getnewamount = int(self.request.get("newamount"))
        getnewunit = self.request.get("newunit")
        #getnewimage = self.request.get("newimage")
        getnewtried = self.request.get("newtried")
        wine = WineData.get_by_id(int(dbobject_id))
        wine.category = getnewcategory
        wine.color = getnewcolor
        wine.sweetness = getnewsweetness
        wine.country = getnewcountry
        wine.region = getnewregion
        wine.winery = getnewwinery
        wine.name = getnewname
        wine.vine = getnewvine
        wine.year = getnewyear
        wine.amount = getnewamount
        wine.unit = getnewunit
        #wine.image = getnewimage
        wine.tried = getnewtried
        wine.put()
        return self.redirect_to("winepy-list")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="winepy-list"),
    webapp2.Route('/add', AddWineHandler, name="winepy-add"),
    webapp2.Route('/delete/<dbobject_id:\d+>', DeleteWineHandler),
    webapp2.Route('/details/<dbobject_id:\d+>', DetailsWineHandler),
    webapp2.Route('/edit/<dbobject_id:\d+>', EditWineHandler),
], debug=True)