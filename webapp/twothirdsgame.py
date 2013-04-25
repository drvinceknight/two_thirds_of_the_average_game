import cgi
import webapp2

from google.appengine.api import users
from google.appengine.ext import db


MAIN_PAGE_HTML = """\
<html>
  <body>
    <h1>Two thirds of the average game</h1>

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


class Guess(db.Model):
    """Models a guess"""
    author = db.StringProperty()
    name = db.StringProperty()
    number = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)


def guess_key(name=None):
    """Constructs a datastore key for a Guess entity with name"""
    return db.Key.from_path('Guessed', name or 'Anonymous')


def is_valid_guess(number):
    """Function to test if we have a valid guess (float between 0 and 100)"""
    try:
        float(number)
        if eval(number) <= 100 and eval(number) >= 0:
            return True
    except ValueError:
        return False


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

        name = self.request.get('name')
        number = self.request.get('guess')

        if is_valid_guess(number):

            guess = Guess(parent=guess_key(name))
            guess.author = users.get_current_user().nickname()
            guess.name = name
            guess.number = number
            guess.put()

            Q = Guess.all()
            Q.filter("author =", guess.author)
            Q.order("date")

            self.response.write('<html><body>Thanks ')
            self.response.write(cgi.escape(self.request.get('name')))
            self.response.write('.')

            Q = [q for q in Q]
            num_prev_guesses = len(Q)

            if num_prev_guesses > 0:
                self.response.write(' This is your guess number: %s. Your previous guess was %s.' % (num_prev_guesses + 1, Q[-1].number))

            self.response.write(' You guessed ')
            self.response.write(cgi.escape(self.request.get('guess')))

            if num_prev_guesses > 0:
                self.response.write(' this time')
            self.response.write(' and this has been added to the database and will be used to evaluate the winning strategy.')
            self.response.write('<p><a href="/">Back</a> <p>')
            self.response.write('</body></html>')

        else:
            self.response.write("I'm sorry ")
            self.response.write(cgi.escape(self.request.get('name')))
            self.response.write("but you guessed '%s' which is not a valid guess (Reel number between 0 and 100).")
            self.response.write('<p><a href="/">Back</a> <p>')
            self.response.write('</body></html>')


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/guess', Guessed)],
                              debug=True)
