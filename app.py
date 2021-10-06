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

@app.route("/")
def index():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM student ORDER BY id_num")
        data = cursor.fetchall()
        print(data)
        return render_template("home.html", student=data)
    
    except Exception as e:
        return str(e)

@app.route("/courses")
def courses():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM course ORDER BY college_code")
        data = cursor.fetchall()
        print(data)
        return render_template("courses.html", course=data)
    
    except Exception as e:
        return str(e)

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

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/add_coursepage")
def add_coursepage():
    return render_template("add_course.html")

@app.route("/add_collegepage")
def add_collegepage():
    return render_template("add_college.html")

@app.route("/edit_student/<string:id_num>")
def edit_student(id_num):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM student WHERE id_num = %s''',(id_num,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_student.html",student_info=data)

@app.route("/edit_coursepage/<string:course_code>")
def edit_coursepage(course_code):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM course WHERE course_code = %s''',(course_code,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_course.html",course_info=data)

@app.route("/edit_collegepage/<string:college_code>")
def edit_collegepage(college_code):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM college WHERE college_code = %s''',(college_code,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_college.html",college_info=data)

@app.route("/add", methods = ['POST'])
def add():
    if request.method == 'POST':
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        yearlvl = request.form['yearlvl']
        gender = request.form['gender']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)''',(id_num, fname, lname, course, yearlvl, gender))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

@app.route("/add_course", methods = ['POST'])
def add_course():
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO course VALUES(%s,%s,%s)''',(course_code, course_name, college_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))

@app.route("/add_college", methods = ['POST'])
def add_college():
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO college VALUES(%s,%s)''',(college_code, college_name))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

@app.route("/delete/<string:id_num>", methods = ['GET'])
def delete(id_num):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM student WHERE id_num = %s''',(id_num,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

@app.route("/delete_course/<string:course_code>", methods = ['GET'])
def delete_course(course_code):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM course WHERE course_code = %s''',(course_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))

@app.route("/delete_college/<string:college_code>", methods = ['GET'])
def delete_college(college_code):
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM college WHERE college_code = %s''',(college_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

@app.route("/edit/<string:id_num>", methods = ['POST'])
def edit(id_num):
    if request.method == 'POST':
        id_num = request.form['id_num']
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course']
        yearlvl = request.form['yearlvl']
        gender = request.form['gender']

        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE student SET stud_fname = %s, stud_lname = %s, course_code = %s, stud_yearlvl = %s, stud_gender = %s WHERE id_num = %s''',(fname, lname, course, yearlvl, gender, id_num))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("index"))

@app.route("/edit_course/<string:course_code>", methods = ['POST'])
def edit_course(course_code):
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE course SET course_name = %s, college_code = %s WHERE course_code = %s''',(course_name, college_code, course_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses"))

@app.route("/edit_college/<string:college_code>", methods = ['POST'])
def edit_college(college_code):
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE college SET college_name = %s WHERE college_code = %s''',(college_name, college_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

if __name__ == "__main__":
    app.run(debug=True)