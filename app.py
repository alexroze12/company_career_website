from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
  {
    'id': 1,
    'title': 'Waiter',
    'location': 'Belarus, Minsk',
    'salary': '900 Br'
  },
  {
    'id': 2,
    'title': 'Cook',
    'location': 'Belarus, Minsk',
    'salary': '1100 Br'
  },
  {
    'id': 3,
    'title': 'Restaurant manager',
    'location': 'Belarus, Minsk',
    'salary': '1600 Br'
  },
  {
    'id': 4,
    'title': 'Сonfectioner',
    'location': 'Belarus, Minsk',
    'salary': '1200 Br'
  }
]

@app.route("/") 
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name='Kukusiki')

@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)

if __name__== "__main__":
  app.run(host="0.0.0.0", debug=True)