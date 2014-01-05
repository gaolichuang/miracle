'''
Created on 2014.1.1

@author: gaolichuang
'''
from oslo.config import cfg
from eventlet import greenthread
from miracle.common.manager import periodic_task
from miracle.common.base import log as logging

CONF = cfg.CONF
CONF.import_opt('periodic_report_tasks_interval', 'miracle.common.service.service')

LOG = logging.getLogger(__name__)

class Manager(periodic_task.PeriodicTasks):
    '''
    Manager is the real worker, you can add your own thread(RUN),and periodic job
    to Manager.
    Manager contain the same context
    '''
    def __init__(self):
        pass

    def periodic_report_tasks(self, service, raise_on_error=False):
        '''fix interval task, you can rewrite run_periodic_report_tasks fuction'''
        try:
            self.run_periodic_report_tasks(service)
        except Exception as e:
            if raise_on_error:
                raise
            LOG.exception(_("Error during %(full_task_name)s: %(e)s"),
                              locals())

    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval.
        you must return float value"""
        return self.run_periodic_tasks(context, raise_on_error=raise_on_error)        


    '''===========Functions blow you can or should rewrite==========='''
    def run_periodic_report_tasks(self,service):
        '''Fix interval report task, if you want, rewrite it 
        Child classes should override this method.
        '''
        pass

    def Run(self, context, *args, **kwargs):
        ''' Run thread, you can add logic task in your while true
        Attention use greenthread.sleep(seconds) to allow switching
        greenthreads
        Child classes should override this method.
        '''
        while True:
            # Atention:Allow switching between greenthreads.
            greenthread.sleep(3) #greenthread.sleep(seconds)

    def pre_start_hook(self):
        """Hook to provide the manager the ability to do additional
        start-up work before any RPC queues/consumers are created. This is
        called after other initialization has succeeded and a service
        record is created.

        Child classes should override this method.
        """
        pass

    def post_start_hook(self):
        """Hook to provide the manager the ability to do additional
        start-up work immediately after a service creates RPC consumers
        and starts 'running'.

        Child classes should override this method.
        """
        pass
