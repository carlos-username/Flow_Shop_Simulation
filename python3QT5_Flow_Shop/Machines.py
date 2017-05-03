#import threading,thread
from PyQt5 import QtGui, QtCore
#from Queue import Queue

class Machines(QtCore.QThread):
    def __init__(self,name,capacity,*args, **kwargs):
        super(Machines, self).__init__(*args,**kwargs)

       # threading.Thread.__init__(self)
        self.availability=True
        self.name=name
        self.capacity=capacity
        #self.capacity=capacity
        self.sema=QtCore.QSemaphore(self.capacity)
        self.current_waiting=[]
        self.last_end_time=[]
        self.ending_time=0
        self.status_time=0
        
        #self.queue=Queue
        
    def add_ServiceTime(self,service_time):
        self.status_time=service_time
        #print self.status_time
    def get_current_status(self):
        return self.status_time

    def add_to_queue(self,item):
        self.current_waiting.append(item)
        #print self.current_waiting

class Horno(Machines):
    def __init__(self, total_tons,*args, **kwargs):
        super(Horno,self).__init__(*args, **kwargs)
        self.total_tons=total_tons
        self.current_tons=0

        #self.sema=threading.BoundedSemaphore(capacity)
        self.list_times=[]
        self.list_names=[]
        self.list_temper=[]

    def add_tons(self,ton):
        if self.current_tons>self.total_tons:
            return False
        self.current_tons+=ton
        return True

    def validate_tons(self):
        if self.current_tons>self.total_tons:
            return False
        else:
            return True
    
    def exit_horno(self,ton,time,temp):
        #print("ACHTUNG!!!!!")
        #print("TONS ITEM: ",inst.tons," NAME: ",inst.name)
        print("tons from piece: ",ton)
        print ("current_tons: ",self.current_tons)
        self.current_tons-=ton
        print("TONELADAS ACTUALES: ",self.current_tons)
        self.list_times.remove(time)
        self.list_temper.remove(temp)
        #self.list_names.remove(name)

    def get_tons(self):
        return self.current_tons        
    
    def get_current_temp(self,temp):
        if self.list_temper:
            print("TEMP_ITEM: ",temp," vs ","LIST_TEMP: ",self.list_temper)
            for t in self.list_temper:
                if temp < t:
                    return False
        return True

    def get_current_status(self,time):
        if self.list_times:
            print("TIME_ITEM: ",time," vs ","LIST_TIME: ",self.list_times)
            for tm in self.list_times:
                if time < tm:
                    return False
        return True
    
    def add_ServiceTime(self,service_time):
        self.list_times.append(service_time)
    
    def add_Temperature(self,temperature):
        self.list_temper.append(temperature)    

    def add_piece_name(self,name):
        self.list_names.append(name)
    
