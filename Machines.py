#import threading,thread
from PyQt4 import QtGui, QtCore

class Machines(QtCore.QThread):
    def __init__(self,name,capacity):
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
    
    def add_ServiceTime(self,service_time):
        self.status_time=service_time
        #print self.status_time
    def get_current_status(self):
        return self.status_time
    
    def set_ending_times(self,end_time):
        
        self.last_end_time.append(end_time)
        
        if self.last_end_time>1:
            self.ending_time=max(self.last_end_time)
        else:
            self.ending_time=self.last_end_time[0]
        return self.ending_time
            
    def check_availability(self,new_item_time,item):
        if self.ending_time >= new_item_time:
            print "You must wait! item: ",item
            print "this is the queue: ",self.current_waiting
            return False
        else:
            if item in self.current_waiting:
                self.current_waiting.remove(item)
            return True
        
    def add_to_queue(self,item):
        self.current_waiting.append(item)
        #print self.current_waiting
            
class Horno(Machines):
    def __init__(self, total_tons,*args, **kwargs):
        self.total_tons=total_tons
        self.current_tons=0
        super(Horno,self).__init__(*args, **kwargs)
        #self.sema=threading.BoundedSemaphore(capacity)
        self.list_times=[]
        
    # def add_tons(self,ton):
    #     if self.current_tons>self.total_tons:
    #         return False
    #     self.current_tons+=ton

    # def exit_horno(self,ton):
    #     self.current_tons-=ton
        
    # def get_tons(self):
    #     return self.current_tons        
    
    # def get_current_status(self):
    #     return max(self.list_times)
    
    # def add_ServiceTime(self,service_time):
    #     self.list_times.append(service_time)
        
