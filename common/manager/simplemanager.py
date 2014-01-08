'''
Created on 2014.1.1

@author: gaolichuang
'''

from eventlet import greenthread
from miracle.common.manager import manager as base_manager
from miracle.common.manager import periodic_task

class SimpleManager(base_manager.Manager):
    def __init__(self):
        super(SimpleManager,self).__init__()

    def run_periodic_report_tasks(self,service):
        print('XXXXXX i am in simplemanager run periodic report tasks')

    def Run(self, context, *args, **kwargs):
        while True:
            print('XXXXX i am in simplermanager run %s'%self.manager_id)
            # Allow switching of greenthreads between queries.
            greenthread.sleep(3)

    '''if you use decorator @periodic_task.periodic_task  the task will be run periodicly'''
    @periodic_task.periodic_task
    def function1(self, context):
        print('XXXXX function 1 %s'%self.manager_id)
#    @periodic_task.periodic_task(spacing=8)
    @periodic_task.periodic_task
    def function2(self, context):
        print('XXXXX function 2 %s'%self.manager_id)
