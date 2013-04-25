import cgi
import webapp2

from google.appengine.api import users


MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/guess" method="post">
        Guess: <input name="guess"><br>
        Name: <input name="name" value="Anonymous"><br>
        <input type="submit" value="Submit form">
    </form>
    <a href=%s>%s</a>
  </body>
</html>
"""

LOGGED_OUT_PAGE_HTML = """\
<html>
  <body>
    <a href=%s>%s</a>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            page = MAIN_PAGE_HTML
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            page = LOGGED_OUT_PAGE_HTML
        self.response.write(page % (url, url_linktext))


class Guessed(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>Thanks ')
        self.response.write(cgi.escape(self.request.get('name')))
        self.response.write(' you guessed: ')
        self.response.write(cgi.escape(self.request.get('guess')))
        self.response.write('<p><a href="/">Back</a> <p>')
        self.response.write('</body></html>')


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/guess', Guessed)],
                              debug=True)
