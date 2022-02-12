import pickle

def pack(data):
    return pickle.dumps(data)


def unpack(data):
    return pickle.loads(data)