from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import time
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



#Display all categories and 5 latest items
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(5).all()

    return render_template('showCatalog.html', items=items, categories=categories)


#Check login status and duplication before new category creation

@app.route('/catalog/new_category/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        newCategory_name = request.form['name']
        duplicated_category = session.query(
            Category).filter_by(name=newCategory_name).first()
        if duplicated_category:
            return render_template('newCategory.html', error='Category %s lready exists' % duplicated_category.name)
        newCategory = Category(name=newCategory_name,
                               user_id=login_session['username'])
        session.add(newCategory)
        session.commit()
        flash("new category created")
        return redirect(url_for('showCatalog'))

    else:

        return render_template('newCategory.html')
# checking for duplication with existing category before renaming 
# Thenedit category 's name and loop through all items under edited category to 
# update item.category_name.  


@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    category = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        editedCategory_name = request.form['name']
        duplicated_category = session.query(Category).filter_by(
            name=editedCategory_name).first()
        if duplicated_category:
            return render_template('editCategory.html', error='Category %s lready exists' % duplicated_category.name, category=category)

        edited_name = request.form['name']
        category.name = edited_name
        session.add(category)
        session.commit()

        items_in_category = session.query(
            Item).filter_by(category_id=category_id).all()
        for item in items_in_category:
            item.category_name = edited_name
            session.add(item)

        session.commit()

        flash("category name edited")
        return redirect(url_for('showCatalog'))

    else:
        return render_template('editCategory.html', category=category)

#delete category and all items under deleted category 
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    category = session.query(Category).filter_by(id=category_id).one()
    items_in_category = session.query(
        Item).filter_by(category_id=category_id).all()
    if request.method == 'POST':

        session.delete(category)
        for item in items_in_category:
            session.delete(item)

        session.commit()
        flash("category deleted")
        return redirect(url_for('showCatalog'))

    return render_template('deleteCategory.html', category=category)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showCategory(category_id):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id).all()

    return render_template('showCategory.html', items=items, categories=categories, category_id=category_id)


@app.route('/catalog/<int:category_id>/new_item/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newitem = Item(name=request.form['name'], description=request.form[
                       'description'], category_id=category_id, category_name=category.name, user_id=login_session['username'])
        session.add(newitem)
        session.commit()
        flash("new item created")
        return redirect(url_for('showCategory', category_id=category_id))

    else:

        return render_template('newItem.html', category=category)


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()

    return render_template('showItem.html', item=item)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        edited_category = session.query(Category).filter_by(
            name=request.form['category']).one()
        item.category_id = edited_category.id
        item.category_name = edited_category.name
        session.add(item)
        session.commit()
        flash("item edited")
        return redirect(url_for('showCategory', category_id=category_id))
    else:

        return render_template('editItem.html', item=item, categories=categories, category_name=category.name)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':

        session.delete(item)
        session.commit()
        flash("item delted")
        return redirect(url_for('showCategory', category_id=category_id))
    else:

        return render_template('deleteItem.html', item=item, category_name=category.name)


@app.route('/search/')
def search():
    q = request.args.get('query')
    search_results = session.query(Item).filter_by(name=q).all()
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(5).all()

    return render_template('showCatalog.html', items=items, categories=categories, search_results=search_results)


@app.route('/catalog/JSON/')
def showCatalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/catalog/<int:category_id>/JSON')
def showCategoryJSON(category_id):

    items = session.query(Item).filter_by(category_id=category_id).all()
    category_name = items[0].category_name
    return jsonify(items=[item.serialize for item in items])


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def showItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    return jsonify(item=[item.serialize])


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code

    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    # if stored_credentials is not None and gplus_id == stored_gplus_id:
    #    response = make_response(json.dumps('Current user is already connected.'),
    #                             200)
    #    response.headers['Content-Type'] = 'application/json'
    #    return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    if getUserID(login_session['email']):
        login_session['user_id'] = getUserID(login_session['email'])

    else:
        login_session['user_id'] = createUser(login_session)

    print 'user id init'
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in our
    # token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/callback')
def callback():
    return render_template('callback.html', STATE=login_session['state'])


@app.route('/gitconnect', methods=['POST'])
def gitconnect():
    print "gitconnect "
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    print "code  received %s " % code
    client_id = json.loads(open('github_client_secrets.json', 'r').read())[
        'web']['app_id']
    client_secret = json.loads(open('github_client_secrets.json', 'r').read())[
        'web']['app_secret']
    url = 'https://github.com/login/oauth/access_token?client_id=%s&client_secret=%s&code=%s&state=%s' % (
        client_id, client_secret, code, login_session['state'])
    h = httplib2.Http()
    result = h.request(url, 'POST')[1]

    if 'error' in result:
        response = make_response(json.dumps(result), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    result = result.split("=")[1]

    access_token = result.split("&")[0]
    print access_token

    userinfo_url = "https://api.github.com/user?access_token=%s" % access_token
    print 'userinfo_url'
    print userinfo_url

    h = httplib2.Http()
    result = h.request(userinfo_url, 'GET')[1]

    data = json.loads(result)
    login_session['access_token'] = access_token
    login_session['provider'] = 'github'
    login_session['username'] = data["name"]
    login_session['github_id'] = data["id"]
    login_session['picture'] = data["avatar_url"]

    email_url = "https://api.github.com/user/emails?access_token=%s" % access_token

    h = httplib2.Http()
    result = h.request(email_url, 'GET')[1]

    result = result[1:-1]
    data = json.loads(result)

    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print "user_id"
    print user_id

    flash("Now logged in as %s" % login_session['username'])

    return render_template('gitredirect.html', username=login_session['username'], picture=login_session['picture'])


@app.route('/gitdisconnect')
def gitdisconnect():
    if 'access_token' in login_session:
        del login_session['access_token']


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()

        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        if login_session['provider'] == 'github':
            gitdisconnect()
            del login_session['github_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':

    app.secret_key = 'super_secret_key'

    app.debug = True

    app.run(host='0.0.0.0', port=5000)
