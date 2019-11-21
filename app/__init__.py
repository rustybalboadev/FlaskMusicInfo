from flask import Flask, request, render_template, redirect, url_for, session, make_response
import pylast
app = Flask(__name__)
API_KEY = '' #LAST FM API KEY
API_SECRET = '' #LAST FM API SECRET
username = '' #LAST FM USERNAME
password_hash = pylast.md5('!') #LAST FM PASSWORD
network = pylast.LastFMNetwork(api_key=API_KEY,api_secret=API_SECRET,username=username,password_hash=password_hash)
user = network.get_user(username)
def playing_now():
    global user
    now_playing = user.get_now_playing()
    return now_playing
def song_played_amount():
    global user
    songs_played = user.get_playcount()
    return songs_played
def your_name():
    global user
    name = user.get_name(properly_capitalized=True)
    return name
def sub():
    global user
    sub_check = user.is_subscriber()
    return sub_check
def recent_played():
    global user
    recent_track = user.get_recent_tracks(limit=2)
    return(recent_track[0][0])
def top_albums():
    global user
    top_album = user.get_top_albums(limit=2)
    return(top_album[0][0])
def top_tracks():
    global user
    top_track = user.get_top_tracks(limit=2)
    return(top_track[0][0])
@app.route('/')
def root():
    resp = make_response(redirect('/login'))
    resp.set_cookie('admin','False')
    return resp
@app.route("/login", methods=['GET','POST'])
def login_page():
    error = None
    if request.method == 'POST':
        if request.form['username'.lower()] == 'admin' or request.form['password'.lower()] == 'admin':
            resp = make_response(redirect('/home'))
            resp.set_cookie('admin','True')
            return resp
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html',error=error)
@app.route('/home', methods=['GET','POST'])
def home():
    adminCheck = request.cookies.get('admin')
    if adminCheck == False:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('admin','False')
        return resp
    else:
        return render_template('index.html',your_username=your_name(),is_sub=sub(),now_playing=playing_now(),recent_play=recent_played(),top_album=top_albums(),top_track=top_tracks(),play_counts=song_played_amount())
    
