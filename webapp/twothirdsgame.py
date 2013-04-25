import cgi
import webapp2

from google.appengine.api import users
from google.appengine.ext import db


MAIN_PAGE_HTML = """\
<html>
  <body>
    <h1>Two thirds of the average game</h1>

    <p>Welcome to this online version of the two thirds of the average game.</p>
    <p>Here are the rules of the game as given on the <a href="http://en.wikipedia.org/wiki/Guess_2/3_of_the_average">wikipedia page</a>: <blockquote>"In game theory, Guess 2/3 of the average is a game where several people guess what 2/3 of the average of their guesses will be, and where the numbers are restricted to the real numbers between 0 and 100, inclusive. The winner is the one closest to the 2/3 average."</blockquote></p>

    <p>I use this game quite a lot in my teaching and during outreach events. I've blogged about it <a href="http://drvinceknight.blogspot.co.uk/2013/04/two-thirds-of-average-game.html">here</a>.</p>

    <p>It's a game to get participants to understand concepts of dominated strategies:</p>

    <img src="/images/Rationalise_two_thirds_of_average_game.gif" width=500>
"""

LOGGED_IN_PAGE_HTML = """\
    <p><b>If you are on this page it is because you are currently logged in via your google user name. I am using this to ensure that every one who chooses to participate will have their last guess only counted (there is an option to logout below).</b></p>

    <p> Please enter a guess below. If you enter a url (G+ page, twitter page, website...) I'll be sure to include it when I disclose the winner(s) on my <a href="http://drvinceknight.blogspot.co.uk/">blog page</a> :)</p>

    <form action="/guess" method="post">
        Guess: <input name="guess"><br>
        Name: <input name="name" value="Anonymous"><br>
        url: <input name="personel_url"><br>
        <input type="submit" value="Submit form">
    </form>
    <a href=%s>%s</a>

  </body>
</html>
"""

LOGGED_OUT_PAGE_HTML = """\
    <p><b>If you are on this page it is because you are currently not logged in. To ensure that the game is played fairly and no one has anymore information than any other player, please log in using your google account.</b></p>
    <a href=%s>%s</a>
  </body>
</html>
"""


class Guess(db.Model):
    """Models a guess"""
    author = db.StringProperty()
    name = db.StringProperty()
    number = db.StringProperty()
    personel_url = db.StringProperty()
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
        page = MAIN_PAGE_HTML

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            page += LOGGED_IN_PAGE_HTML
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            page += LOGGED_OUT_PAGE_HTML
        self.response.write(page % (url, url_linktext))


class Guessed(webapp2.RequestHandler):

    def post(self):

        name = self.request.get('name')
        number = self.request.get('guess')
        personel_url = self.request.get('personel_url')

        if is_valid_guess(number):

            guess = Guess(parent=guess_key(name))
            guess.author = users.get_current_user().nickname()
            guess.name = name
            guess.number = number
            guess.personel_url = personel_url
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
