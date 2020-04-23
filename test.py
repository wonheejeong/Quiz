def quiz(s):
    implemented = []
    for i in range(len(s)):
        implemented.append(s[i])
    answersheet = list()
    wrong = list()

    for i in range(0, len(s)):
        if(s[i]=='('):
            temp = ''
            indexStart = i
            indexEnd = 0
            while(s[i]!=')'):
                i+=1
                if(s[i]!=')'):
                    temp+=s[i]
                    indexEnd = i
            answersheet.append(temp)

            for j in range(indexStart+1,indexEnd+1):
                implemented[j]=' '

    print(''.join(implemented))

    useranswer = list()

    for i in range(0,len(answersheet)):
        temp = input()
        useranswer.append(temp)

    correct = 0

    for i in range(0,len(useranswer)):
        if(useranswer[i]==answersheet[i]):
            correct +=1

    if(len(useranswer)==correct):
        print("다 맞았습니다")
    else:
        print(len(answersheet)-correct,"개 틀렸습니다. 오답노트 저장을 원하시면 Yes를 입력해주세요")
        temp = input()
        if(temp =='Yes'):
            wrong.append(implemented)
'''
    return render_template('question_list.html',result=wrong)
'''