from pprint import pprint
from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort
import flask
from flask.ext.login import LoginManager, UserMixin,login_required
import flask_login
import xmltodict, json
import requests
from flask.ext.jsonpify import jsonify



SOURCE_URL = 'https://api.litmos.com/v1.svc'
API_KAY = '?apikey=F84AE653-A0CF-473F-9145-C40DBA615810&source=MY-APP'
C_T = {"Content-Type": "application/json"}
# C_T = {"Content-Type": "text/xml"}

app = Flask(__name__)
# app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
class User(UserMixin):
    # proxy for a database of users
    pass
    # user_database = {"JohnDoe": ("JohnDoe", "John"),
    #            "JaneDoe": ("JaneDoe", "Jane")}
    # def __init__(self, username, password):
    #     self.id = username
    #     self.password = password
    #
    # @classmethod
    # def get(cls,id):
    #     return cls.user_database.get(id)


login_manager = LoginManager()
login_manager.init_app(app)
users = {'foo@bar.tld': {'pw': 'secret'}}
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['pw'] == users[email]['pw']
    return user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form[' pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
# login_manager.login_view = 'login'
#
#
# @login_manager.request_loader
# def load_user(request):
#     token = request.headers.get('Authorization')
#     if token is None:
#         token = request.args.get('token')
#
#     if token is not None:
#         username,password = token.split(":") # naive token
#         user_entry = User.get(username)
#         if (user_entry is not None):
#             user = User(user_entry[0],user_entry[1])
#             if (user.password == password):
#                 return user
#     return None

# @app.route('/')
# def index():
#     return render_template('index.html')
# @app.route("/",methods=["GET"])
# def index():
#     return render_template('login.html')

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     return redirect(url_for('index'))
    # return Response(response="Hello World!",status=200)


# @app.route("/protected/",methods=["GET"])
# @login_required
# def protected():
#     return Response(response="Hello Protected World!", status=200)


@app.route('/get_all_users', methods=['GET', 'POST'])
def get_all_users():
    ans = requests.get(SOURCE_URL + '/users' + API_KAY, headers=C_T)
    return jsonify(xmltodict.parse(ans.content))

@app.route('/get_user/<user_id>', methods=['GET', 'POST'])
def get_user(user_id):
    ans = requests.get(SOURCE_URL + '/users/'+user_id + API_KAY, headers=C_T)

    print(ans.headers)
    return jsonify(xmltodict.parse(ans.content))


@app.route('/get_all_courses', methods=['GET', 'POST'])
def get_all_courses():
    ans = requests.get(SOURCE_URL + '/courses' + API_KAY, headers=C_T)
    return json.dumps(xmltodict.parse(ans.content))




@app.route('/get_courses_assign_user/<user_id>', methods=['GET', 'POST'])
def get_courses_assign_user(user_id):
    ans = requests.get(SOURCE_URL + '/users/' + user_id +'/courses' + API_KAY, headers=C_T)
    return json.dumps(xmltodict.parse(ans.content))


j={
  "Courses": {
    "Course": { "Id": "'POYwU1fofdw1'" }
  }
}

# xml='<Courses><Course><Id>pwbXSvNf_L01</Id></Course></Courses>'
# r=requests.post("https://api.litmos.com/v1.svc/users/vOrVE-3SvnA1/courses?apikey=F84AE653-A0CF-473F-9145-C40DBA615810&source=MY-APP&"
#                                                                              ,data=json.dumps(j),headers={"Content-Type":"application/json"})
#
#
# # print(j)
# print(r.reason)
# POST /users/{user-id}/courses


@app.route('/assignCourseToUser/<user_id>/<course_id>', methods=['GET', 'POST'])
def assignCourseToUser(user_id, course_id):

    xml='<Courses><Course><Id>'+course_id+'</Id></Course></Courses>'

    body={
      "Courses": {
        "Course": { "Id": course_id }
      }
    }

    ans = requests.post(SOURCE_URL + '/users/' + user_id + '/courses'+ API_KAY, data=xml, headers=C_T)
    return json.dumps(ans.status_code)



# DELETE /users/{user-id}/courses/{course-id}

@app.route('/delete_course_from_user/<userId>/<courseid>', methods=['GET', 'POST'])
def delete_course_from_user(userId,courseid):
    ans = requests.delete(SOURCE_URL + '/users/' + userId +'/courses/'+ courseid + API_KAY, headers=C_T)
    return json.dumps(ans.status_code)

@app.route('/get_users_assign_course/<courseid>', methods=['GET', 'POST'])
def get_users_assign_course(courseid):
    ans = requests.get(SOURCE_URL + '/courses/' + courseid +'/users' + API_KAY, headers=C_T)
    return json.dumps(xmltodict.parse(ans.content))

TODO = {
    'eli@eligur.com': ['java-course', 'php-course'],
    'josh@ravtech.co.il': ['css', 'java', 'php-course']
}


@app.route('/get_my_todo')
# @login_required
def get_my_todo():
    return jsonify(TODO.get('eli@eligur.com', []))
    # return json.dumps(TODO.get('eli@eligur.com', []))
if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(
        host="localhost",
        port=int("5001"),
        debug=True
    )
