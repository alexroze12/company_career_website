from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string, connect_args={
  "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
})

def load_jobs_from_database():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    column_names = result.keys()
    jobs = []
    for row in result.all():
      first_result_dict = dict(zip(column_names, row))
      jobs.append(first_result_dict)
    return jobs

def load_all_jobs_from_database(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"select * from job_{id}"))
    column_names = result.keys()
    job = []
    for row in result.all():
      first_result_dict = dict(zip(column_names, row))
      job.append(first_result_dict)
    return job

def load_job_from_database(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"select * from jobs where id = {id}"))
    rows = result.all()
    column_names = result.keys()
    if len(rows) == 0:
      return None
    else:
      return dict(zip(column_names, rows[0]))

def add_information_about_person(job_index_id, name_id, gender_id, age_id, country_id):
  with engine.connect() as conn:
    result = conn.execute(text(f"INSERT INTO job_{job_index_id} (name, gender, age, country, job_index) VALUES ('{name_id}', '{gender_id}', '{age_id}', '{country_id}', '{job_index_id}')"))

def update_information_about_person(index, id, name_id, gender_id, age_id, country_id):
  with engine.connect() as conn:
    result = conn.execute(text(f"UPDATE job_{index} SET name = '{name_id}', gender = '{gender_id}', age = '{age_id}', country = '{country_id}' WHERE id = '{id}'"))


def delete_information_from_database(index, id):
  with engine.connect() as conn:
    result = conn.execute(text(f"delete from job_{index} where id = {id}"))