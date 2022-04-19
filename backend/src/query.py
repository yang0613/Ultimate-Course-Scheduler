import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#psql postgres
#\c to check `CURRENT_USER`
#Create username with: CREATE USER postgres;
#grant `CURRENT_USER` to postgres;
#Postgres login: psql -d postgres -U postgres

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/5432'

# db = SQLAlchemy(app)

# major = Majors.query.all()

conn = psycopg2.connect('dbname=postgres user=postgres host=localhost', options='-c search_path=Majors')
cur = conn.cursor()

cur.execute("SELECT * FROM Classes WHERE classID LIKE 'CSE 12'")
print(cur.fetchall())