from random import randint
import random
from PyQt5 import QtGui, QtCore
from PyQt5.Qt import QMutex,QWaitCondition
from config_vars import *
import sys
from collections import OrderedDict

day_duration=50
total_times=[]

def get_val_tons(name):
    return machines[name].get_tons()

def get_sequence():
    return sequence 

def get_total_times():
    return total_times

class Item(QtCore.QThread):
    machineChanged = QtCore.pyqtSignal(object)
    startChanged = QtCore.pyqtSignal(object)
    endChanged = QtCore.pyqtSignal(object)
    operationChanged = QtCore.pyqtSignal(object)
    statusChanged = QtCore.pyqtSignal(object)
    dayChanged = QtCore.pyqtSignal(object)
    def __init__(self,name,diameter,temp,time_freezing,service_times,tons,publisher,parent=None):
        super(Item, self).__init__(parent)
        self.pub=publisher
        self.tons=tons
        self.delay = 1000
        self.day=1
        self.diameter=diameter
        self.temp=temp
        self.time_freezing=time_freezing
        self.total_diameter=randint(7,10)
        self.name=name
        self.end_time=0
        self.list_times=service_times.values.tolist()
        self.mutex = QMutex()
        self.conta_machine=0
        self.start_time=0
        self.operation=0
        self.list_all_machines=["Cortadora","Horno1","Prensa","Horno2","Roladora","Horno3"]
        self.list_machines=["Cortadora","Prensa","Roladora"]
        self.machine_conta=0
        self.previous_machine=machines["Cortadora"]
        self.current_machine=machines["Cortadora"]
        self.horno_names={"Horno1":False,"Horno2":False,"Horno3":False}
        self.h_name=True        
        self.running=True
        self.temp_time=0

    def update(self,name):
        self.horno_names[name[1]]=name[0]
        
    def run(self):
        if not self.running:
            return
        
        while self.running:
            if self.h_name:
                if self.current_machine.name in self.list_machines:# and not self.busy:
                    machine_status=self.current_machine.get_current_status()
                    if self.end_time>=machine_status:
                        self.current_machine.sema.acquire()
                        service_time=self.list_times[0][self.list_all_machines.index(self.current_machine.name)]
                        self.start_time = self.end_time
                        self.end_time=self.start_time+service_time
                        print("substract_time",(self.end_time-self.temp_time))
                        if (self.end_time-self.temp_time)>=day_duration:
                            self.day+=1
                            self.temp_time=self.end_time
                        self.current_machine.add_ServiceTime(self.end_time)
                        sys.stdout.write(str(self.start_time) + '\n')
                        self.c_name=self.current_machine.name
                        print("CURRENT FROM ABOVE: ",self.c_name)
                        self.operation+=1
                        self.machineChanged.emit(self.c_name)
                        self.startChanged.emit(self.start_time)
                        self.endChanged.emit(self.end_time)
                        self.operationChanged.emit(self.operation)
                        self.dayChanged.emit(self.day)
                        if "Roladora" in self.current_machine.name:
                            print(self.diameter," vs ",self.total_diameter)
                            if self.diameter>=self.total_diameter:
                                print("Finished!",self.name)
                                sequence.remove(self.name)
                                print("SEQUENCE FROM THREAD: ",sequence)
                                total_times.append((self.name,self.end_time))
                                self.running=False
                            self.diameter+=1
                        self.current_machine.sema.release()
                        self.previous_machine=self.current_machine
                        print("registering...")
                        self.pub.register("Change",self)
                        #self.current_machine="Horno1"
                        self.h_name=False
                    else:
                        self.end_time=self.current_machine.get_current_status()
            else:
                print(self.name,self.horno_names)
                if True in list(self.horno_names.values()):
                    name=[key for key in self.horno_names if self.horno_names[key]==True]
                    lg=len(name)-1
                    name=name[randint(0,lg)]
                    current_horno=machines[name]
                    service_time=self.list_times[0][self.list_all_machines.index(name)]
                    start_time=self.end_time
                    end_time=start_time+service_time
                    flag_time=current_horno.get_current_status(end_time)
                    flag_temper=current_horno.get_current_temp(self.temp)
                    print("time: ",flag_time,"-- temperature: ",flag_temper)
                    if current_horno.validate_tons() and flag_time and flag_temper:
                        print("LIST_TIMES: ",current_horno.list_times)
                        print("LIST TEMPERATURES: ",current_horno.list_temper)
                        print(current_horno.name+"inside loop")
                        print("NOMBRE!!!: ",self.name)
                        print("unregistering..")
                        self.pub.unregister("Change",self)
                        print("inside machine!")
                        self.current_machine=machines[name]
                        print("HORNO!!")
                        print(self.current_machine.name)
                        self.current_machine.sema.acquire()
                        self.h_name=False
                        self.current_machine.add_tons(self.tons)
                        self.start_time=self.end_time
                        self.end_time=self.start_time+service_time
                        print("substract_time",(self.end_time-self.temp_time))
                        if (self.end_time-self.temp_time)>=day_duration:
                            self.day+=1
                            self.temp_time=self.end_time
                        self.current_machine.add_ServiceTime(self.end_time)
                        self.current_machine.add_Temperature(self.temp)
                        self.operation+=1
                        self.c_name=self.current_machine.name
                        self.machineChanged.emit(self.c_name)
                        self.startChanged.emit(self.start_time)
                        self.endChanged.emit(self.end_time)
                        self.operationChanged.emit(self.operation)
                        self.dayChanged.emit(self.day)
                        print("CURRENT TONS: ",machines[self.current_machine.name].get_tons())
                        if "Roladora" in self.previous_machine.name:
                            self.machine_conta=2
                            curr_machine=machines[self.list_machines[self.machine_conta]]
                        else:
                            print(len(self.list_machines)-1)
                            if self.machine_conta<len(self.list_machines)-1:
                                self.machine_conta+=1
                                curr_machine=machines[self.list_machines[self.machine_conta]]
                        self.current_machine.sema.release()
                        self.current_machine.exit_horno(self.tons,end_time,self.temp)
                        #self.current_machine.exit_horno(self)
                        self.current_machine=curr_machine
                        self.h_name=True
                        print("Current!!!: ",self.current_machine.name)
            

            QtCore.QThread.msleep(self.delay)
            
            
