import os
import glob
import json
import random
import logging
import pandas as pd
import tornado
from tornado import websocket, web, ioloop, gen, escape
from tornado.log import enable_pretty_logging

logger = logging.getLogger("tornado.application")
enable_pretty_logging()

KEY_DIR = os.getenv('iot_key_dir')
IOT17_STUDENTS = os.getenv('NetId_19csv')
NET = "192.168.1.0"
# For 2019 batch, we will have 2 users per RPI. If there is 1 per Pi, remove the `* 2`
RPI_IP_POOL = [NET.replace(NET.split('.')[-1], str(host)) for host in range(51, 61)] * 2
AUTHORIZED_USERS = {}
CLIENTS = []
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
        username = AUTHORIZED_USERS[self.current_user.decode('utf-8').strip('"')]['FirstName']
        logger.info("User {} logged in".format(username))
        # if IP = 192.168.1.44, the key assigned = 44.key
        # The things you need to do to convert between bytes and string!!!
        pi_ip=AUTHORIZED_USERS[self.current_user.decode('utf-8').strip('"')]['Ip']
        key_path = os.path.join(os.path.relpath(KEY_DIR), pi_ip.split('.')[-1],
                                "files", "root", "home", "pi", ".ssh", "private.key")
        pivpn_path = os.path.join(os.path.relpath(KEY_DIR), pi_ip.split('.')[-1],
                                  "files", "vpnkeys", "pivpn{0}.ovpn".format(pi_ip.split('.')[-1]))
        myvpn_path = os.path.join(os.path.relpath(KEY_DIR), pi_ip.split('.')[-1],
                                  "files", "vpnkeys", "myvpn{0}.ovpn".format(pi_ip.split('.')[-1]))
        self.render("index.html",
                    title="IOTclass",
                    username=username,
                    pi_ip=pi_ip,
                    myKey=key_path,
                    pivpnKey=pivpn_path,
                    myvpnKey=myvpn_path)

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


class RealtimeHandler(websocket.WebSocketHandler):
    """
    Class to handle the sockets
    """
    def check_origin(self, origin):
        """
        Accept all cross-origin traffic
        """
        return True

    def open(self):
        #print("Socket Opened by: "+escape.json_decode(self.get_secure_cookie("user")))
        if self.get_secure_cookie("user"):
            self.write_message("Socket opened")
            if not self in CLIENTS:
                CLIENTS.append(self)
        else:
            self.close(code=401, reason="Unauthorized")
            return

    def on_message(self, message):
        print("Message Recieved: " + message)

    def on_close(self):
        if self in CLIENTS:
            CLIENTS.remove(self)
        #print("Socket closed")

class StatusUploadHandler(BaseHandler):
    """
    Class to handle the status upload from sensors
    """
    def get(self):
        pass

    def post(self):
        self.status_info = json.loads(self.request.body)
        uploaded_by = self.request.headers.get('Id')
        for client in CLIENTS:
            if escape.json_decode(client.get_secure_cookie("user")) == uploaded_by:
                client.write_message(self.status_info)
                break
        self.write("OK")

class WarningHandler(BaseHandler):
    """
    a 404 handler
    """
    def get(self, resource):
        username = ""
        try:
            username = AUTHORIZED_USERS[self.current_user.decode('utf-8').strip('"')]["FirstName"]
        except Exception as ex:
            username = ""
        self.render("404.html",
                    title="Error",
                    comment="Hey common now {user}, \
                    you know you are not allowed to be here, right?".format(user=username))

    def post(self):
        pass

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
        (r"/status_upload", StatusUploadHandler),
        (r"/realtime", RealtimeHandler),
        (r"/keys/(.*)", web.StaticFileHandler,{'path': os.path.relpath(KEY_DIR)}),
        (r"/(.*)", WarningHandler),
    ],
    **settings
)

if __name__ == "__main__":
    # Update authorized users first
    update_authorized_users()
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
