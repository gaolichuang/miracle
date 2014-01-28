'''
Created on 2014.1.27

@author: gaolichuang
'''

from miracle.common.utils import timeutils

def convert_datetimes(values, *datetime_keys):
    for key in values:
        if key in datetime_keys and isinstance(values[key], basestring):
            values[key] = timeutils.parse_strtime(values[key])
    return values

if __name__ == '__main__':
    pass