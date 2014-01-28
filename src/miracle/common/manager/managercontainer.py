'''
Created on 2014.1.1

@author: gaolichuang
'''
import random
from oslo.config import cfg
from eventlet import greenthread
from miracle.common.manager import periodic_task
from miracle.common.manager import manager
from miracle.common.utils.gettextutils import _  # noqa
from miracle.common.base import log as logging

CONF = cfg.CONF
CONF.import_opt('periodic_report_tasks_interval', 'miracle.common.service.service')

LOG = logging.getLogger(__name__)

class ManagerContainer(periodic_task.PeriodicTasks):
    '''
    ManagerContainer can contain many Manager
    '''
    def __init__(self, manager = None, number = 0):
        self._input_queue = None
        self._output_queue = None
        self.managers = []
        self.number = number
        LOG.info(_("=====================Start %s number:%s===================="% (manager,self.number)))
        i = 0
        while i < self.number:
            _manager = manager()
            self.managers.append(_manager)
            LOG.info(_("Start Manager in Container: %(mname)s id:%(m_id)s"),
                        {'mname':_manager.__class__.__name__,'m_id':_manager.m_id})
            i = i + 1
        LOG.info(_(60*"="))
        self.m_name = 'NA'
        if len(self.managers) != 0:
            self.m_name = self.managers[0].__class__.__name__
        
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
            for manager in self.managers:
                manager.run_periodic_report_tasks(service)
        except Exception as e:
            if raise_on_error:
                raise
            LOG.exception(_("Error during  %(e)s"),
                              locals())

    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval.
        you must return float value"""
        return self.run_periodic_tasks(context, raise_on_error=raise_on_error)        
    def Run(self, context, *args, **kwargs):
        ''' put inputqueue output queue to manager'''
        for manager in self.managers:
            '''TODO:XXX input queue info always get by the first manger?!?'''
            manager.m_input_queue = self._input_queue
            manager.m_output_queue = self._output_queue
            context.tg.add_thread(manager.Run, context, *args, **kwargs)

    def pre_start_hook(self,context):
        for manager in self.managers:
            LOG.info(_("%(cname)s id:%(m_id)s Pre_start_hook"),
                     {'cname':manager.__class__.__name__,'m_id':manager.m_id})
            manager.pre_start_hook()

    def post_start_hook(self,context):
        for manager in self.managers:
            LOG.info(_("%(cname)s id:%(m_id)s Post_start_hook"),
                     {'cname':manager.__class__.__name__,'m_id':manager.m_id})
            manager.post_start_hook()
        ''' start multi fetchers'''
        if context.periodic_enable:
            if context.periodic_fuzzy_delay:
                initial_delay = random.randint(0, context.periodic_fuzzy_delay)
            else:
                initial_delay = None
                for manager in self.managers:
                    ''' start periodic tasks'''
                    context.tg.add_dynamic_timer(manager.periodic_tasks,
                                            initial_delay=initial_delay,
                                            periodic_interval_max=
                                                context.periodic_interval_max,
                                            context = context)
