from flask import Flask, render_template
from flask_mysqldb import MySQL, MySQLdb
import cloudinary
import cloudinary.uploader


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SSIS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

cloudinary.config(
    cloud_name = 'dglj9023b',
    api_key = '115467398695897',
    api_secret = '3tS8qm3H5BdgSmbfmvkdTKotAlk'
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