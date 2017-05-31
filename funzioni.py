import sys, os, datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import *
from PyQt4 import QtGui,uic
from qgis.gui import QgisInterface 
from PyQt4 import QtSql


def salva(dialog):
    #msgBox = QMessageBox()
    #msgBox.setText("Salvataggio dati")
    #msgBox.exec_()
    global hostName, databaseName, userName, passWord
  
    tabWidget=dialog.findChild(QTabWidget,"tabWidget")
    gid=dialog.findChild(QLineEdit,"gid").text()  
    
    db = QtSql.QSqlDatabase.addDatabase('QPSQL')

    db.setHostName(hostName)
    db.setPort(5432)
    db.setDatabaseName(databaseName)
    db.setUserName(userName)
    db.setPassword(passWord)
    ok = db.open()
    if ok:    
      for t in range(tabWidget.count()):
        widget=tabWidget.widget(t)
        id_univoco=widget.findChild(QLineEdit,"id_univoco").text()
        id_classe=widget.findChild(QLineEdit,"id_classe").text()
        id_giada=widget.findChild(QLineEdit,"id_giada").text()
        #classe=widget.findChild(QLineEdit,"classe").text()
        #sottoclasse=widget.findChild(QLineEdit,"sottoclasse").text()
        
        if id_univoco !="" and id_classe !="":
          query = QtSql.QSqlQuery(db)
          sql="delete from ra_nodi_classi where id_univoco="+id_univoco
          query.exec_(sql)
          
          sql="insert into ra_nodi_classi (gid,id_classe,id_giada,id_univoco) values ("+gid+","+id_classe+","+id_giada+","+id_univoco+")"
          query.exec_(sql)
          
          msgBox = QMessageBox()
          msgBox.setText("Salvataggio effettuato per "+id_univoco)
          msgBox.exec_() 
        
        elif id_classe !="":
          if id_giada!="":
            sql="insert into ra_nodi_classi (gid,id_classe,id_giada) values ("+gid+","+id_classe+","+id_giada+")"
          else:
            sql="insert into ra_nodi_classi (gid,id_classe) values ("+gid+","+id_classe+")"
            
          query.exec_(sql)
              
          msgBox = QMessageBox()
          msgBox.setText("Salvataggio effettuato per nuovo")
          msgBox.exec_()  



def bottoneCancella(self,id_univoco,w,t):
  global hostName, databaseName, userName, passWord
  msgBox = QMessageBox.question(None, "Eliminazione", "Si vuole cancellare l'associazione "+id_univoco.text()+"?",QMessageBox.Yes, QMessageBox.No)
  
  if msgBox == QMessageBox.Yes:
    db = QtSql.QSqlDatabase.addDatabase('QPSQL')

    db.setHostName(hostName)
    db.setPort(5432)
    db.setDatabaseName(databaseName)
    db.setUserName(userName)
    db.setPassword(passWord)
    ok = db.open()
    if ok:       
      query = QtSql.QSqlQuery(db)
      sql="delete from ra_nodi_classi where id_univoco="+id_univoco.text()
      query.exec_(sql)
      w.removeTab(t-1)


def classeScelta(index,id_classe):
    id_classe.setText(str(index))


  

    