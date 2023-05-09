from flask import Flask, render_template, jsonify
from database import load_jobs_from_database, load_job_from_database, load_cooks_from_database


app = Flask(__name__)


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
  cooks_prof = load_cooks_from_database()
  job = load_job_from_database(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job, cooks=cooks_prof)


if __name__== "__main__":
  app.run(host="0.0.0.0", debug=True)