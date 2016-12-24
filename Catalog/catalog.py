from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Team, PlayerItem, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#from flask.ext.github import GitHub

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hockey Team Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///teamwithplayer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all teams
@app.route('/')
@app.route('/catalog/')
def showTeams():
    teams = session.query(Team).order_by(asc(Team.name))
    if 'username' not in login_session:
        return render_template('publicteams.html', teams=teams)
    else:
        return render_template('teams.html', teams=teams)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Facebook oauth connect
@app.route('/fbconnect', methods=['GET', 'POST'])
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

    # The token must be stored in the login_session in order to
    # properly logout, let's strip out the information before the
    # equals sign in our token
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

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'

    flash("Now logged in as %s" % login_session['username'])
    return output


# Facebook oauth disconnect
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s'%(facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Google plus oauth connect
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
    login_session['email'] = data['email']
    #login_session['picture'] = data['picture']

    if getUserID(login_session['email']):
        login_session['user_id'] = getUserID(login_session['email'])

    else:
        login_session['user_id'] = createUser(login_session)

    print 'user id init'
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Google plus oauth disconnect
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            
        del login_session['provider']
        flash("You have been logged out.")
        return redirect(url_for('showTeams'))
    else:
        flash("You are not logged in")
        return redirect(url_for('showTeams'))


# JSON APIs to view Team Information
@app.route('/catalog/<int:team_id>/team/JSON')
def teamPlayerJSON(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    items = session.query(PlayerItem).filter_by(
        team_id=team_id).all()
    return jsonify(PlayerItems=[i.serialize for i in items])


@app.route('/catalog/<int:team_id>/players/<int:player_id>/JSON')
def playerJSON(team_id, player_id):
    Player_Item = session.query(PlayerItem).filter_by(id=player_id).one()
    return jsonify(Player_Item=Player_Item.serialize)


@app.route('/catalog/JSON')
def teamJSON():
    teams = session.query(Team).all()
    return jsonify(teams=[r.serialize for r in teams])


# Create a new team
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newTeam():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newTeam = Team(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newTeam)
        flash('New Team %s Successfully Created' % newTeam.name)
        session.commit()
        return redirect(url_for('showTeams'))
    else:
        return render_template('newTeam.html')


# Edit a team
@app.route('/catalog/<int:team_id>/edit/', methods=['GET', 'POST'])
def editTeam(team_id):
    editedTeam = session.query(
        Team).filter_by(id=team_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedTeam.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this team. Please create your own team in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedTeam.name = request.form['name']
            flash('Team Successfully Edited %s' % editedTeam.name)
            return redirect(url_for('showTeams'))
    else:
        return render_template('editTeam.html', team=editedTeam)


# Delete a team
@app.route('/catalog/<int:team_id>/delete/', methods=['GET', 'POST'])
def deleteTeam(team_id):
    teamToDelete = session.query(
        Team).filter_by(id=team_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if teamToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');} </script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(teamToDelete)
        flash('%s Successfully Deleted' % teamToDelete.name)
        session.commit()
        return redirect(url_for('showTeams', team_id=team_id))
    else:
        return render_template('deleteTeam.html', team=teamToDelete)


# Show team players 
@app.route('/catalog/<int:team_id>/')
@app.route('/catalog/<int:team_id>/players/')
def showPlayer(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    creator = getUserInfo(team.user_id)
    items = session.query(PlayerItem).filter_by(
            team_id=team_id).all()
    if 'username' not in login_session:
        return render_template('publicplayers.html', items=items,
                                    team=team, creator=creator)
    else:   
        return render_template('players.html', items=items,
                                team=team, creator=creator)


# Create a new player item
@app.route('/catalog/<int:team_id>/player/new/', methods=['GET', 'POST'])
def newPlayer(team_id):
    if 'username' not in login_session:
        return redirect('/login')
    team = session.query(Team).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add player to this team. Please create your own team in order to add players.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newPlayer = PlayerItem(name=request.form['name'],
                               description=request.form['description'],
                               number=request.form['number'],
                               position=request.form['position'],
                               team_id=team_id, user_id=team.user_id)
        session.add(newPlayer)
        session.commit()
        flash('Player %s Successfully Added' % (newPlayer.name))
        return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('newplayer.html', team_id=team_id)


# Edit a player
@app.route('/catalog/<int:team_id>/menu/<int:player_id>/edit',
           methods=['GET', 'POST'])
def editPlayer(team_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPlayer = session.query(PlayerItem).filter_by(id=player_id).one()
    team = session.query(Team).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit players to this team. Please create your own team in order to edit players.');} </script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedPlayer.name = request.form['name']
        if request.form['description']:
            editedPlayer.description = request.form['description']
        if request.form['number']:
            editedPlayer.price = request.form['number']
        if request.form['position']:
            editedPlayer.course = request.form['position']
        session.add(editedPlayer)
        session.commit()
        flash('Player Successfully Edited')
        return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('editplayer.html', team_id=team_id,
                               player_id=player_id, player=editedPlayer)


# Delete a player
@app.route('/catalog/<int:team_id>/menu/<int:player_id>/delete',
           methods=['GET', 'POST'])
def deletePlayer(team_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    team = session.query(Team).filter_by(id=team_id).one()
    playerToDelete = session.query(PlayerItem).filter_by(id=player_id).one()
    if login_session['user_id'] != team.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this restaurant. Please create your own restaurant in order to delete items.');} </script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        flash('Player Successfully Deleted')
        return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('deletePlayer.html', player=playerToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
