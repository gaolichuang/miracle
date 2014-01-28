# vim: tabstop=4 shiftwidth=4 softtabstop=4

import random
from eventlet import queue

#http://blog.csdn.net/yatere/article/details/6668006
from oslo.config import cfg

from miracle.common.utils import importutils
from miracle.common.manager import context
from miracle.common.service import service
from miracle.common.manager import managercontainer

from miracle.common.utils.gettextutils import _  # noqa
from miracle.common.base import log as logging


muitlservice_opts = [
    cfg.IntOpt('max_queue_size',
               default=100,
               help='max queue size ')
]

CONF = cfg.CONF
CONF.register_opts(muitlservice_opts)

CONF.import_opt('report_interval', 'miracle.common.service.service')
CONF.import_opt('periodic_enable', 'miracle.common.service.service')
CONF.import_opt('periodic_fuzzy_delay', 'miracle.common.service.service')

from cccrawler.manager import manager as crawler_manager

LOG = logging.getLogger(__name__)
'''
Sample:
server = multiservice.MultiServer.create(
           managers = ['cccrawler.scheduler.manager.DummySchedulerManager',
                       'cccrawler.fetcher.managercontainer.FetcherManagerContainer',
                       ('cccrawler.handler.manager.DummyHandlerManager',2)])   # this line means there is 2 DummyHandlerManager
'''
class MultiServer(service.Service):
    ''' simple server, add manager.Run to thread and maintain period task in manager'''
    def __init__(self, managers, report_interval=None,
             periodic_enable=None, periodic_fuzzy_delay=None,
             periodic_interval_max=None, *args, **kwargs):
        super(MultiServer, self).__init__()
        self.managers_class_name = managers
        self.containers = []
        LOG.info(_("=====================Start ManagerContainers ===================="))
        for manager_class_name in self.managers_class_name:
            if isinstance(manager_class_name, tuple):
                manager_class = importutils.import_class(manager_class_name[0])
                manager_class_number = manager_class_name[1]
                LOG.info(_("Start Multi %s  number %s"%(manager_class,manager_class_number)))
            else:
                manager_class = importutils.import_class(manager_class_name)
                manager_class_number = 1
            if issubclass(manager_class, managercontainer.ManagerContainer):
                manager_or_container = manager_class()
                self.containers.append(manager_or_container)
                LOG.info(_("Start ManagerContainer: %(mname)s"), {'mname':manager_or_container.m_name})
            else:
                container = managercontainer.ManagerContainer(manager = manager_class,
                                                              number = manager_class_number)
                self.containers.append(container)
        LOG.info(_(60*"="))
        self.report_interval = report_interval
        self.periodic_enable = periodic_enable
        self.periodic_fuzzy_delay = periodic_fuzzy_delay
        self.periodic_interval_max = periodic_interval_max
        self.saved_args, self.saved_kwargs = args, kwargs
        self.context = context.get_service_context()
        self.context.tg = self.tg
        self.context.periodic_enable = self.periodic_enable
        self.context.report_interval = self.report_interval
        self.context.periodic_fuzzy_delay = self.periodic_fuzzy_delay
        self.context.periodic_interval_max = self.periodic_interval_max
        LOG.info(_("========================Managers chain================="))
        idx = 0
        while idx < len(self.containers):
            LOG.info(_("Chain %(index)s  Manager: %(mname)s"),
                            {'index':idx,'mname':self.containers[idx].m_name})
            idx += 1
        LOG.info(_(60*"="))

        length = len(self.containers)
        if length == 0:
            raise
        i = 1
        while i < length:
            '''connect all manager containers, containers hand in hand'''
            _queue = queue.LightQueue(CONF.max_queue_size)
            self.containers[i-1].output_queue = _queue
            self.containers[i].input_queue = _queue
            i += 1

    @classmethod
    def create(cls, managers, report_interval=None, periodic_enable=None,
               periodic_fuzzy_delay=None, periodic_interval_max=None, *args, **kwargs):
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
        service_obj = cls(managers, report_interval=report_interval,
                          periodic_enable=periodic_enable,
                          periodic_fuzzy_delay=periodic_fuzzy_delay,
                          periodic_interval_max=periodic_interval_max, *args, **kwargs)
        return service_obj

    def start(self):
        LOG.info(_("Begin to loop container.pre_start_hook"))
        for container in self.containers:
            LOG.info(_("%(cname)s Pre_start_hook"),{'cname':container.m_name})
            container.pre_start_hook(self.context)
        LOG.info(_("End to loop container.pre_start_hook"))

        for container in self.containers:
            '''start container thread Run'''
            self.tg.add_thread(container.Run, self.context, self.saved_args, self.saved_kwargs)

        LOG.info(_("Begin to loop container.post_start_hook"))
        for container in self.containers:
            LOG.info(_("%(cname)s Post_start_hook"),{'cname':container.m_name})
            container.post_start_hook(self.context)
        LOG.info(_("End to loop container.post_start_hook"))

        if self.periodic_enable:
            if self.periodic_fuzzy_delay:
                initial_delay = random.randint(0, self.periodic_fuzzy_delay)
            else:
                initial_delay = None
            for container in self.containers:
                ''' start periodic tasks'''
                self.tg.add_dynamic_timer(container.periodic_tasks,
                                     initial_delay=initial_delay,
                                     periodic_interval_max=
                                        self.periodic_interval_max,context = self.context)
            if self.report_interval:
                ''' start report state peridic tasks'''
                self.tg.add_timer(self.report_interval, self._report_state,
                                 self.report_interval, self)

    def _report_state(self,service):
        '''FixedIntervalLoopingCall use report_interval'''
        for container in self.containers:
            container.periodic_report_tasks(service)

