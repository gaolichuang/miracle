# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""DB related custom exceptions.
copy from nova.openstack.common.db.exception"""

from miracle.common.utils.gettextutils import _  # noqa


class DBError(Exception):
    """Wraps an implementation specific exception."""
    def __init__(self, inner_exception=None):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(str(inner_exception))

class DBDuplicateEntry(DBError):
    """Wraps an implementation specific exception."""
    def __init__(self, columns=[], inner_exception=None):
        self.columns = columns
        super(DBDuplicateEntry, self).__init__(inner_exception)

class DBDeadlock(DBError):
    def __init__(self, inner_exception=None):
        super(DBDeadlock, self).__init__(inner_exception)

class DBInvalidUnicodeParameter(Exception):
    message = _("Invalid Parameter: "
                "Unicode is not supported by the current database.")
