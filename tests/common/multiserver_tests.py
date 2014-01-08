'''
Created on 2014.1.1

@author: gaolichuang
'''

import sys

from oslo.config import cfg

from miracle.common import config
from miracle.common.base import log as logging
from miracle.common.service import service
from miracle.common.service import multiservice

def main():
    config.parse_args(sys.argv)
    logging.setup("miracle")

    server = multiservice.MultiServer.create(
                    managers = ['miracle.common.manager.simplemanager.SimpleManager',
                                'miracle.common.manager.simplemanager.SimpleManager',
                                'miracle.common.manager.simplemanager.SimpleManager'])

    service.serve(server)
    service.wait()


if __name__ == '__main__':
    main()

