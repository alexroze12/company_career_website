from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, session, make_response
from database import load_jobs_from_database, load_job_from_database, load_all_jobs_from_database, add_information_about_person, delete_information_from_database, update_information_about_person
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


app = Flask(__name__)
app.config['SECRET_KEY'] = ''

def token_required(func):
  @wraps(func)
  def decorated(*args, **kwargs):
    token = request.args.get('token')
    if not token:
      return jsonify({"Allert!": "Token is missing"})
    try:
      payload = jwt.decode(token, app.config['SECRET_KEY'])
    except:
      return jsonify({"Allert!": "Invalid Token"})
  return decorated

github_blueprint = make_github_blueprint(client_id='37a5229eb8ea708e7660',client_secret='5b0bf54681fb0145a9224130609f8bcc4c062754')
google_blueprint = make_google_blueprint(client_id='224208229278-nj1gnbvrk9goihb4rfej8i0vstl7j67b.apps.googleusercontent.com', client_secret='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', scope=["profile", "email"])

app.register_blueprint(github_blueprint, url_prefix="/github_login")
app.register_blueprint(google_blueprint, url_prefix="/login")


@app.route('/information')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return 'Logged in currently'

@app.route('/')
def hello_world():
  jobs = load_jobs_from_database()
  return render_template('home.html', jobs=jobs, company_name='Company')


@app.route('/person_login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
      return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


@app.route('/google')
def google_login():
  jobs = load_jobs_from_database()
  if not google.authorized:
    return redirect(url_for('google.login'))
  account_info = github.get('/plus/v1/people/me')
  if account_info.ok:
    account_info_json = account_info.json() 
    return render_template('home.html', jobs=jobs, company_name='Company')
  return '<h1>Request failed!</h1>'

@app.route('/github')
def github_login():
  jobs = load_jobs_from_database()
  if not github.authorized:
    return redirect(url_for('github.login'))
  account_info = github.get('/user')
  if account_info.ok:
    account_info_json = account_info.json() 
    return render_template('home.html', jobs=jobs, company_name='Company')
  return '<h1>Request failed!</h1>'

@app.route('/script_spa.js')
@app.route("/job_page_spa.html")
def spa():
  return send_from_directory(app.static_folder, request.path[1:])

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_database()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job_information(id):
  all_jobs = load_all_jobs_from_database(id)
  job = load_job_from_database(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job, all_jobs=all_jobs)

@app.route("/job/<id>/add", methods=['post'])
def add_people(id):
  name = request.form['name']
  gender = request.form['gender']
  age = request.form['age']
  country = request.form['country']
  add_information_about_person(id, name, gender, age, country)
  return show_job_information(id)
  
    
@app.route("/job/<index>/<id>/delete", methods=['post', 'get'])
def delete_information(index, id):
  delete_information_from_database(index, id)
  return show_job_information(index)


@app.route("/job/<index>/<id>/upd", methods=['post', 'get'])
def update_information(index, id):
  name = request.form['name_1']
  gender = request.form['gender_1']
  age = request.form['age_1']
  country = request.form['country_1']
  update_information_about_person(index, id, name, gender, age, country)
  return show_job_information(index)

app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !  '

if __name__== "__main__":
  app.run(host="0.0.0.0", debug=True)
  