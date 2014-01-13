'''
Created on 2014.1.5

@author: gaolichuang
'''



from miracle.common.utils import jsonutils
from miracle.common.base.exception import UnsupportDocType
_MESSAGE_TYPE = 'message_type'   # use for unserialize, for examlpe: crawldoc
_MESSAGE_KEY = 'message_key'

def serialize_msg(raw_msg,message_type='DEFAULT'):
    ''' python dict to json object(python str)
    return string'''
    msg = {_MESSAGE_TYPE: message_type,
           _MESSAGE_KEY: jsonutils.dumps(raw_msg)}
    return msg

def deserialize_msg(msg, message_type='DEFAULT'):
    if not isinstance(msg, dict):
        return msg

    base_envelope_keys = (_MESSAGE_TYPE, _MESSAGE_KEY)
    if not all(map(lambda key: key in msg, base_envelope_keys)):
        return msg

    if msg[_MESSAGE_TYPE] != message_type:
        raise UnsupportDocType(org_doct_ype=msg[_MESSAGE_TYPE],accept_doc_type=message_type)

    msg_dict = jsonutils.loads(msg[_MESSAGE_KEY])
    return msg_dict