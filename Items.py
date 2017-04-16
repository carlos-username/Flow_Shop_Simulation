import threading,thread
from random import randint
import random
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QMutex,QWaitCondition
#from Machines import Machines
from config_vars import *
import sys
from collections import OrderedDict
#global queue_wating
class Item(QtCore.QThread):
    machineChanged = QtCore.pyqtSignal(object)
    startChanged = QtCore.pyqtSignal(object)
    endChanged = QtCore.pyqtSignal(object)
    operationChanged = QtCore.pyqtSignal(object)
    statusChanged = QtCore.pyqtSignal(object)
    #conta_pChanged=QtCore.pyqtSignal(object)
    def __init__(self,name,diameter,temp,time_freezing,service_times,tons,publisher,parent=None):
        #threading.Thread.__init__(self)
        super(Item, self).__init__(parent)
        self.pub=publisher
        self.tons=tons
        #self.lock=QtCore.QThread.__init__(self)
        #self.c_machine = None
        self.delay = 3000
        self.diameter=diameter
        self.temp=temp
        self.time_freezing=time_freezing
        self.total_diameter=self.time_freezing+3
        self.name=name
        self.end_time=0
        self.list_times=service_times.values.tolist()
        self.mutex = QMutex()
        self.conta_machine=0
        self.start_time=0
        self.operation=0
        self.busy=False
        self.list_all_machines=["Cortadora","Horno1","Prensa","Horno2","Roladora","Horno3"]
        self.list_machines=["Cortadora","Prensa","Roladora"]
        self.machine_conta=0
        self.previous_machine=""
        self.current_machine=machines["Cortadora"]
        self.c_name=""
        self.horno_names={"Horno1":False,"Horno2":False,"Horno3":False}
        self.h_name=""

    def update(self,name):
        #if self.busy is False:
        self.horno_names[name]=True
        
        
    def update1(self,name):
        if self.busy:
            try:
                self.pub.unregister("Change",self)
            except:
                pass
            return
        
        if not self.busy:
            self.mutex.lock()
            self.busy=True
            self.mutex.unlock()
            current_horno=machines[name]
            max_time=current_horno.get_current_status()
            service_time=self.list_times[0][self.list_all_machines.index(name)]
            start_time=self.end_time
            end_time=start_time+service_time
            diff_max_time=max_time-end_time
            if current_horno.validate_tons() and diff_max_time<=0:
                print "inside machine!"
                self.current_machine=machines[name]
                print "HORNO!!"
                print self.current_machine.name
                self.current_machine.sema.acquire()
                self.current_machine.add_tons(self.tons)
                self.busy=True
                self.start_time=self.end_time
                self.end_time=self.start_time+service_time
                self.c_name=self.current_machine.name
                self.current_machine.add_ServiceTime(self.end_time)
                self.machineChanged.emit(self.c_name)
                self.startChanged.emit(self.start_time)
                self.endChanged.emit(self.end_time)
                self.operationChanged.emit("0")
                if "Roladora" in self.previous_machine.name:
                    self.machine_conta=2
                else:
                    if self.machine_conta<len(self.list_machines)-1:
                        self.machine_conta+=1
                self.current_machine.exit_horno(self.tons)
                self.current_machine.sema.release()
                curr_machine=machines[self.list_machines[self.machine_conta]]
                self.current_machine=curr_machine
                return
        else:
            self.busy=False

    def run(self):
        while True:
            if self.current_machine is not "":
                if self.current_machine.name in self.list_machines:# and not self.busy:
                    machine_status=self.current_machine.get_current_status()
                    if self.end_time>=machine_status:
                        self.current_machine.sema.acquire()
                        self.busy=True
                        service_time=self.list_times[0][self.list_all_machines.index(self.current_machine.name)]
                        self.start_time = self.end_time
                        self.end_time=self.start_time+service_time
                        self.current_machine.add_ServiceTime(self.end_time)
                        sys.stdout.write(str(self.start_time) + '\n')
                        self.c_name=self.current_machine.name
                        print "CURRENT FROM ABOVE: ",self.c_name
                        self.machineChanged.emit(self.c_name)
                        self.startChanged.emit(self.start_time)
                        self.endChanged.emit(self.end_time)
                        self.operationChanged.emit("0")
                        if "Roladora" in self.current_machine.name:
                            self.diameter+=1
                            if self.diameter>=self.total_diameter:
                                return
                        self.current_machine.sema.release()
                        self.current_machine=""
                        self.busy=False
                        self.previous_machine=self.current_machine
                        self.pub.register("Change",self)
                        self.h_name="Horno"
                    else:
                        self.end_time=self.current_machine.get_current_status()
            if self.h_name not in self.list_machines:
                try:
                    name=[key for key in self.horno_names if self.horno_names[key]==True][0]
                    current_horno=machines[name]
                    max_time=current_horno.get_current_status()
                    service_time=self.list_times[0][self.list_all_machines.index(name)]
                    start_time=self.end_time
                    end_time=start_time+service_time
                    diff_max_time=max_time-end_time
                    if current_horno.validate_tons() and diff_max_time<=0:
                        self.pub.unregister("Change",self)
                        print "inside machine!"
                        self.current_machine=machines[name]
                        print "HORNO!!"
                        print self.current_machine.name
                        self.current_machine.sema.acquire()
                        self.current_machine.add_tons(self.tons)
                        self.busy=True
                        self.start_time=self.end_time
                        self.end_time=self.start_time+service_time
                        self.c_name=self.current_machine.name
                        self.current_machine.add_ServiceTime(self.end_time)
                        self.machineChanged.emit(self.c_name)
                        self.startChanged.emit(self.start_time)
                        self.endChanged.emit(self.end_time)
                        self.operationChanged.emit("0")
                        if "Roladora" in self.previous_machine.name:
                            self.machine_conta=2
                            curr_machine=machines[self.list_machines[self.machine_conta]]
                        else:
                            if self.machine_conta<len(self.list_machines):
                                self.machine_conta+=1
                                curr_machine=machines[self.list_machines[self.machine_conta]]
                        self.current_machine.exit_horno(self.tons)
                        self.current_machine.sema.release()
                        self.busy=False
                        
                        self.current_machine=curr_machine
                        print "Current!!!: ",self.current_machine.name
                except:
                    pass
                    
            QtCore.QThread.msleep(self.delay)
            
            
