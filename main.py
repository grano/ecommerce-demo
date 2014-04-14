import webapp2
import jinja2
import urllib
import urllib2
import os
import uuid

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

GA_WEBPROPERTY = 'UA-25868527-5'

def sendMeasurementProtocolHit(params):
	url = 'http://www.google-analytics.com/collect'
	values = params
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)

def makeTrans():
	return True

class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class HomePage(MainHandler):
	def get(self):
		self.render('home.html')

class ProcessTransactions(MainHandler):
	def post(self):
		transactionSuccessful = makeTrans()
		if(transactionSuccessful):
			clientId = self.request.get('clientId')
			if(clientId == ''):
				clientId = str(uuid.uuid4())
				cd4 = 'server side'
			else:
				cd4 = 'analytics.js'
			ip = self.request.remote_addr
			userAgent = str(self.request.headers['User-Agent'])
			params = dict(v = '1', 
						  tid = GA_WEBPROPERTY,
						  cid = clientId,
						  uip = ip,
						  ua = userAgent,
						  dp = '/transaction-successful',
						  cd4 = cd4			  
						  )
			sendMeasurementProtocolHit(params)

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/purchase', ProcessTransactions)
], debug=True)
