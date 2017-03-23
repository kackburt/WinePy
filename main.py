#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import WineData
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

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


class MainHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        wines = WineData.query().fetch()
        params = {"wines": wines}
        return self.render_template("winepy.html", params=params)
#class AddWineHandler(BaseHandler):
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
        #getimage = self.request.get("image")
        try:
            getimage = self.get_uploads()[0]
            wine_image = WineData(
                wine=wines.get_current_user().user_id(),
                image=upload.key())
            wine_image.put()
            self.redirect_to("winepy-home")
        except:
            self.error(500)
        gettried = True if self.request.get("tried") == "True" else False


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
                            #image = getimage,
                            tried = gettried,
                        )
        wine.put()

        wines = WineData.query().fetch()
        params = {"wines": wines}
        return self.render_template("winepy.html", params=params)


class EditWineHandler(BaseHandler):
    def get(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy_edit.html", params=params)

    def post(self, dbobject_id):
        getnewcategory = self.request.get("newcategory")
        getnewcolor = self.request.get("newcolor")
        getnewsweetness = self.request.get("newsweetness")
        getnewcountry = self.request.get("newcountry")
        getnewregion = self.request.get("newregion")
        getnewwinery = self.request.get("newwinery")
        getnewname = self.request.get("newname")
        getnewvine = self.request.get("newvine")
        getnewyear = int(self.request.get("newyear"))
        getnewamount = int(self.request.get("newamount"))
        getnewunit = self.request.get("newunit")
        getnewimage = self.request.get("newimage")
        getnewtried = self.request.get("newtried")
        wine = WineData.get_by_id(int(dbobject_id))
        wine.category = getnewcategory,
        wine.color = getnewcolor,
        wine.sweetness = getnewsweetness,
        wine.country = getnewcountry,
        wine.region = getnewregion,
        wine.winery = getnewwinery,
        wine.name = getnewname,
        wine.vine = getnewvine,
        wine.year = getnewyear,
        wine.amount = getnewamount,
        wine.unit = getnewunit,
        wine.image = getnewimage,
        wine.tried = getnewtried,
        wine.put()
        return self.redirect_to("winepy-home")


class DeleteWineHandler(BaseHandler):
    def get(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy_delete.html", params=params)

    def post(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        wine.key.delete()
        return self.redirect_to("winepy-home")


class NotTriedWineHandler(BaseHandler):
    def get(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy_nottried.html", params=params)

    def post(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        wine.tried = False
        wine.put()
        return self.redirect_to("winepy-home")


class TriedWineHandler(BaseHandler):
    def get(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        params = {"wine": wine}
        return self.render_template("winepy_tried.html", params=params)

    def post(self, dbobject_id):
        wine = WineData.get_by_id(int(dbobject_id))
        wine.tried = True
        wine.put()
        return self.redirect_to("winepy-home")


class ImageUploadFormHandler(BaseHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/imageupload')
        files = blobstore.BlobInfo.all().fetch(300)
        params = {'upload_url':upload_url, 'files':files, 'n_files':len(files)}
        self.render_template("winepy_imageupload.html", params=params)


class ImageUploadHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            wine_image = WineData(
                wine=wines.get_current_user().user_id(),
                image=upload.key())
            wine_image.put()
            self.redirect_to("winepy-add")
        except:
            self.error(500)


class ViewImageHandler(BaseHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, image_key):
        image_url = images.get_serving_url(image_key)
        if not image_url:
            self.error(404)
        else:
            self.redirect(image_url)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="winepy-home"),
    #webapp2.Route('/add', AddWineHandler, name="winepy-add"),
    webapp2.Route('/edit/<dbobject_id:\d+>', EditWineHandler),
    webapp2.Route('/delete/<dbobject_id:\d+>', DeleteWineHandler),
    webapp2.Route('/imageupload', ImageUploadHandler),
    webapp2.Route('/viewimage/<photo_key:([^/]+)?>', ViewImageHandler),
    webapp2.Route('/nottried/<dbobject_id:\d+>', NotTriedWineHandler),
    webapp2.Route('/tried/<dbobject_id:\d+>', TriedWineHandler)
], debug=True)