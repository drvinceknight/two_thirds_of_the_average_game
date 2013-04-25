import webapp2
import jinja2
import os

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
                                        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, webapp2 World!')
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            html_file = 'index.html'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            html_file = 'login.html'

        template_values = {
            'url': url,
            'url_linktext': url_linktext
        }

        template = JINJA_ENVIRONMENT.get_template(html_file)
        self.response.write(template.render(template_values))


class GuessedPage(webapp2.RequestHandler):

    def post(self):
        self.response("<html><body>Thanks for guessing</body></html>")


app = webapp2.WSGIApplication([('/', MainPage), ('/guessed', GuessedPage)],
                              debug=True)
