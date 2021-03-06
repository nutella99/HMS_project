import sys
import psycopg2
from PySide.QtCore import QRegExp, QPoint
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader

from Base.Dialog_MsgBox import ConfirmMsgClass
from Patient import PatientClass

class EditOrNewEmployeeDialog(QDialog):
    def __init__(self, editOrNew, id=0, parent=None):
        super(EditOrNewEmployeeDialog, self).__init__(parent)
        self.editOrNew = editOrNew
        self.idEmployee = id
        self.setGeometry(300, 200, 400, 400)
        self.loader = QUiLoader()
        self.ui = self.loader.load('./view/Dialog_EditOrNewEmployeeUI.ui', self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.ui)
        self.initUI()
        self.ans = []
        self.show()


    def initUI(self):
        self.setInput = []
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_1"))
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_2"))
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_3"))
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_4"))
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_5"))
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_6"))
        self.setInput.append(self.ui.findChild(QLineEdit, "lineEdit_7"))
        self.b_save = self.ui.findChild(QPushButton, "b_save")
        self.b_cancel = self.ui.findChild(QPushButton, "b_cancel")
        self.b_save.clicked.connect(self.save)
        self.b_cancel.clicked.connect(self.cancel)
        self.setValidation()
        self.setLineEdit()

    def setLineEdit(self):
        if self.idEmployee != 0:
            text = []
            #getText from database search
            for i in range(len(self.setInput)):
                self.setInput[i].setText(text[i])

        self.setInput[5].textChanged.connect(self.check_state)
        self.setInput[5].textChanged.emit(self.setInput[5].text())

    def setValidation(self):
        checkInt = QDoubleValidator()
        self.setInput[5].setValidator(checkInt)

    def check_state(self, *args, **kwargs):
        if self.setInput[3].text() == self.setInput[4].text():
            color = '#c4df9b'
            self.setInput[4].setStyleSheet('QLineEdit { background-color: %s }' % color)
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(), 0)[0]
            if state == QValidator.Acceptable:
                color = '#c4df9b'  # green
            elif state == QValidator.Intermediate:
                color = '#fff79a'  # yellow
            else:
                color = '#f6989d'  # red
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            color = '#f6989d'
            self.setInput[4].setStyleSheet('QLineEdit { background-color: %s }' % color)

    def check_password(self, *args, **kwargs):
        pass

    def onTextChange(self, text):
        regExp = QRegExp()
        regExp.setPattern("[^0-9]*")
        m_correctText = ""
        if regExp.exactMatch(text):
            m_correctText = text
            QToolTip.hideText()

        else:
            point = QPoint(self.l.geometry().left(), self.l.geometry().bottom())
            self.l.setText(m_correctText)
            QToolTip.showText(point, "Cannot enter number..")

    def save(self):
        text = []
        for lineEdit in self.setInput:
            text.append(lineEdit.text())
        try:
            sql_insert = """INSERT INTO users VALUES(%s, %s, %s)"""
            sql_insert1 ="""INSERT INTO doctor VALUES(%s, %s, %s, %s, %s)"""
            conn_string = "host='localhost' dbname='postgres' user='postgres' password='4141'"
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute(sql_insert,(text[0], text[1], text[2],))
            cursor.close()

            cursor = conn.cursor()
            cursor.execute(sql_insert1, (text[3], text[4], text[5], text[6], text[7],))
            cursor.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            conn.close()
        self.close()

    def cancel(self):
        dialog = ConfirmMsgClass.ConfirmYesNo()
        if dialog.ans == True:
            print("Discard")
            self.close()
        else:
            print("Cancel")

def main():
    app = QApplication(sys.argv)
    win = EditOrNewEmployeeDialog('new')
    print(win.ans)
    win.exec_()

if __name__ == "__main__":
    main()