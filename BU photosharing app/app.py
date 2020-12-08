######################################
# author ben lawson <balawson@bu.edu> 
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from 
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
#import flask.ext.login as flask_login
import flask_login
from flask_login import current_user
#for image uploading
from werkzeug import secure_filename
import os, base64
from bs4 import BeautifulSoup
import re, urllib, urllib2
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password' #CHANGE THIS TO YOUR MYSQL PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users") 
users = cursor.fetchall()


def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users") 
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user



@app.route('/home/<int:photo_id>/', methods=['POST'])
def viewComment(photo_id):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Albums A, Photos P, Users U, NumLikes L, NumComments N  WHERE A.owner_id = U.user_id  AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND AND L.photo_id= N.photo_id AND L.photo_id='{0}'".format(photo_id))
    userphotos=cursor.fetchall()
    cursor.execute("SELECT U.email, U.profile_pic, C.text, C.dates FROM Users U,Comment C WHERE C.owner_id=U.user_id AND C.photo_id='{0}'".format(photo_id))
    comments=cursor.fetchall()
    return render_template('home.html', photos=userphotos, comments=comments)



@app.route('/profile/home/<int:photo_id>/', methods=['POST','GET'])
@flask_login.login_required
def viewProfileComment(photo_id):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments  FROM Albums A, Photos P, Users U, NumLikes L, NumComments N  WHERE A.owner_id = U.user_id  AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=N.photo_id AND L.photo_id='{0}'".format(photo_id))
    userphotos=cursor.fetchall()

    cursor.execute(query1.format(args))
    results=cursor.fetchall()
    photo_array=[]
    for pic in results:
        photo_array.append(str(pic[0]))


    query2="SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Albums A, Photos P, Users U, NumLikes L, NumComments N, Tag_Photo T  WHERE A.owner_id = U.user_id  AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id= N.photo_id AND N.photo_id=T.photo_id AND T.photo_id='{0}' "
    for j in range(1,len(photo_array)):
        query2 += "AND T.word='{{{0}}}' ".format(j)

    args2 = ""
    for values in photo_array:
        args2 += str(values) + ","
        
    cursor.execute(query2.format(args))
    search = cursor.fetchall()

    return render_template("profile.html", search=search, albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id) )


    
def userRecommentdations(user_id):
    top_tags = getTopFive(user_id)
    
    all_tags=alltags()
    mydict = dict()
    for values in all_tags:
        if values[0] ==top[0]:
            if values[0] in mydict.keys():
                mydict[values[0]]+=1
            else:
                mydict[values[0]]=0
            
        if values[0]==top[1]:
            if values[0] in mydict.keys():
                mydict[values[0]]+=1
            else:
                mydict[values[0]]=0
        if values[0]==top[2]:
           if values[0] in mydict.keys():
               mydict[values[0]]+=1
           else:
               mydict[values[0]]=0
        if values[0]==top[3]:
           if values[0] in mydict.keys():
               mydict[values[0]]+=1
           else:
               mydict[values[0]]=0

        if values[0]==top[4]:
            if values[0] in mydict.keys():
                mydict[values[0]]+=1
            else:
                mydict[values[0]]=0
    refined = sorted(mydict.items(), reverse=True, key=operator.itemgetter(1))
   
    return 0
#create list of photos and 
        

@app.route('/home/<int:photo_id>/', methods=['POST','GET'])
def viewComment(photo_id):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments  FROM Albums A, Photos P, Users U, NumLikes L, NumComments N  WHERE A.owner_id = U.user_id  AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=N.photo_id AND L.photo_id='{0}'".format(photo_id))
    userphotos=cursor.fetchall()
    cursor.execute("SELECT U.email, U.profile_pic, C.text, C.dates FROM Users U,Comment C WHERE C.owner_id=U.user_id AND C.photo_id='{0}'".format(photo_id))
    comments=cursor.fetchall()
    return render_template('profile.html', photos=userphotos, comments=comments, toptags=toptags())



@app.route('/profile/home/<int:photo_id>/', methods=['POST','GET'])
@flask_login.login_required
def viewProfileComment(photo_id):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments  FROM Albums A, Photos P, Users U, NumLikes L, NumComments N  WHERE A.owner_id = U.user_id  AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=N.photo_id AND L.photo_id='{0}'".format(photo_id))
    userphotos=cursor.fetchall()
    cursor.execute("SELECT U.email, U.profile_pic, C.text, C.dates FROM Users U,Comment C WHERE C.owner_id=U.user_id AND C.photo_id='{0}'".format(photo_id))
    comments=cursor.fetchall()
    return render_template('profile.html', album_photos=userphotos, comments=comments)



@app.route('/profile/home/<int:photo_id>/delete', methods=['POST','GET'])
@flask_login.login_required
def deletePhoto(photo_id):
    email=flask_login.current_user.get_id()
    user_id=getUserIdFromEmail(email)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Photos WHERE photo_id='{0}'".format(photo_id))
    conn.commit()
    return render_template("profile.html",  albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id) )

    

@app.route('/profile/home/<int:photo_id>/likes', methods=['GET','POST'])
@flask_login.login_required
def addLike(photo_id):
    cursor = conn.cursor()
    email=flask_login.current_user.get_id()
    user_id=getUserIdFromEmail(email)
    try:
        cursor.execute("INSERT INTO Likes(user_id, photo_id) VALUES ('{0}','{1}')".format(user_id, photo_id))
        conn.commit()
        cursor.execute("UPDATE NumLikes SET numLikes= numLikes + '1' WHERE photo_id='{0}'".format(photo_id))
        conn.commit()
        cursor.execute("UPDATE Users SET contribution = contribution + '1' WHERE user_id='{0}'".format(user_id))
        conn.commit()
        return render_template('profile_home.html', photos=getAllPhotosNotUsers(user_id))
    except:
        return render_template('profile_home.html', photos=getAllPhotosNotUsers(user_id))

def getLikes():
    cursor=conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, L.photo_id, U.profile_pic, P.caption from Users U, Likes L, Photos P where U.user_id=L.user_id AND L.photo_id=P.photo_id  ")
    return cursor.fetchall()

@app.route('/home/', methods=['GET', 'POST'])
def addComment():
    if flask.request.method=='GET':
        return render_template('home.html', photos=getAllPhotos(), toptags=toptags())
    else:
        try:
            comment = request.form['comment']
            photo_id= request.form['comment_photo_id'] 
            email=flask_login.current_user.get_id()
            user_id=getUserIdFromEmail(email)
            cursor= conn.cursor()
            cursor.execute("SELECT A.owner_id FROM Albums A, Photos P WHERE A.album_id=P.album_id AND P.photo_id='{0}'".format(photo_id))
            if user_id not in cursor.fetchall()[0]:
                cursor.execute("INSERT INTO Comment (text,photo_id,owner_id) VALUES ('{0}','{1}','{2}')".format(comment,photo_id,user_id))
                cursor.execute("UPDATE NumComments SET numComments= numComments + '1' where photo_id='{0}'".format(photo_id))
                conn.commit()
                return render_template("home.html",photos=getAllPhotos(), toptags=toptags())
            else:
                return render_template("home.html", photos=getAllPhotos(), toptags=toptags())
        except:
            comment = request.form['comment']
            photo_id= request.form['comment_photo_id']
            user_id='1'
            cursor= conn.cursor()
            cursor.execute("INSERT INTO Comment (text,photo_id,owner_id) VALUES ('{0}','{1}','{2}')".format(comment,photo_id,user_id))
            cursor.execute("UPDATE NumComments SET numComments= numComments + '1' where photo_id='{0}'".format(photo_id))
            conn.commit()
            return render_template("home.html",photos=getAllPhotos(), toptags=toptags())


def getAllPhotos():
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Albums A, Photos P, Users U, NumLikes L, NumComments N WHERE A.owner_id = U.user_id AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=N.photo_id")
    return cursor.fetchall() 



@app.route('/login/', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='/login/' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
		   <a href='/'>Home</a>
			   '''
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchone()
		pwd = str(data[0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
                        
                        user_id = getUserIdFromEmail(email)
                        return render_template("profile.html", photos=getUsersPhotos(user_id), albums=getUsersAlbums, toptags=toptags(), alltags=alltags() )
#protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out') 

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html') 

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register/", methods=['GET'])
def register():
	return render_template('improved_register.html', supress='True')  

@app.route("/register/", methods=['POST'])
def register_user():
	try:
		email=request.form.get('email')
                password=request.form.get('password')
                firstname=request.form.get('firstname')
                lastname=request.form.get('lastname')
                birthday=request.form.get('birthday')
	except:
		return flask.redirect(flask.url_for('register'))
	bio=request.form.get('bio')
        hometown=request.form.get('hometown')
        gender=request.form.get('gender')
        cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
                try:
                    imgfile=request.file['photo']
                    photo_data = base64.standard_b64encode(imgfile.read())
                    cursor.execute("INSERT INTO Users (email, password,first_name,last_name, birthday, profile_pic, bio,hometown,gender) VALUES ('{0}', '{1}', '{2}','{3}', '{4}', '{5}', '{6}','{7}', '{8}')".format(email, password,firstname,lastname,birthday,photo_data, bio, hometown, gender))
                    conn.commit()
                    #log user in
                    user = User()
                    user.id = email
                    flask_login.login_user(user)
                    return render_template('profile.html', profile_pic = getprofilepic(), toptags=toptags(), mytags=mytags() )
                except: 
                    imgfile = default_photo()
                    photo_data = base64.standard_b64encode(imgfile)
                    cursor.execute("INSERT INTO Users (email, password,first_name,last_name, birthday, profile_pic, bio,hometown,gender) VALUES ('{0}', '{1}', '{2}','{3}', '{4}', '{5}', '{6}','{7}', '{8}')".format(email, password,firstname,lastname,birthday,photo_data, bio, hometown, gender))
                    conn.commit()
                    #log user in
                    user = User()
                    user.id = email
                    flask_login.login_user(user)
                    return render_template('profile.html', profile_pic = getprofilepic(), toptags=toptags(), mytags=mytags() )

	else:
		return flask.redirect(flask.url_for('register'))

def default_photo():
    with open("/home/kali/Downloads/default.png", "rb") as f:
        return f.read()


def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Users U, Albums A, Photos P, NumLikes L, NumComments N WHERE U.user_id=A.owner_id AND A.owner_id = '{0}' AND A.album_id=P.album_id AND L.photo_id=N.photo_id AND L.photo_id=P.photo_id".format(uid))
	return cursor.fetchall() #NOTE list of tuples, [(imgdata, pid), ...]

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)): 
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
#end login code


def getUsersAlbumsPhotos(uid):
    albumtree= list()
    cursor = conn.cursor()
    cursor.execute("SELECT A.name, A.album_id from Users U, Albums A where A.owner_id = U.user_id and U.user_id='{0}'".format(uid))
    lists = cursor.fetchall()
    for album in lists:
        photos= getPhotosFromAlbum(album[0], uid)
        albumtree.append(photos)
    return albumtree

def getPhotosFromAlbum(album_name, user_id):
    album_id = getAlbumId(album_name, user_id)
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Users U, Albums A, Photos P, NumLikes L, NumComments N WHERE U.user_id=A.owner_id AND A.album_id = '{0}' AND A.album_id=P.album_id AND L.photo_id=N.photo_id AND L.photo_id=P.photo_id".format(album_id))
    return cursor.fetchall() 


def getUsersAlbums(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT A.name, A.album_id from Users U, Albums A where A.owner_id = U.user_id and U.user_id='{0}'".format(uid))
    return cursor.fetchall()

@flask_login.login_required
@app.route("/profile/home/createalbum/", methods=['GET','POST'])
def create_album():
    email = flask_login.current_user.get_id()
    user_id = getUserIdFromEmail(email)
    album = request.form.get('newalbum')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Albums(owner_id,name) VALUES ('{0}','{1}')".format(user_id, album))
    conn.commit()
                        

    return render_template('profile.html', profile_pic=getprofilepic(), albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id))


def getAlbumId(album,uid):
    cursor = conn.cursor()
    cursor.execute("SELECT A.album_id FROM Albums A WHERE A.owner_id='{0}' AND A.name = '{1}'".format(uid,album))
    return cursor.fetchone()[0]

def getAllPhotosNotUsers(uid):
    cursor= conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Albums A, Photos P, Users U, NumLikes L, NumComments N where U.user_id=A.owner_id AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=N.photo_id AND A.owner_id NOT in ( SELECT A2.owner_id FROM Albums A2, Photos P2 WHERE A2.album_id=P2.album_id AND A2.owner_id='{0}')".format(uid));
    return cursor.fetchall()




@flask_login.login_required
@app.route('/profile/<int:album_id>/delete',methods =['GET','POST'])
def delete_album(album_id):
    email = flask_login.current_user.get_id()
    user_id = getUserIdFromEmail(email)
    cursor=conn.cursor()
    cursor.execute("DELETE FROM Albums Where album_id='{0}'".format(album_id))
    conn.commit()
    return render_template('profile.html', profile_pic=getprofilepic(), albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id))

    
@flask_login.login_required
@app.route('/profile/<int:album_id>/photos', methods=['GET','POST'])
def showAlbum(album_id):
    email = flask_login.current_user.get_id()
    user_id = getUserIdFromEmail(email)
    return render_template("profile.html", profile_pic=getprofilepic(), album_photos= getPhotos(album_id), photos=False, albums=False, toptags=toptags(), mytags=mytags(user_id) ) 


def getPhotos(album_id):
    cursor=conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes, N.numComments FROM Albums A, Photos P, Users U, NumLikes L, NumComments N where U.user_id=A.owner_id AND A.album_id='{0}' AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=N.photo_id".format(album_id))
    return cursor.fetchall()

@app.route('/profile/<int:photo_id>/editcaption', methods=['GET','POST'])
@flask_login.login_required
def editcaptionhelper(photo_id):
    user_id = getUserIdFromEmail(flask_login.current_user.id)
    return render_template('profile.html', profile_pic=getprofilepic(), albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id), edit_caption=photo_id)

@app.route('/profile/editcaption',methods=['GET','POST'])
@flask_login.login_required
def editCaption():
    user_id = getUserIdFromEmail(flask_login.current_user.id)
    photo_id= request.form.get('photo_id')
    caption = request.form.get('caption')
    cursor = conn.cursor()
    cursor.execute("UPDATE Photos SET caption='{0}' WHERE photo_id='{1}'".format(caption, photo_id))
    conn.commit()
    return render_template("profile.html", albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id) ) 


    

@app.route('/profile/home/<int:user_id>/addfriend/', methods=['GET','POST'])
@flask_login.login_required
def addfriend(user_id):
    cursor = conn.cursor()
    email=flask_login.current_user.get_id()
    uid=getUserIdFromEmail(email)
    try:
        cursor.execute("INSERT INTO Friends(user_id, friend_id) VALUES ('{0}','{1}')".format(uid, user_id))
        conn.commit()
        return render_template('profile.html', profile_pic=getprofilepic(), albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id))
    except:
        return render_template('profile.html', profile_pic=getprofilepic(), albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id))



@app.route('/profile/home/<int:user_id>/removefriend/', methods=['GET','POST'])
@flask_login.login_required
def removefriend(user_id):
    cursor = conn.cursor()
    email=flask_login.current_user.get_id()
    uid=getUserIdFromEmail(email)
    try:
        cursor.execute("DELETE FROM Friends where user_id='{0}'AND friend_id='{1}'".format(uid, user_id))
        conn.commit()
        return render_template('profile_home.html', alltags=alltags(), photos=getAllPhotosNotUsers(uid))
    except:
        return render_template('profile_home.html', alltags-alltags(), photos=getAllPhotosNotUsers(uid))


@app.route('/profile/friends/')
@flask_login.login_required
def friends_page():
    email = flask_login.current_user.get_id()
    uid=getUserIdFromEmail(email)
    user_friends=listUserFriends(uid)
    notfriends=listAllUsersNotFriends(uid)
    return render_template("friends.html",user_friends = user_friends, followers= listFollowers(uid), notfriends=notfriends, top_users= topusers(), photos=getUsersPhotos(uid), toptags=toptags(), alltags=alltags())


def listFollowers(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.contribution, U.bio, U.profile_pic, U.first_name, U.last_name FROM Users U, Friends F Where U.user_id=F.user_id AND F.friend_id='{0}'".format(uid))
    return cursor.fetchall()

def listUserFriends(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.contribution, U.bio, U.profile_pic, U.first_name, U.last_name FROM Users U, Friends F Where U.user_id=F.friend_id AND F.user_id='{0}'".format(uid))
    return cursor.fetchall()

def listAllUsersNotFriends(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.contribution, U.bio, U.profile_pic, U.first_name, U.last_name from Users U where U.user_id<>'1' AND U.user_id<>'{0}' AND U.user_id NOT IN (SELECT F.friend_id from Friends F where F.user_id='{1}')".format(uid, uid))  
    return cursor.fetchall()
    

def topusers():
    cursor = conn.cursor()
    cursor.execute("Select U.email, U.user_id, U.contribution, U.bio, U.profile_pic, U.first_name, U.last_name FROM Users U WHERE U.user_id <> 1 ORDER BY U.contribution DESC LIMIT 10")
    return cursor.fetchall()

    

@app.route('/profile/')
@flask_login.login_required
def profile():
    email=flask_login.current_user.get_id()
    user_id=getUserIdFromEmail(email)
    
    return render_template("profile.html", profile_pic=getprofilepic(), albums=getUsersAlbums(user_id), photos=getUsersPhotos(user_id), toptags=toptags(), mytags=mytags(user_id) )


@app.route('/profile/home/addtag/', methods=['GET', 'POST'])
@flask_login.login_required
def addTag():
    user_id = getUserIdFromEmail(flask_login.current_user.id)
    if request.method=='POST':
        tagstring = request.form.get('tag')
        photo_id = request.form.get('photo_id')
        tags= [x for x in re.split("\s|(?<!\d)[,.](?!\d)",tagstring)]
        for tag in tags:
            try:
                cursor= conn.cursor()
                cursor.execute("INSERT INTO Tag_Photo(word, photo_id) VALUES ('{0}', '{1}')".format(tag,photo_id))
                conn.commit()
            except:
                continue

    return render_template("profile.html", photos=getUsersPhotos(user_id),profile_pic=getprofilepic(), toptags=toptags(), mytags=mytags(user_id), albums=getUsersAlbums(user_id))

@app.route('/profile/home/<int:photo_id>/addtag/', methods=['GET','POST'])
@flask_login.login_required
def addphototag(photo_id):
    return render_template("profile.html", tag_upload=photo_id)

@app.route('/profile/mytag/<word>/', methods=['GET', 'POST'])
@flask_login.login_required
def showusertags(word):
    user_id = getUserIdFromEmail(flask_login.current_user.id)
    cursor= conn.cursor()
    cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes FROM Albums A, Photos P, Users U, NumLikes L, Tag_Photo T where U.user_id=A.owner_id AND A.owner_id='{0}' AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=T.photo_id AND T.word='{1}'".format(user_id, word))
    photos=cursor.fetchall()
    return render_template("profile.html", album_photos=photos, toptags=toptags(), mytags=mytags(user_id), alltags=alltags())
  

@app.route('/profile/<int:photo_id>/<word>/remove')
@flask_login.login_required
def remove_tag(photo_id, word):
    user_id = getUserIdFromEmail(flask_login.current_user.id)
    cursor=conn.cursor()
    cursor.execute("Delete from Tag_Photo where photo_id='{0}' AND word='{1}'".format(photo_id, word))
    conn.commit()
    return render_template("profile.html", photos=getUsersPhotos(user_id),profile_pic=getprofilepic(), toptags=toptags(), mytags=mytags(user_id), albums=getUsersAlbums(user_id))
    
@app.route('/profile/alluserstag/<word>/', methods=['GET','POST'])
@flask_login.login_required
def showalltags(word):
    if request.method=='POST':
        cursor= conn.cursor()
        cursor.execute("SELECT U.email, U.user_id, U.profile_pic, A.name, A.album_id, P.data, P.photo_id, P.caption, P.dates, L.numLikes FROM Albums A, Photos P, Users U, NumLikes L, Tag_Photo T where U.user_id=A.owner_id AND A.album_id=P.album_id AND P.photo_id=L.photo_id AND L.photo_id=T.photo_id AND T.word='{0}'".format(word))
        photos=cursor.fetchall()
        return render_template("profile.html", album_photos=photos, toptags=toptags(), alltags=alltags())
    else:
        user_id = getUserIdFromEmail(flask_login.current_user.id)
        return render_template("profile.html", photos=getUsersPhotos(user_id), toptags=toptags(), alltags=alltags())


def toptags():
    cursor= conn.cursor()
    cursor.execute("SELECT word, count(*) FROM Tag_Photo GROUP BY word LIMIT 10 ")
    return cursor.fetchall()

def alltags():
    cursor=conn.cursor()
    cursor.execute("SELECT word, photo_id FROM Tag_Photo")
    return cursor.fetchall()


def mytags(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT T.word, T.photo_id From Tag_Photo T, Users U, Albums A, Photos P where U.user_id = '{0}' AND U.user_id=A.owner_id AND A.album_id=P.album_id AND P.photo_id=T.photo_id".format(uid))
    return cursor.fetchall()
    

@app.route('/profile/home/', methods=['GET', 'POST'])
@flask_login.login_required
def profile_home():
    email=flask_login.current_user.get_id()
    user_id=getUserIdFromEmail(email)
    if flask.request.method=='GET':
        return render_template('profile_home.html', photos=getAllPhotosNotUsers(user_id), toptags=toptags(), alltags=alltags(), albums= getUsersAlbumsPhotos(user_id), mytags=mytags(user_id))
    else:
        try:
            comment = request.form['comment']
            photo_id= request.form['comment_photo_id']
            cursor= conn.cursor()
            cursor.execute("SELECT A.owner_id FROM Albums A, Photos P WHERE A.album_id=P.album_id AND P.photo_id='{0}'".format(photo_id))
            if user_id not in cursor.fetchall()[0]:
                cursor.execute("INSERT INTO Comment (text,photo_id,owner_id) VALUES ('{0}','{1}','{2}')".format(comment,photo_id,user_id))
                cursor.execute("UPDATE Users SET contribution= contribution + '1' where user_id='{0}'".format(user_id))
                cursor.execute("UPDATE NumComments SET numComments= numComments + '1' where photo_id='{0}'".format(photo_id))
                conn.commit()
                return render_template("profile.html", photos=getUsersPhotos(user_id),profile_pic=getprofilepic(), toptags=toptags(), mytags=mytags(user_id), albums=getUsersAlbums(user_id))
         else:
                return render_template("profile.html", photos=getUsersPhotos(user_id),profile_pic=getprofilepic(), toptags=toptags(), mytags=mytags(user_id), albums=getUsersAlbums(user_id))
        except:
                return render_template("profile.html", photos=getUsersPhotos(user_id),profile_pic=getprofilepic(), toptags=toptags(), mytags=mytags(user_id), albums=getUsersAlbums(user_id))
 


@flask_login.login_required
def protected():
    return render_template('profile.html', name=flask_login.current_user.id, message="Here's your profile")


#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/profile/upload', methods=['GET','POST'])
@flask_login.login_required
def uploadprofile():
    if request.method== 'POST':
        try:
            uid= getUserIdFromEmail(flask_login.current_user.id)
            imgfile = request.files['pro_pic']
            photo_data= base64.standard_b64encode(imgfile.read())
            cursor = conn.cursor()
            cursor.execute("UPDATE Users SET profile_pic='{0}' WHERE user_id='{1}'".format(photo_data, uid))
            conn.commit()
            return render_template("profile.html", photos= getUsersPhotos(uid), toptags=toptags(), alltags=alltags())
        except:
            return render_template("profile.html", photos= getUsersPhotos(uid), toptags=toptags(), alltags=alltags())
    else:
        return render_template("profile.html", album_photos=getUsersAlbumsphotos= getUsersPhotos(uid), toptags=toptags(), alltags=alltags())

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
    if request.method == 'POST':
        try:
            uid = getUserIdFromEmail(flask_login.current_user.id)
            imgfile = request.files['photo']
            caption = request.form.get('caption')
            album = request.form.get('album')
            photo_data = base64.standard_b64encode(imgfile.read())
            cursor = conn.cursor()
            if cursor.execute("SELECT A.album_id FROM Albums A  WHERE A.owner_id='{0}' AND A.name='{1}'".format(uid,album)):
                album_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO Photos(data,album_id, caption) VALUES ('{0}','{1}','{2}')".format(photo_data, album_id, caption))
                photo_id = cursor.lastrowid 
                cursor.execute("INSERT INTO NumLikes(photo_id) VALUES ('{0}')".format(photo_id))
                cursor.execute("INSERT INTO NumComments(photo_id) VALUES ('{0}')".format(photo_id))
                conn.commit()
                return render_template("profile_home.html", photos= getAllPhotos(), toptags=toptags(), alltags=alltags())
            else:
                cursor.execute("INSERT INTO Albums(name, owner_id) VALUES ('{0}','{1}')".format(album,uid))
                album_id = getAlbumId(album,uid)
                cursor.execute("INSERT INTO Photos (data, album_id, caption) VALUES ('{0}', '{1}', '{2}' )".format(photo_data,album_id, caption))        
                photo_id = cursor.lastrowid
                cursor.execute("INSERT INTO NumLikes(photo_id) VALUES ('{0}')".format(photo_id))
                cursor.execute("INSERT INTO NumComments(photo_id) VALUES ('{0}')".format(photo_id))
                conn.commit()
                return render_template("profile_home.html", photos= getAllPhotos(), toptags=toptags(), alltags=alltags())
        
        except:
            return render_template("profile_home.html", photos= getAllPhotos(), toptags=toptags(), alltags=alltags())
            
    else: return render_template("profile_home.html", photos= getAllPhotos(), toptags=toptags(), alltags=alltags())
            

#default page  
@app.route("/", methods=['GET'])
def hello():
	return render_template('home.html',)


if __name__ == "__main__":
	#this is invoked when in the shell  you run 
	#$ python app.py 
	app.run(port=5000, debug=True)
