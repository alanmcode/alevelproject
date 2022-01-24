#from PyQt import QtCore, QtGui, QtWidgets, QApplication, QLabel
import sqlite3
import random

DB = 'qtable.sqlite'

def create_connection(db):
    #creates connection to the database
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print (e)
    return conn

            
def GetQuestions(conn):
    #retrieves questions from database via PyQt input
    cursor = conn.cursor()
    #link below SQL with the PyQt GUI after
    cursor.execute('''
    SELECT Question FROM QTable
    WHERE Unit=12 OR Unit=7
    AND AO1=1 AND (AO2=1 OR AO2=0) AND AO3=0''')

    questions = cursor.fetchall()
    #print(questions)
    question = questions
    
    for i in range(len(questions)):
        print(question[1])
        print(question[4])
        print(question[2])
        #print(question.random)
        break

    return questions

def GetMarks(conn):
    cursor = conn.cursor()
    global marks
    
    for question in questions:
        cursor.execute('''
        SELECT Marks FROM QTable''')
    marks = cursor.fetchall()
    
    for mark in marks:
        print(marks[1])
        print(marks[2])
        print(marks[5])
        break
    print(marks)
    return marks


def GenerateHTML(questions):
    examPaper = open('ExamPaperTemplate.html',"r" )
    lines = examPaper.readlines()

    examPaperOutput = open("ExamPaperOutput.html", "w")
    
    for line in lines:
        if "{questions}" in line:
            for question in questions:
                examPaperOutput.write("<p>")
                examPaperOutput.write(str(question))
                examPaperOutput.write("</p>")
                examPaperOutput.write("\n")

            if marks in question > 5:
                examPaperOutput.write("<p>")
                examPaperOutput.write("________________________________________________________________")
                examPaperOutput.write("</p>")
                examPaperOutput.write("<p>")
                examPaperOutput.write("________________________________________________________________")
                examPaperOutput.write("</p>")
                examPaperOutput.write("<p>")
                examPaperOutput.write("________________________________________________________________")
                examPaperOutput.write("</p>")
                examPaperOutput.write("<p>")
                examPaperOutput.write("________________________________________________________________")
                examPaperOutput.write("</p>")
        else:
            examPaperOutput.write(line)
                
    examPaperOutput.close()
    examPaper.close()

#creates connection
conn = create_connection(DB)
#extracts questions
questions = GetQuestions(conn)
#extracts marks
GetMarks(conn)
#writes the HTML paper
GenerateHTML(questions)
