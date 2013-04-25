import cgi
import webapp2

from google.appengine.api import users


LOGGED_IN_PAGE_HTML = """\
<html>
  <body>
    <form action="/guess" method="post">
        Guess: <input name="guess"><br>
        Name: <input name="name" value="Anonymous"><br>
        <input type="submit" value="Submit form">
    </form>
    <a href=%s>Logout</a>
  </body>
</html>
"""

LOGGED_OUT_PAGE_HTML = """\
<html>
  <body>
    <form action="/guess" method="post">
        Guess: <input name="guess"><br>
        Name: <input name="name" value="Anonymous"><br>
        <input type="submit" value="Submit form">
    </form>
  </body>
</html>
"""

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/guess" method="post">
        Guess: <input name="guess"><br>
        Name: <input name="name" value="Anonymous"><br>
        <input type="submit" value="Submit form">
    </form>
  </body>
</html>
"""


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.response.write(LOGGED_IN_PAGE_HTML % users.create_logout_url(self.request.uri))

        else:
            self.response.write(LOGGED_OUT_PAGE_HTML)


class Guessed(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>Thanks ')
        self.response.write(cgi.escape(self.request.get('name')))
        self.response.write(' you guessed: ')
        self.response.write(cgi.escape(self.request.get('guess')))
        self.response.write('</body></html>')


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/guess', Guessed)],
                              debug=True)
