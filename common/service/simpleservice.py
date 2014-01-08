# vim: tabstop=4 shiftwidth=4 softtabstop=4

import random


from oslo.config import cfg

from miracle.common.utils import importutils
from miracle.common.manager import context
from miracle.common.service import service

CONF = cfg.CONF
CONF.import_opt('report_interval', 'miracle.common.service.service')
CONF.import_opt('periodic_enable', 'miracle.common.service.service')
CONF.import_opt('periodic_fuzzy_delay', 'miracle.common.service.service')

class SimpleServer(service.Service):
    ''' simple server, add manager.Run to thread and maintain period task in manager'''
    def __init__(self, manager, report_interval=None,
             periodic_enable=None, periodic_fuzzy_delay=None,
             periodic_interval_max=None, *args, **kwargs):
        super(SimpleServer, self).__init__()
        self.manager_class_name = manager
        manager_class = importutils.import_class(self.manager_class_name)
        self.manager = manager_class(*args, **kwargs)
        self.report_interval = report_interval
        self.periodic_enable = periodic_enable
        self.periodic_fuzzy_delay = periodic_fuzzy_delay
        self.periodic_interval_max = periodic_interval_max
        self.saved_args, self.saved_kwargs = args, kwargs
        self.context = context.get_service_context()
    @classmethod
    def create(cls, manager, report_interval=None, periodic_enable=None,
               periodic_fuzzy_delay=None, periodic_interval_max=None):
        """Instantiates class and passes back application object.

        :param manager: you must assgin an available manager
        :param report_interval: defaults to CONF.report_interval
        :param periodic_enable: defaults to CONF.periodic_enable
        :param periodic_fuzzy_delay: defaults to CONF.periodic_fuzzy_delay
        :param periodic_interval_max: if set, the max time to wait between runs

        """
        if report_interval is None:
            report_interval = CONF.report_interval
        if periodic_enable is None:
            periodic_enable = CONF.periodic_enable
        if periodic_fuzzy_delay is None:
            periodic_fuzzy_delay = CONF.periodic_fuzzy_delay
        service_obj = cls(manager, report_interval=report_interval,
                          periodic_enable=periodic_enable,
                          periodic_fuzzy_delay=periodic_fuzzy_delay,
                          periodic_interval_max=periodic_interval_max)
        return service_obj

    def start(self): 
        self.manager.pre_start_hook()
        '''start manager thread Run'''
        self.tg.add_thread(self.manager.Run, self.context, self.saved_args, self.saved_kwargs)
        
        self.manager.post_start_hook()

        if self.periodic_enable:
            if self.periodic_fuzzy_delay:
                initial_delay = random.randint(0, self.periodic_fuzzy_delay)
            else:
                initial_delay = None
            ''' start periodic tasks'''
            self.tg.add_dynamic_timer(self._periodic_tasks,
                                     initial_delay=initial_delay,
                                     periodic_interval_max=
                                        self.periodic_interval_max)
            if self.report_interval:
                ''' start report state peridic tasks'''
                self.tg.add_timer(self.report_interval, self._report_state,
                                 self.report_interval, self)

    def _report_state(self,service):
        '''FixedIntervalLoopingCall use report_interval'''
        self.manager.periodic_report_tasks(service)

    def _periodic_tasks(self,raise_on_error=False):
        '''DynamicLoopingCall use periodic_interval_max'''
        return self.manager.periodic_tasks(self.context, raise_on_error=raise_on_error)

