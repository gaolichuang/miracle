'''
Created on 2014.1.5

@author: gaolichuang@gmail.com
'''
from miracle.common.utils.gettextutils import _  # noqa
from miracle.common.base import log as logging

LOG = logging.getLogger(__name__)

class MiracleBaseException(Exception):
    msg_fmt = _("An unknown related exception occurred.")

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.msg_fmt % kwargs

            except Exception:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception(_('Exception in string format operation'))
                for name, value in kwargs.iteritems():
                    LOG.error("%s: %s" % (name, value))
                # at least get the core message out if something happened
                message = self.msg_fmt

        super(BaseException, self).__init__(message)
        
class UnsupportDocType(MiracleBaseException):
    msg_fmt = _("Doc type does not match, org doctype %(org_doct_ype)s, accept doc type "
                " %(accept_doc_type)s.")        