'''
Created on 2014.1.1

@author: gaolichuang
'''
from oslo.config import cfg
from eventlet import greenthread
from miracle.common.manager import periodic_task
from miracle.common.manager import manager
from miracle.common.base import log as logging

CONF = cfg.CONF
CONF.import_opt('periodic_report_tasks_interval', 'miracle.common.service.service')

LOG = logging.getLogger(__name__)

class ManagerContainer(periodic_task.PeriodicTasks):
    '''
    ManagerContainer can contain many Manager
    '''
    def __init__(self, manager = None):
        self._input_queue = None
        self._output_queue = None
        self.manager = manager

    @property
    def input_queue(self):
        return self._input_queue
    @input_queue.setter
    def input_queue(self,queue):
        self._input_queue = queue
    @property
    def output_queue(self):
        return self._output_queue
    @output_queue.setter
    def output_queue(self,queue):
        self._output_queue = queue

    def periodic_report_tasks(self, service, raise_on_error=False):
        '''fix interval task, you can rewrite run_periodic_report_tasks fuction'''
        try:
            self.manager.run_periodic_report_tasks(service)
        except Exception as e:
            if raise_on_error:
                raise
            LOG.exception(_("Error during %(full_task_name)s: %(e)s"),
                              locals())

    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval.
        you must return float value"""
        return self.manager.run_periodic_tasks(context, raise_on_error=raise_on_error)        


    def run_periodic_report_tasks(self,service):
        '''Fix interval report task, if you want, rewrite it 
        Child classes should override this method.
        '''
        self.manager.run_periodic_report_tasks(service)

    def Run(self, context, *args, **kwargs):
        ''' Run thread, you can add logic task in your while true
        Attention use greenthread.sleep(seconds) to allow switching
        greenthreads
        Child classes should override this method.
        '''
        ''' put inputqueue output queue to manager'''
        self.manager.inputqueue = self._input_queue
        self.manager.outputqueue = self._output_queue
        self.manager.Run(context, *args, **kwargs)

    def pre_start_hook(self,context):
        """Hook to provide the manager the ability to do additional
        start-up work before any RPC queues/consumers are created. This is
        called after other initialization has succeeded and a service
        record is created.

        Child classes should override this method.
        """
        self.manager.pre_start_hook()

    def post_start_hook(self,context):
        """Hook to provide the manager the ability to do additional
        start-up work immediately after a service creates RPC consumers
        and starts 'running'.

        Child classes should override this method.
        """
        self.manager.post_start_hook()
