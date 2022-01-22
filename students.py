from flask import Blueprint, render_template, request
from flask_mysqldb import MySQLdb
from flask.helpers import url_for
from werkzeug.utils import redirect
from app import mysql
import cloudinary
import cloudinary.uploader

students = Blueprint('students', __name__, url_prefix='/students')

def uploadImage(image):
    uploadInput = cloudinary.uploader.upload(image, folder = "SSIS - profiles")
    return uploadInput['secure_url']

# function for add_student page
@students.route("/add_student")
def add_student():
    title = 'Add Student'
    return render_template("add_student.html", title=title)

# function for edit_student page
@students.route("/edit_student/<string:id_num>")
def edit_student(id_num):
    title = 'Edit Student'
    # loads data from student table into fields to be edited
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM student WHERE id_num = %s''',(id_num,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_student.html",student_info=data, title=title)

# function for add(students) action
@students.route("/add", methods = ['POST'])
def add():
    #requests input from webpage
    if request.method == 'POST':
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        yearlvl = request.form['yearlvl']
        gender = request.form['gender']
        image = request.files['file']

        stud_img_url = uploadImage(image)
        
        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s,%s)''',(id_num, fname, lname, course, yearlvl, gender, stud_img_url, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

#function for delete(students) action
@students.route("/delete/<string:id_num>", methods = ['GET'])
def delete(id_num):
        #removes records from student table through id_num
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM student WHERE id_num = %s''',(id_num,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

#function for edit(students)action
@students.route("/edit/<string:id_num>", methods = ['POST'])
def edit(id_num):
    if request.method == 'POST':
        #requests input from webpage
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        yearlvl = request.form['yearlvl']
        gender = request.form['gender']
        image = request.files['file']

        if image:
            stud_img_url = uploadImage(image)
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE student SET stud_img_url = %s WHERE id_num = %s''',(stud_img_url, id_num,))
            mysql.connection.commit()
            cursor.close()

        #updates records from student table through id_num
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student SET stud_fname = %s, stud_lname = %s, course_code = %s, stud_yearlvl = %s, stud_gender = %s WHERE id_num = %s''',(fname, lname, course, yearlvl, gender, id_num))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))
