import threading,thread
from random import randint
import random
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QMutex,QWaitCondition
#from Machines import Machines
from config_vars import *
import sys

#global queue_wating
class Item(QtCore.QThread):
    machineChanged = QtCore.pyqtSignal(object)
    startChanged = QtCore.pyqtSignal(object)
    endChanged = QtCore.pyqtSignal(object)
    operationChanged = QtCore.pyqtSignal(object)
    statusChanged = QtCore.pyqtSignal(object)
    #conta_pChanged=QtCore.pyqtSignal(object)
    def __init__(self,name,diameter,temp,time_freezing,service_times,tons,parent=None):
        #threading.Thread.__init__(self)
        super(Item, self).__init__(parent)
        self.tons=tons
        self.c_machine = None
        self.delay = 1000
        self.diameter=diameter
        self.temp=temp
        self.time_freezing=time_freezing
        self.total_diameter=self.time_freezing+3
        self.name=name
        #self.total=0
        self.conta_p=0
        #self.num_machines={"Cortadora":[0,False],"Horno1":[1,False],"Prensa":[2,False],
        #                   "Horno2":[3,False],"Roladora":[4,False],"Horno3":[5,False]}
        self.num_machines=["Cortadora","Horno1","Prensa","Horno2","Roladora","Horno3"]
        self.status=0
        self.end_time=0
        self.list_times=service_times.values.tolist()
        self.mutex = QMutex()
        self.conta_machine=0
        self.start_time=0
        self.operation=0
        self.next_machine=0
        
    def run(self):
        while True:
            sys.stdout.write(str(self.name) + str(self.end_time) + '\n')
            current_machine=machines[self.num_machines[self.conta_machine%len(self.num_machines)]]
            #print self.conta_machine
                
            machine_status=current_machine.get_current_status()
            #self.start_time = machine_status
            if self.end_time>=machine_status:
                current_machine.sema.acquire()
                print type(self)
                service_time=self.list_times[0][self.conta_machine%len(self.num_machines)]
                self.start_time = self.end_time
                self.end_time=self.start_time+service_time
                current_machine.add_ServiceTime(self.end_time)
                            
                sys.stdout.write(str(self.start_time) + '\n') 
                self.c_machine = current_machine.name
                
                self.machineChanged.emit(self.c_machine)
                self.startChanged.emit(self.start_time)
                self.endChanged.emit(self.end_time)
                self.operationChanged.emit(self.conta_machine)
                
                self.conta_machine+=1
                
                current_machine.sema.release()
                
            else:
                
                self.start_time=current_machine.get_current_status()
                self.end_time=self.start_time
                current_machine.add_to_queue(self.name)

            QtCore.QThread.msleep(self.delay)
            
