from flask import Flask, render_template, jsonify, request, send_from_directory
from database import load_jobs_from_database, load_job_from_database, load_all_jobs_from_database, add_information_about_person, delete_information_from_database, update_information_about_person


app = Flask(__name__)

@app.route("/job_page_spa.html/<id>")
def spa():
  all_jobs = load_all_jobs_from_database(id)
  job = load_job_from_database(id)
  return send_from_directory(app.static_folder, request.path[1:], job=job, all_jobs=all_jobs)

@app.route("/") 
def hello_world():
  jobs = load_jobs_from_database()
  return render_template('home.html', jobs=jobs, company_name='Kukusiki')

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_database()
  return jsonify(jobs) #rest api

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


if __name__== "__main__":
  app.run(host="0.0.0.0", debug=True)