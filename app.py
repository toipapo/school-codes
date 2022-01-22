from flask import Flask, render_template
from flask_mysqldb import MySQL, MySQLdb
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader

load_dotenv()
app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_DB")
app.config['MYSQL_CURSORCLASS'] = os.getenv("DB_CURSORCLASS")

cloudinary.config(
    cloud_name = os.getenv('cloud_name'),
    api_key = os.getenv('api_key'),
    api_secret = os.getenv('api_secret')
)

mysql = MySQL(app)

from students import students
from courses import courses
from colleges import colleges

app.register_blueprint(students)
app.register_blueprint(courses)
app.register_blueprint(colleges)

# function for students homepage
@app.route("/")
def index():
    try:
        #load data from student table into student homepage
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM student ORDER BY id_num")
        data = cursor.fetchall()
        print(data)
        return render_template("home.html", student=data)
    
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)