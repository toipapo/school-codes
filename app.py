from MySQLdb import cursors
from flask import Flask, render_template,request,jsonify
from flask_mysqldb import MySQL, MySQLdb
from flask.helpers import url_for
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SSIS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

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

# function for courses homepage
@app.route("/courses")
def courses():
    try:
        #load data from course table into course homepage
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM course ORDER BY college_code")
        data = cursor.fetchall()
        print(data)
        return render_template("courses.html", course=data)
    
    except Exception as e:
        return str(e)

# function for colleges homepage
@app.route("/colleges")
def colleges():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM college ORDER BY college_code")
        data = cursor.fetchall()
        print(data)
        return render_template("colleges.html", college=data)
    
    except Exception as e:
        return str(e)

# function for add_student page
@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

# function for add_course page
@app.route("/add_coursepage")
def add_coursepage():
    return render_template("add_course.html")

# function for add_college page
@app.route("/add_collegepage")
def add_collegepage():
    return render_template("add_college.html")

# function for edit_student page
@app.route("/edit_student/<string:id_num>")
def edit_student(id_num):
    # loads data from student table into fields to be edited
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM student WHERE id_num = %s''',(id_num,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_student.html",student_info=data)

# function for edit_course page
@app.route("/edit_coursepage/<string:course_code>")
def edit_coursepage(course_code):
    # loads data from course table into fields to be edited
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM course WHERE course_code = %s''',(course_code,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_course.html",course_info=data)

# function for edit_college page
@app.route("/edit_collegepage/<string:college_code>")
def edit_collegepage(college_code):
    # loads data from college table into fields to be edited
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM college WHERE college_code = %s''',(college_code,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_college.html",college_info=data)

# function for add(students) action
@app.route("/add", methods = ['POST'])
def add():
    #requests input from webpage
    if request.method == 'POST':
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        yearlvl = request.form['yearlvl']
        gender = request.form['gender']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)''',(id_num, fname, lname, course, yearlvl, gender))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

#function for add_course action
@app.route("/add_course", methods = ['POST'])
def add_course():
    if request.method == 'POST':
        #requests input from webpage
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO course VALUES(%s,%s,%s)''',(course_code, course_name, college_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))

#function for add_college action
@app.route("/add_college", methods = ['POST'])
def add_college():
    if request.method == 'POST':
        #requests input from webpage
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO college VALUES(%s,%s)''',(college_code, college_name))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

#function for delete(students) action
@app.route("/delete/<string:id_num>", methods = ['GET'])
def delete(id_num):
        #removes records from student table through id_num
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM student WHERE id_num = %s''',(id_num,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

#function for delete_course action
@app.route("/delete_course/<string:course_code>", methods = ['GET'])
def delete_course(course_code):
        #removes records from course table through course_code
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM course WHERE course_code = %s''',(course_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))

#function for delete_college action
@app.route("/delete_college/<string:college_code>", methods = ['GET'])
def delete_college(college_code):
        #removes records from college table through college_code
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM college WHERE college_code = %s''',(college_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

#function for edit(students)action
@app.route("/edit/<string:id_num>", methods = ['POST'])
def edit(id_num):
    if request.method == 'POST':
        #requests input from webpage
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        yearlvl = request.form['yearlvl']
        gender = request.form['gender']

        #updates records from student table through id_num
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student SET stud_fname = %s, stud_lname = %s, course_code = %s, stud_yearlvl = %s, stud_gender = %s WHERE id_num = %s''',(fname, lname, course, yearlvl, gender, id_num))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

#function for edit_course action
@app.route("/edit_course/<string:course_code>", methods = ['POST'])
def edit_course(course_code):
    if request.method == 'POST':
        #requests input from webpage
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        #updates records from course table through course_code
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE course SET course_name = %s, college_code = %s WHERE course_code = %s''',(course_name, college_code, course_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))

#function for edit_college action
@app.route("/edit_college/<string:college_code>", methods = ['POST'])
def edit_college(college_code):
    if request.method == 'POST':
        #requests input from webpage
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        #updates records from college table through college_code
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE college SET college_name = %s WHERE college_code = %s''',(college_name, college_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

if __name__ == "__main__":
    app.run(debug=True)