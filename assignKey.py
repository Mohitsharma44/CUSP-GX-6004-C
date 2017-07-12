import os
import glob
import random
import pandas as pd
from tornado import websocket, web, ioloop, gen, escape

AUTHORIZED_USERS = {}
[AUTHORIZED_USERS.update(
    {x['NYU NetID']: {'First Name': x['First Name'],
                      'Last Name': x['Last Name']}})
 for x in pd.read_csv(os.getenv('NetId_17csv')).to_dict(orient='records')]


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @web.asynchronous
    @web.authenticated
    def get(self):
        userid = escape.xhtml_escape(self.current_user)
        self.render("index.html",
                    title="IOTclass",
                    # The things you need to do to convert between bytes and string!!!
                    username=AUTHORIZED_USERS[self.current_user.decode('utf-8').strip('"')]
                    ['First Name'])

    def post(self):
        pass


class LoginHandler(BaseHandler):
    def get(self):
        try:
            error_msg = self.get_argument("error")
        except Exception:
            error_msg = ""
        self.render("login.html", errormessage=error_msg)

    def post(self):
        userid = self.get_argument("netid", "")
        if userid in AUTHORIZED_USERS.keys():
            self.set_current_user(userid)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + escape.url_escape("UserID incorrect")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", escape.json_encode(user))
        else:
            self.clear_cookie("user")


class LogoutHandler(BaseHandler):
    """
    Logout user and clear the cookie
    """
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", u"/"))


class KeyDownloadHandler(BaseHandler):
    """
    Class to provide download of key
    """
    def get(self):
        self.render("index.html", title="",
                    login_form=True, myKey="",
                    authenticated=False)

    def post(self):
        dict_key_netid = {}
        keys  = None
        paths = glob.glob(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "keys") + "/*.key")
        keys  = [os.path.basename(k)[:-4] for k in paths]
        netid = self.get_argument("netid")
        validate = False
        checkId  = pd.read_csv("CUSP_F17_Students.csv", usecols=[2])
        if (checkId["NYU NetID"].str.contains(netid).any()):
            validate = True
        if validate:
            if ((netid not in dict_key_netid) and keys):
                assignKey = random.choice(keys)
                dict_key_netid[netid] = assignKey
                keys.pop(keys.index(assignKey))
                path = os.path.join("../keys", assignKey) + ".key"
            else:
                keyFound = dict_key_netid[netid]
                path = os.path.join("../keys", keyFound) + ".key"
            self.render("index.html", title="IOT Keys",
                        myKey=path, login_form="True",
                        authenticated=True)

settings = {
    'login_url': '/login',
    'template_path': 'templates/',
    'compiled_template_cache': 'False',
    'debug': True,
    'cookie_secret': "Mysup3rS3cr3tC00kie",
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
}


def make_app():
    return web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/key", KeyDownloadHandler),
        (r"/keys/(.*)", web.StaticFileHandler,{'path': "../keys"}),
    ],
    **settings
)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
