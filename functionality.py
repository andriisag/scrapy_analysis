import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt6.uic import loadUi
from PyQt6 import QtCore, QtGui, QtWidgets

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        self.pushButton.clicked.connect(self.browsefiles)
        self.comboBox.activated.connect(self.combo_adap)
        self.pushButton_2.clicked.connect(self.popular_reviews)
        self.pushButton_3.clicked.connect(self.frequent)
        self.pushButton_4.clicked.connect(self.sentinment)

    def browsefiles(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select .csv file",
            QtCore.QDir.currentPath(),
            "Configure File (*.csv)"
        )
        self.lineEdit_2.setText(fname[0])
    def combo_adap(self):
        _translate = QtCore.QCoreApplication.translate
        if(self.comboBox.currentText() == "reviews"):
         self.pushButton_2.setText(_translate("MainWindow", "Popular reviews"))
         self.pushButton_3.setText(_translate("MainWindow", "Frequent words"))
         self.pushButton_4.setText(_translate("MainWindow", "Reviews sentinment"))
        else:
         self.pushButton_2.setText(_translate("MainWindow", "Popular products"))
         self.pushButton_3.setText(_translate("MainWindow", "Frequent words"))
         self.pushButton_4.setText(_translate("MainWindow", "Products sentinment"))
    def popular_reviews(self):
      path = self.lineEdit_2.text()
      if (path!='' and path !="Error"):
       if(self.comboBox.currentText() == "reviews"): 
        from analysis import popular_reviews
        popular_reviews(path)
       else:
          from analysis import popular_products
          popular_products(path)
      else:
         self.lineEdit_2.setText("Error")

    

    def frequent(self):
      path = self.lineEdit_2.text()
      if (path!='' and path !="Error"):
       if(self.comboBox.currentText() == "reviews"): 
          from analysis import frequent_in_reviews
          frequent_in_reviews(path)
       else:
          from analysis import frequent_in_products
          frequent_in_products(path)
      else:
         self.lineEdit_2.setText("Error")

          
    def sentinment(self):
      path = self.lineEdit_2.text()
      if (path!='' and path !="Error"):
       if(self.comboBox.currentText() == "reviews"): 
          from analysis import reviews_sentinment
          reviews_sentinment(path)
       else:
          from analysis import products_sentinment
          products_sentinment(path)
      else:
          self.lineEdit_2.setText("Error")

       
    
          
    

app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(650)
widget.setFixedHeight(370)
widget.show()
sys.exit(app.exec())