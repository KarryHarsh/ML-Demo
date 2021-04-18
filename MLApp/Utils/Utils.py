# Helper methods
import pickle

def APIresponse(StatusCode,Message,result):
    response = dict()
    response['StatusCode'] = StatusCode
    response['Message'] = Message
    response['Data'] = result
    return response

def pickleload(filename):
    with open(filename, 'rb') as handle:
        file = pickle.load(handle)
        return file