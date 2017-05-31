# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        modulo_nodi.py
# Purpose:
#
# Author:      Francesco Marucci
#
# Created:     05-10-2017
# Copyright:   (c) Tecnograph 2017
# Licence:     <GPL>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys, os, datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import *
from PyQt4 import QtGui,uic
from qgis.gui import QgisInterface 
from PyQt4 import QtSql
import funzioni

myDialog = None
myfeatureid = None
curLayer = None

hostName = None
databaseName = None
userName = None
passWord= None

sys.path.append(QgsProject.instance().homePath())

def formOpen(dialog,layerid,featureid):
    #definisco le variabili globali
    global myDialog, myfeatureid, curLayer
    global hostName, databaseName, userName, passWord
    
    try:
      provider = layerid.dataProvider()
      if provider.name() == 'postgres':
        uri = QgsDataSourceURI(provider.dataSourceUri())
        hostName=uri.host()
        databaseName=uri.database()
        userName=uri.username()
        passWord=uri.password()
      
    except Exception, e:
      msgBox = QMessageBox()
      msgBox.setText(repr(e))
      msgBox.exec_()      
    
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    try:
      buttonBox=myDialog.findChild(QDialogButtonBox,"buttonBox")
      buttonBox.accepted.connect(lambda: funzioni.salva(myDialog))
    except Exception, e:
      msgBox = QMessageBox()
      msgBox.setText(repr(e))
      msgBox.exec_()
    
    gid=myDialog.findChild(QLineEdit,"gid")
    gid.setStyleSheet('''
        QLineEdit {
            border: 1px solid rgb(202, 201, 200);
            color: rgb(60, 60, 60);
            background-color: rgb(224, 221, 219);
            font-weight: bold;
        }
    ''')    
    
    db = QtSql.QSqlDatabase.addDatabase('QPSQL')

    db.setHostName(hostName)
    db.setPort(5432)
    db.setDatabaseName(databaseName)
    db.setUserName(userName)
    db.setPassword(passWord)

    tabWidget=myDialog.findChild(QTabWidget,"tabWidget")
    labOggetti=myDialog.findChild(QLabel,"oggetti")
    ok = db.open()
    if ok:
      query = QtSql.QSqlQuery(db)
      
      listaClassi=[]
      listaIdClassi=[]
      sql="select id, case when subclasse2 is null then subclasse1||' ('||classe||')' else subclasse2 ||' ('||classe||' - '||subclasse1||')' end as nome from ra_classi where id_tipo_oggetto is not null and classe is not null and subclasse1 is not null and id_tipo_oggetto <> 'Non definito' order by classe, subclasse1"
      query.exec_(sql)
      idxClasse=0
      while query.next():
        listaIdClassi.append(query.value(0))
        listaClassi.append(query.value(1))

        
      
      
      if not query.exec_('select gid, id_univoco, id_classe, ra_classi.classe, ra_classi.subclasse1,ra_nodi_classi.id_giada from ra_nodi_classi left join ra_classi on ra_nodi_classi.id_classe=ra_classi.id where gid='+str(myfeatureid.id())):
        raise RuntimeError('fallito')
      else:
        yy=0
        try:
          while query.next():
            yy+=1
            tab = QWidget(tabWidget)
            tabWidget.addTab(tab, query.value(3))

            layout = QFormLayout()
            
            id_univoco=QLineEdit(str(query.value(1)))
            id_univoco.setObjectName("id_univoco")
            layout.addRow("id_univoco",id_univoco)
            id_univoco.setEnabled(False)
            
            id_classe=QLineEdit(str(query.value(2)))
            id_classe.setObjectName("id_classe")
            layout.addRow("id_classe",id_classe)
            classeIdx=listaIdClassi.index(query.value(2))
            id_classe.setEnabled(False)
            
            #classe=QLineEdit(query.value(3))
            #classe.setObjectName("classe")
            #layout.addRow("classe",classe)
            
            #sottoclasse=QLineEdit(query.value(4))
            #sottoclasse.setObjectName("sottoclasse")
            #layout.addRow("sottoclasse",sottoclasse)
            
            comboclasse=QComboBox()
            comboclasse.setObjectName("comboclasse")
            comboclasse.addItems(listaClassi)
            layout.addRow("comboclasse",comboclasse)
            comboclasse.setCurrentIndex(classeIdx)
            comboclasse.currentIndexChanged[int].connect(lambda ind,target=id_classe: funzioni.classeScelta(listaIdClassi[ind],target))
            
            id_giada=QLineEdit(str(query.value(5)))
            id_giada.setObjectName("id_giada")
            layout.addRow("id_giada",id_giada)
           
            bottoneCancella=QPushButton("Elimina")
            bottoneCancella.setObjectName("bottoneCancella")
            bottoneCancella.clicked.connect(lambda self, id=id_univoco,w=tabWidget,t=yy: funzioni.bottoneCancella(self,id,w,t))
            layout.addRow(bottoneCancella)
            
            tab.setLayout(layout)
            
          labOggetti.setText("Oggetti associati: "+str(yy))
          
          tab = QWidget(tabWidget)
          tabWidget.addTab(tab, " + ")
          layout = QFormLayout()
          
          id_univoco=QLineEdit("")
          id_univoco.setObjectName("id_univoco")
          layout.addRow("id_univoco",id_univoco)
          id_univoco.setEnabled(False)
            
          id_classe=QLineEdit()
          id_classe.setObjectName("id_classe")
          layout.addRow("id_classe",id_classe)
          id_classe.setEnabled(False)
          
          comboclasse=QComboBox()
          comboclasse.setObjectName("comboclasse")
          comboclasse.addItems(listaClassi)
          comboclasse.currentIndexChanged[int].connect(lambda ind,target=id_classe: funzioni.classeScelta(listaIdClassi[ind],target))
          layout.addRow("comboclasse",comboclasse)
            
          id_giada=QLineEdit()
          id_giada.setObjectName("id_giada")
          layout.addRow("id_giada",id_giada)
          tab.setLayout(layout)
          
                
        except Exception, e:
          msgBox = QMessageBox()
          msgBox.setText(repr(e))
          msgBox.exec_()
          #print repr(e)

        #msgBox = QMessageBox()
        #msgBox.setText(str(yy))
        #msgBox.exec_()




    
    # assegno gli oggetti della combo
    #TblIndagini= myDialog.findChild(QTableWidget,"tableIndagini")
    #LblIdSito= myDialog.findChild(QLineEdit,"pkey_spu")
    #LblQuota= myDialog.findChild(QLineEdit,"quota_slm")
    #datDataSito= myDialog.findChild(QDateEdit,"data_sito")
    
    
    #mette la data di default ad oggi quando e null
    #if datDataSito.date().toString("dd/MM/yyyy")==QDate(1900,1,1).toString("dd/MM/yyyy"):
    #    datDataSito.setDateTime(datetime.datetime.now())
        
    #collego i segnali
    #LblQuota.textChanged.connect(lambda: mzs.validaQuota(LblQuota))


