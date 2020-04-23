from flask import Flask, render_template, redirect, request, url_for
import pymysql
app = Flask(__name__)

# DB 연결
db= pymysql.connect(host='172.31.18.206',
                     port=3306,
                     user='test',
                     passwd='passwd',
                     db='studyblank',
                     charset='utf8')

cursor = db.cursor()




@app.route('/')
def root():
    return render_template('home.html')



# 문제만들기 화면
@app.route('/question')
def db_insert_q():
    return render_template('question_make.html')


# 문제장 insert
@app.route('/question/make',methods = ['POST'])
def make_question_list():
    sql = """INSERT INTO question(q_user_id,subject, topic, content)
                 VALUES(\'{q_user_id}\', \'{subject}\',\'{topic}\',\'{content}\');"""
    sql = sql.format(q_user_id = request.form['q_user_id'], subject=request.form['subject'],topic= request.form['topic'], content=request.form['content'])
    print(sql)
    cursor.execute(sql)
    db.commit()

    return redirect(url_for('success'))



@app.route('/success', methods=['POST','GET'])
def success(name):
   return '문제 만들기 성공'





# 문제 보기

@app.route('/question/view')
def view_question():
    sql = """SELECT * FROM question;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()

    return render_template('question_list.html', result =result)




# 오답노트 보기

@app.route('/incorrect_note/view')
@app.route('/incorrect_note/view/<int:a_user_id>')
def view_incorrect_note(a_user_id = None, result = None):
    if a_user_id ==None:
        result= None
    else:
        sql = """SELECT * FROM answer where a_user_id = {a_user_id};""".format(a_user_id= a_user_id)

        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()

    return render_template('incorrect_list.html', a_user_id =a_user_id ,result = result)

@app.route('/incorrect_note', methods=['POST'])
def incorrect_note(a_user_id=None):
    if request.method =='POST':
        temp = request.form['a_user_id']
    else:
        temp =None
    return redirect(url_for('view_incorrect_note',a_user_id =temp))




# 문제 풀기
@app.route('/question/solve')
def solve_question(score=None):
    sql = """ SELECT q_id, content FROM question ORDER BY RAND() LIMIT 10;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    parsed = []

    answer_list=[]
    for i in result:
        parsed.append(parse_question(i))
    # print(parsed)


    return render_template('question_solve.html',result =parsed ,answer_list = answer_list ,score = score)


# 문제 빈칸 파싱 함수
def parse_question(input):
    question = []  # 구멍 뚫린 문제를 만들기 위한 임시 리스트
    inputString = input[1]
    for i in range(len(inputString)):
        question.append(inputString[i])
    answersheet = list()  # 괄호안에 들어갈 정답

    for i in range(0, len(inputString)):
        if (inputString[i] == '('):
            temp = ''  # 정답 키워드를 빼내오기 위한 변수
            indexStart = i
            indexEnd = 0
            while (inputString[i] != ')'):
                i += 1
                if (inputString[i] != ')'):
                    temp += inputString[i]
                    indexEnd = i
            answersheet.append(temp)

            for j in range(indexStart + 1, indexEnd + 1):  # 괄호 안 키워드 대신 공백으로 채움
                question[j] = ' '
    return '/'.join(answersheet), ''.join(question), input[0]



# 성적 처리 및 오답노트db insert
@app.route('/grade', methods = ['POST'])
def grade(answer=None):
    if request.method == 'POST':
        user_answer = request.form.getlist('user_answer')
        real_answer = request.form.getlist('real_answer')
        real_question = request.form.getlist('real_question')
        q_id = request.form.getlist('q_id')
        grade_result =[]
        for i in range(len(user_answer)):
            print(user_answer[i], " ",real_answer[i])
            tmp=[]
            tmp.append(q_id[i])
            tmp.append(user_answer[i])
            tmp.append(real_answer[i])

            if user_answer[i] == real_answer[i]:
                tmp.append('정답')
            else:
                tmp.append('오답')
                sql = """INSERT INTO answer( a_user_id, user_answer, true_answer,q_id)
                         VALUES(1,\'{user_answer}\', \'{real_answer}\' , {q_id});"""
                sql = sql.format(user_answer = user_answer[i], real_answer=real_answer[i], q_id=q_id[i])
                print(sql)
                cursor.execute(sql)
                db.commit()
            grade_result.append(tmp)

    else:
        answer = None



    return render_template('question_solve.html',real_answer=real_answer,real_question=real_question , score =grade_result )





if __name__ == '__main__':
    app.run()

