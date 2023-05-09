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

def load_cooks_from_database():
  with engine.connect() as conn:
    result = conn.execute(text("select * from cooks"))
    column_names = result.keys()
    cooks = []
    for row in result.all():
      first_result_dict = dict(zip(column_names, row))
      cooks.append(first_result_dict)
    return cooks

def load_job_from_database(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"select * from jobs where id = {id}"))
    rows = result.all()
    column_names = result.keys()
    if len(rows) == 0:
      return None
    else:
      return dict(zip(column_names, rows[0]))
  