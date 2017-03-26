#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time, random
from random import shuffle
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QMutex
from Machines import Machines,Horno
from random import randint
from Items import Item
from config_vars import *

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        
        self.tableWidget = QtGui.QTableWidget(self)
        df = pd.read_csv('times_new.csv')
        
        machines["Cortadora"]=Machines("Cortadora",1)
        machines["Horno1"]=Horno(400,"Horno1",5)
        machines["Prensa"]=Machines("Prensa",1)
        machines["Horno2"]=Horno(400,"Horno2",5)
        machines["Roladora"]=Machines("Roladora",1)
        machines["Horno3"]=Horno(400,"Horno3",5)
        num_orders=len(df.groupby("family"))
        order_ids=df["family"].unique()
        for id_order in order_ids:
            products=df[df["family"]==id_order]
            longitud=len(products)
            #print products
            for id_item in xrange(longitud):
                name=(id_order,id_item)
                diameter=random.randint(1,3)
                temp=random.randint(3,5)
                time_freezing=random.randint(6,15)
                list_times=products.iloc[[id_item]]
                tons=100
                #print list_times
                if id_order not in orders:
                    orders[id_order]=[]
                orders[id_order].append(Item(name,diameter,temp,time_freezing,list_times,tons,self))

        seq_orders=[i for i in xrange(len(orders))]
        shuffle(seq_orders)

        for order_id in seq_orders: #for every order id, get sub indixes of items
            print order_id
            items_sub=[i for i in xrange(len(orders[order_id]))]
            shuffle(items_sub)
            for item_id in items_sub:
                sequence.append((order_id,item_id))
            
        print sequence
        print machines
        num_col=1
        self.tableWidget.setRowCount(num_col)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.signalMapper = QtCore.QSignalMapper(self)  
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        
        global values
        
        values = ["Job","Family","Operation", "Machine", "Start" ,"End"]
        self.tableWidget.setHorizontalHeaderLabels(values)
        counter=0
        signals=["machineChanged","startChanged","endChanged","operationChanged"]
        for order_id,item_id in sequence:
            print "Sequence: ",order_id,item_id
            current_thread=orders[order_id][item_id]
            #print current_thread
            self.signalMapper.setMapping(current_thread, counter)
            #current_thread.operationChanged.connect(self.signalMapper.map)
            current_thread.machineChanged.connect(self.signalMapper.map)
            #current_thread.startChanged.connect(self.signalMapper.map)
            #current_thread.endChanged.connect(self.signalMapper.map)
            counter+=1
            current_thread.start()
            
            
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.addWidget(self.tableWidget, 0, 0)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, number):
        #if self.signalMapper.mapping(number).mutex.tryLock():
        #values = ["Job","Family","Operation", "Machine", "Start" ,"End"]
        job_info=self.signalMapper.mapping(number)
        info=[job_info.name[0],job_info.name[1],job_info.operation,job_info.c_machine,job_info.start_time,job_info.end_time]
        rowPosition = self.tableWidget.rowCount()
        for index,value in enumerate(info):
            item1 = QtGui.QTableWidgetItem()
            item1.setText("{0}".format(value))
            self.tableWidget.setItem(rowPosition-1,index,item1)
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.scrollToItem(item1,QtGui.QAbstractItemView.PositionAtTop)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(666, 111)
    main.show()

    sys.exit(app.exec_())
