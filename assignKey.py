import tornado.ioloop
import tornado.web
import tornado.httpserver
import pandas as pd
import random
import glob
import os

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html", title="", myKey="")

    def post(self):

	paths = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys") + "/*.key")

	#map(lambda x: os.path.basename(x)[:-4], paths)
	keys = [os.path.basename(k)[:-4] for k in paths]

	#dict_key_netid = {dk:0 for dk in keys}	
	dict_key_netid = {}

	netid = self.get_argument("netid")
	validate = 0
    
	checkId = pd.read_csv("CUSP_F17_Students.csv", usecols=[2])

	if (checkId["NYU NetID"].str.contains(netid).any()):
		validate = 1    

	if(validate == 1):
	
		if ((netid not in dict_key_netid) and len(keys)):
		
			assignKey = random.choice(keys)
			dict_key_netid[netid] = assignKey
			keys.pop(keys.index(assignKey))
			path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys", assignKey) + ".key"		

			self.render("index.html", title = "IOT Keys", myKey = path)
		else:
			
			keyFound = dict_key_netid[netid]
			path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys", keyFound) + ".key"		
			self.render("index.html", title = "IOT Keys", myKey = path)
		 			

settings = {
    'template_path': 'templates/',
    'compiled_template_cache': 'False',
    'debug': False,
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")
}


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
	(r"/(.*)", tornado.web.StaticFileHandler, {'path':"/home/himanshu/Documents/tornadoFileServer/keys"}),
    ],
    **settings
)

if __name__ == "__main__":
    app = tornado.httpserver.HTTPServer(make_app())
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
