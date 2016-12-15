import os
import re
import random
import hashlib
import hmac
from string import letters
import webapp2
import jinja2
from google.appengine.ext import db

#Template directory for jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#Secret code for hashing value
secret = '53cr57'

#Hashing functions
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#Salt and password hashing for login
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

#User properties and function
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


#Main handler for the blog
class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    #Sets the cookie for distinct user
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    #Reads the cookie
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


#Signup section of the blog
class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        if self.request.get('action')=='Already have an account? Login here!':
            self.redirect('/login')
        elif self.request.get('action') == 'signup':
            self.username = self.request.get('username')
            self.password = self.request.get('password')
            self.verify = self.request.get('verify')
            self.email = self.request.get('email')

            params = dict(username = self.username,
                          email = self.email)

            if not valid_username(self.username):
                params['error_username'] = "That's not a valid username."
                have_error = True

            if not valid_password(self.password):
                params['error_password'] = "That wasn't a valid password."
                have_error = True
            elif self.password != self.verify:
                params['error_verify'] = "Your passwords didn't match."
                have_error = True

            if not valid_email(self.email):
                params['error_email'] = "That's not a valid email."
                have_error = True

            if have_error:
                self.render('signup-form.html', **params)
            else:
                self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


#Register section of the blog
class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')


#Login section that gets username and password
class Login(BlogHandler):
    def get(self):
        self.render('login-form.html', error=self.request.get('error'))

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)


#Logs users out and redirects to front page of blog
class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')
        

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)


#Blog's front page
class BlogFront(BlogHandler):
    def get(self):
        delete_id = self.request.get('delete_id')
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts=posts, delete_id=delete_id)
        

#Post section of the blog
class Post(db.Model):
    user_id = db.IntegerProperty(required=True)
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    likes = db.StringListProperty()

    def getUser(self):
        user = User.by_id(self.user_id)
        return user.name
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)


#Post page of the blog
class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        comments = db.GqlQuery("select * from Comment where post_id="+
                               post_id+ " order by created desc")

        like = db.GqlQuery("select * from LikePost where post_id="+post_id)
        
        if not post:
            self.error(404)
            return

        error = self.request.get('error')
        
        self.render("permalink.html", post=post, comments=comments,
                    numLikes=like.count(), error=error)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        c=""
        if(self.user):
            #Click to submit comment
            if(self.request.get('comment')):
                c = Comment(parent=blog_key(), user_id=self.user.key().id(),
                            post_id=int(post_id),
                            comment=self.request.get('comment'))
                c.put()
            if(self.request.get('like') and
               self.request.get('like') == "update"):
                like = db.GqlQuery("select * from LikePost where post_id="+
                                   post_id+"and user_id="+
                                   str(self.user.key().id()))
                if self.user.key().id() == post.user_id:
                    self.redirect("/"+post_id+
                                  "?error=You cannot like your own post.")
                    return
                elif like.count() == 0:
                    l = LikePost(parent=blog_key(),
                                 user_id=self.user.key().id(),
                                 post_id=int(post_id))
                    l.put()
        else:
            self.redirect("/login?error=You need to login before " +
                          "performing edit, like or commenting.")
            return

        comments = db.GqlQuery("select * from Comment where post_id=" +
                               post_id + "order by created desc")

        like = db.GqlQuery("select * from LikePost where post_id="+post_id)
        
        self.render("permalink.html", post=post,
                    comments=comments, numLikes=like.count(), new=c)


#Handles new post for blog
class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), user_id=self.user.key().id(),
                     subject=subject, content=content)
            p.put()
            self.redirect('/%s' % str(p.key().id()))
        else:
            error = "Subject and Content, please!"
            self.render("newpost.html", subject=subject,
                        content=content, error=error)


#Deletes the post
class DeletePost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.user_id == self.user.key().id():
                post.delete()
                self.redirect("/?delete_id="+post_id)
            else:
                self.redirect("/"+post_id+"?error=You can't delete"+
                              " this post. You didn't create it.")
        else:
            self.redirect("/"+post_id+"?error=You need to be logged in"+
                          " to delete posts.")


#Edits a post
class EditPost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.user_id == self.user.key().id():
                self.render("newpost.html", subject=post.subject,
                            content=post.content)
            else:
                self.redirect("/"+post_id+"?error=You can't edit " +
                              "this post. You didn't create it.")
        else:
            self.redirect("/"+post_id+"?error=You need to be logged in"+
                          "to edit posts.")
    def post(self, post_id):
        if not self.user:
            self.redirect('/')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/%s' % post_id)
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject,
                        content=content, error=error)


#Comment properties
class Comment(db.Model):
    user_id = db.IntegerProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    
    def getUser(self):
        user = User.by_id(self.user_id)
        return user.name


#Delete comments
class DeleteComment(BlogHandler):
    def get(self, post_id, comment_id):
        if self.user:
            key=db.Key.from_path('Comment', int(comment_id),
                                 parent=blog_key())
            comments=db.get(key)
            if comments.user_id == self.user.key().id():
                comments.delete()
                self.redirect("/"+post_id+"?deleted_comment_id="+
                              comment_id)
            else:
                self.redirect("/"+post_id+"?error=You can't delete "+
                              "this comment. You didn't create it.")
        else:
            self.redirect("/login?error=You need to be logged in"+
                          "to delete this comment.") 


#Edit comments
class EditComment(BlogHandler):
    def get(self, post_id, comment_id):
        if self.user:
            key=db.Key.from_path('Comment', int(comment_id),
                                 parent=blog_key())
            comments=db.get(key)
            if comments.user_id == self.user.key().id():
                self.render("editcomment.html", comment=comments.comment)
            else:
                self.redirect("/"+post_id+"?error=You can't edit "+
                              "this comment. You didn't create it.")
        else:
            self.redirect("/login?error=You need to be logged in"+
                          "to delete this comment.")

    def post(self, post_id, comment_id):
        if not self.user:
            self.redirect('/')

        c=self.request.get('comment')

        if c:
            key=db.Key.from_path('Comment', int(comment_id),
                                 parent=blog_key())
            comments=db.get(key)
            comments.comment = c
            comments.put()
            self.redirect('/%s' % post_id)
        else:
            error="Subject and Content, please!"
            self.render("editpost.html", subject=subject,
                        content=content, error=error)


class LikePost(db.Model):
    user_id = db.IntegerProperty(required=True)
    post_id = db.IntegerProperty(required=True)
            

app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/signup', Register),
                               ('/([0-9]+)', PostPage),
                               ('/newpost', NewPost),
                               ('/deletepost/([0-9]+)', DeletePost),
                               ('/editpost/([0-9]+)', EditPost),
                               ('/deletecomment/([0-9]+)/([0-9]+)',
                                DeleteComment),
                               ('/editcomment/([0-9]+)/([0-9]+)',
                                EditComment),
                               ('/login', Login),
                               ('/logout', Logout),
                               ],
                               debug=True)
