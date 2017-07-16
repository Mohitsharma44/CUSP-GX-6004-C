import os
import glob
import random
import pandas as pd
from tornado import websocket, web, ioloop, gen, escape

KEY_DIR = os.getenv('iot_key_dir')
IOT17_STUDENTS = os.getenv('NetId_17csv')
NET = "192.168.1.0"
RPI_IP_POOL = [NET.replace(NET.split('.')[-1], str(host)) for host in range(50, 81)]
AUTHORIZED_USERS = {}
# Randomize the pool to assign to the authorized users
# before the server is initialized
random.shuffle(RPI_IP_POOL)

def update_authorized_users():
    """
    Update the dict of `AUTHORIZED_USERS`
    """
    try:
        if not os.path.exists(IOT17_STUDENTS):
            raise("FileNotFound")
        # Read the csv file
        students_df = pd.read_csv(IOT17_STUDENTS)
        # Delete all the Ip from RPI_IP_POOL that
        # are already allocated
        [RPI_IP_POOL.remove(ip) for ip in students_df[students_df['Ip'].notnull()]['Ip']]
        # Allocate the remaining Ip to unallocated
        # users
        to_be_filled = students_df[students_df['Ip'].isnull()].shape[0]
        if to_be_filled > 0:
            students_df.loc[students_df['Ip'].isnull(), 'Ip'] = RPI_IP_POOL[:to_be_filled]
            # write the updated dataframe to csv file
            students_df.to_csv(IOT17_STUDENTS)
        # update authorized_users dict
        [AUTHORIZED_USERS.update(
            {x['NetId']: {'FirstName': x['FirstName'],
                          'LastName': x['LastName'],
                          'Ip': x['Ip']}})
         for x in students_df.to_dict(orient='records')]
    except Exception as ex:
        print("Error updating authorized users: "+str(ex))


class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):

    def get_key_path(self):
        dict_key_netid = {}
        keys  = None
        paths = glob.glob(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../keys") + "/*.key")
        keys  = [os.path.basename(k)[:-4] for k in paths]

    @web.asynchronous
    @web.authenticated
    def get(self):
        userid = escape.xhtml_escape(self.current_user)
        # if IP = 192.168.1.44, the key assigned = 44.key
        key_path = os.path.join(os.path.relpath(KEY_DIR),
                                AUTHORIZED_USERS[self.current_user.decode('utf-8')
                                                 .strip('"')]['Ip'].split('.')[-1]) + ".key"
        self.render("index.html",
                    title="IOTclass",
                    # The things you need to do to convert between bytes and string!!!
                    username=AUTHORIZED_USERS[self.current_user.decode('utf-8').strip('"')]
                    ['FirstName'],
                    pi_ip=AUTHORIZED_USERS[self.current_user.decode('utf-8').strip('"')]
                    ['Ip'],
                    myKey=key_path)

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
        (r"/keys/(.*)", web.StaticFileHandler,{'path': os.path.relpath(KEY_DIR)}),
    ],
    **settings
)

if __name__ == "__main__":
    # Update authorized users first
    update_authorized_users()
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
