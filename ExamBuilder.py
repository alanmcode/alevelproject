import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit
from PyQt5 import uic, QtWidgets
import sqlite3
import random

Ui_MainWindow, QtBaseClass = uic.loadUiType("ExamBuilder_CSfilters.ui") 

class ExamBuilder(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = 'qtable.sqlite'
        self.create_connection()
        self.GetQuestions()
        #self.GenerateHTML()

        #Generate
        self.ui.commandLinkButton_generate.clicked.connect(self.Generate)

        
    def create_connection(self):
        #creates connection to the database
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db)
        except Error as e:
            print (e)
        #return conn

    def GetMarks(self):
        cursor = self.conn.cursor()
        global marks
        
        cursor.execute('''SELECT Marks FROM QTable''')
        marks = cursor.fetchall()

        #test code
        for mark in marks:
            print(marks[1])
            print(marks[2])
            print(marks[5])
            break
        print(marks)
        return marks
                
    def GetQuestions(self):
        #retrieves questions from database via PyQt input
        cursor = self.conn.cursor()

        AnyAO = int(self.ui.checkBox_anyao.isChecked())
        AO1 = int(self.ui.checkBox_ao1.isChecked())
        AO2 = int(self.ui.checkBox_ao2.isChecked())
        AO3 = int(self.ui.checkBox_ao3.isChecked())
        
        if AnyAO == int(self.ui.checkBox_anyao.isChecked()) == 1:
            AO1 = int(self.ui.checkBox_ao1.isChecked()+1)
            AO2 = int(self.ui.checkBox_ao2.isChecked()+1)
            AO3 = int(self.ui.checkBox_ao3.isChecked()+1)

        elif AO1 or AO2 or AO3 == 2:
            print("error")

        Unit1 = int(self.ui.checkBox_1.isChecked()*1)
        Unit2 = int(self.ui.checkBox_2.isChecked()*2)
        Unit3 = int(self.ui.checkBox_3.isChecked()*3)
        Unit4 = int(self.ui.checkBox_4.isChecked()*4)
        Unit5 = int(self.ui.checkBox_5.isChecked()*5)
        Unit6 = int(self.ui.checkBox_6.isChecked()*6) 
        Unit7 = int(self.ui.checkBox_7.isChecked()*7)
        Unit8 = int(self.ui.checkBox_8.isChecked()*8)
        Unit9 = int(self.ui.checkBox_9.isChecked()*9)
        Unit10 = int(self.ui.checkBox_10.isChecked()*10)
        Unit11 = int(self.ui.checkBox_11.isChecked()*11)
        Unit12 = int(self.ui.checkBox_12.isChecked()*12)

        duration30 = int(self.ui.radioButton_30m.isChecked())
        duration1h = int(self.ui.radioButton_1h.isChecked())
        duration2h30m = int(self.ui.radioButton_2h30m.isChecked())

        #duration = int(self.ui.lineEdit_duration.text())

        #testing purposes for system
        print("Units")
        print(Unit1)
        print(Unit2)
        print(Unit3)
        print(Unit4)
        print(Unit5)
        print(Unit6)
        print(Unit7)
        print(Unit8)
        print(Unit9)
        print(Unit10)
        print(Unit11)
        print(Unit12)
        print("AOs")
        print(AnyAO)
        print(AO1)
        print(AO2)
        print(AO3)
        print("Duration")
        print(duration30)
        print(duration1h)
        print(duration2h30m)
        #print(duration)

        questions = []
        tempquestions = []
        
        cursor.execute('''
        SELECT Question FROM QTable
        WHERE (Unit=? OR Unit=? OR Unit=? OR Unit=? OR Unit=? OR Unit=? OR
        Unit=? OR Unit=? OR Unit=? OR Unit=? OR Unit=? OR Unit=?) 
        AND (AO1=? OR AO2=? OR AO3=?)''', (Unit1,Unit2,Unit3,Unit4,Unit5,Unit6,Unit7,Unit8,Unit9,Unit10,Unit11,Unit12,AO1,AO2,AO3,))

        questions = cursor.fetchall()

        #duration settings
        if duration30 == 1:
            questions = questions[0:10]

        elif duration1h == 1:
            questions = questions[0:15]

        elif duration2h30m == 1:
            questions = questions[0:20]

##        #new duration settings
##        for question in questions:
##            marks[question]
##            print(marks)
##        time = marks * 1.1
##        
##        print(time)

        #adding fitted in questions to final exam paper list
        for question in tempquestions:
            questions.append(question)
        random.shuffle(questions)
        return questions


    def SubmitQuestion(self):
        #user submission to database
        cursor = self.conn.cursor
        sub = str(input())
        userQ = str(input())
        userMarks = int(input())
        userUnit = int(input())
        userAO1 = bool(input())
        userAO2 = bool(input())
        userAO3 = bool(input())
        userMrkSch = str(input())
        userApproved = 0
        #inputs to be PyQt integrated buttons
        
        cursor.execute('''INSERT INTO QTable
                        (ID,Subject,Question,Unit,Marks,AO1,AO2,AO3,MrkScheme)
                        VALUES(?,?,?,?,?,?,?,?,?)'''(sub,userQ,userMarks,userUnit,
                                                     userAO1,userAO2,userAO3,
                                                     userMrkSch,))

        #test
        #print(sub,userQ,userMarks,userUnit,userAO1,userAO2,userAO3,userMrkSch)
        conn.commit()
        cursor.close()
        

    def GenerateHTML(self):
        #writes and generates HTML exam paper
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

                #for marks in question(0,5):
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
                examPaperOutput.write(line) #validation

        #add mark scheme to file
        cursor = self.conn.cursor
        getmrksch = int(self.ui.checkBox_addmrksch.isChecked())

        if getmrksch == 1:
            cursor.execute('''SELECT * MrkSch WHERE Question = ?'''(questions[question]))

            markscheme = []
            markscheme = cursor.fetchall()

            examPaperOutput.write("<p>")
            examPaperOutput.write("---Mark Scheme---")
            examPaperOutput.write("</p>")

            for markq in markscheme:
                examPaperOutput.write("<p>")
                examPaperOutput.write(str(markq))
                examPaperOutput.write("</p>")

        else:
            examPaperOutput.write("<p>")
            examPaperOutput.write("End Of Questions")
            examPaperOutput.write("</p>")
                    
        examPaperOutput.close()
        examPaper.close()

    def Generate(self):
        #object that generate the HTML when generate button is clicked
        #print("generating")
        questions = self.GetQuestions()
        for question in questions:
            print("".join(question))
        self.GenerateHTML()
        #self.GenerateHTML(questions)
        
def main():
    app = QApplication(sys.argv)
    window = ExamBuilder() #initialise UI
    window.show() #shows window
    sys.exit(app.exec_())

main()
