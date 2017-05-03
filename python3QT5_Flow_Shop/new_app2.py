#!/usr/bin/env python

import time, random
from random import shuffle
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QMutex
from Machines import Machines,Horno
from random import randint
from Items import Item,get_val_tons,get_sequence,get_total_times
from config_vars import *
import csv
from Publisher import Publisher

class Dispatcher(QtCore.QThread):
    def __init__(self,horno_name,pub,parent=None):
        super(Dispatcher, self).__init__(parent)
        self.pub=pub
        self.horno_name=horno_name
        self.worker_thread = QtCore.QThread()
        self.delay = 1000
        
    def run(self):
        while True:
            self.check_machines()
            new_seq=get_sequence()
            print("SEQUENCE FROM APP: ",new_seq)
            if not new_seq:
                print("TOTAL_TIMES: ",get_total_times())
                return
            QtCore.QThread.msleep(self.delay)
            
    def check_machines(self):
        """thread worker function"""
        #print name,":",machines[name].get_current_status()
        #sys.stdout.write(str(name) + str(machines[name].get_current_status()) + '\n')
        total_tons=machines[self.horno_name].total_tons
        tons=get_val_tons(self.horno_name) #machines[self.horno_name].get_tons()
        print(self.horno_name+" ",tons,"vs",total_tons)
        if total_tons>=tons:
            self.pub.dispatch("Change",(True,self.horno_name))
        else:
            self.pub.dispatch("Change",(False,self.horno_name))
            
class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        #self.filename=filename
        self.mutex = QMutex()
        self.buttonSave = QtWidgets.QPushButton('Save', self)
        self.buttonSave.clicked.connect(self.handleSave)
        self.pub=Publisher(["Change"])
        self.tableWidget = QtWidgets.QTableWidget(self)
        df = pd.read_csv('times_new.csv')
        machines["Cortadora"]=Machines("Cortadora",1)
        machines["Horno1"]=Horno(100,"Horno1",5)
        machines["Prensa"]=Machines("Prensa",1)
        machines["Horno2"]=Horno(100,"Horno2",5)
        machines["Roladora"]=Machines("Roladora",1)
        machines["Horno3"]=Horno(100,"Horno3",5)
        num_orders=len(df.groupby("family"))
        order_ids=df["family"].unique()
        for id_order in order_ids:
            products=df[df["family"]==id_order]
            longitud=len(products)
            for id_item in range(longitud):
                name=(id_order,id_item)
                diameter=random.randint(3,5)
                temp=random.randint(3,5)
                time_freezing=random.randint(6,15)
                list_times=products.iloc[[id_item]]
                tons=20
                if id_order not in orders:
                    orders[id_order]=[]
                orders[id_order].append(Item(name,diameter,temp,time_freezing,list_times,tons,self.pub,self))
                
        seq_orders=[i for i in range(len(orders))]
        shuffle(seq_orders)

        for order_id in seq_orders: #for every order id, get sub indixes of items
            print(order_id)
            items_sub=[i for i in range(len(orders[order_id]))]
            shuffle(items_sub)
            for item_id in items_sub:
                sequence.append((order_id,item_id))
            
        print(sequence)
        print(machines)
        num_col=1
        self.tableWidget.setRowCount(num_col)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.signalMapper = QtCore.QSignalMapper(self)  
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        
        
        self.values = ["Job","Family","Operation", "Machine", "Start" ,"End","Day"]
        self.tableWidget.setHorizontalHeaderLabels(self.values)
        Hornos=["Horno1","Horno2","Horno3"]
        #threads = []
        for i,name in enumerate(Hornos):
            disp=Dispatcher(name,self.pub,self)
            disp.start()
       
        counter=0
        #signals=["machineChanged","startChanged","endChanged","operationChanged"]
        
        for order_id,item_id in sequence:
            print("Sequence: ",order_id,item_id)
            current_thread=orders[order_id][item_id]
            self.signalMapper.setMapping(current_thread, counter)
            current_thread.machineChanged.connect(self.signalMapper.map)
            counter+=1
            #self.pub.register("Change",orders[order_id][item_id])
            current_thread.start()
        
            
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.tableWidget, 0, 0)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, number):
        #if self.signalMapper.mapping(number).mutex.tryLock():
        #values = ["Job","Family","Operation", "Machine", "Start" ,"End"]
        job_info=self.signalMapper.mapping(number)
        #self.mutex.lock()
        
        info=[job_info.name[0],job_info.name[1],job_info.operation,job_info.c_name,job_info.start_time,job_info.end_time,
              job_info.day]
        rowPosition = self.tableWidget.rowCount()
        for index,value in enumerate(info):
            item1 = QtWidgets.QTableWidgetItem()
            item1.setText("{0}".format(value))
            self.tableWidget.setItem(rowPosition-1,index,item1)
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.scrollToItem(item1,QtWidgets.QAbstractItemView.PositionAtTop)
        #self.mutex.unlock()
        #thread.sleep(2)
    def handleSave(self):
        path = "result.csv" #QtWidgets.QFileDialog.getSaveFileName(
            #self, 'Save File', '', 'CSV(*.csv)')
        if path:
            with open(str(path), 'w') as stream:
                writer = csv.writer(stream)
                for row in range(self.tableWidget.rowCount()):
                    rowdata = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            rowdata.append(
                                str(item.text()))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(666, 111)
    main.show()

    sys.exit(app.exec_())
