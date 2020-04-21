from flask import Flask, render_template, redirect, request, url_for
import pymysql
app = Flask(__name__)


db= pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='password',
                     db='new',
                     charset='utf8')

cursor = db.cursor()


# 문제만들기 화면
@app.route('/question')
def db_insert_q():
    return render_template('home.html')


# 문제 만들기
@app.route('/question/make',methods = ['POST'])
def make_question():
    sql = """INSERT INTO question(q_user_id,subject, topic, content)
                 VALUES(\'{q_user_id}\', \'{subject}\',\'{topic}\',\'{content}\');"""
    sql = sql.format(q_user_id = request.form['q_user_id'], subject=request.form['subject'],topic= request.form['topic'], content=request.form['content'])
    print(sql)
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('success'))

# 문제 보기
@app.route('/question/view')
def view_question():
    sql = """SELECT * FROM question;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()

    return render_template('question_list.html', result =result)

@app.route('/success')
def success(name):
   return '문제 만들기 성공'

# 문제 풀기
@app.route('/question/solve')
def view_question():
    sql = """SELECT * FROM question;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()

    return render_template('question_list.html', result =result)


@app.route('/')
@app.route('/<int:num>')
def inputTest(num=None):
    return render_template('main.html', num=num)



if __name__ == '__main__':
    app.run()

