import os.path, getopt, sys
import socket
import json
import nethandler as nh
class Data:
    """An empty data structure.  Useful for data structures with dynamic
    member fields, i.e. adding new member variables at run time.
    """

    def __init__(self, other=None, **kw):
        self.update(other, **kw)
        return

    def __repr__(self):
        c = self.__class__
        s = '%s.%s(' % (c.__module__, c.__name__)
        for (k, v) in self.__dict__.items():
            s += '%s=%s, ' % (k, repr(v))

        s += ')'
        return s
        return

    def update(self, other=None, **kw):
        if other != None:
            self.__dict__.update(other.__dict__)
        self.__dict__.update(kw)
        return

    def clone(self):
        other = Data()
        other.update(self)
        return other
        return

def main():
    id = 0
    expire = 1200
    vbid = '000'
    logoId = None
    mediaNum = None
    flavor = None
    duration = 0
    durationFrames = 0
    (opts, args_proper) = getopt.getopt(sys.argv[1:], '', [6, 7, 8, 9, 10])
    for (opt, val) in opts:
        if opt == '--id':
            id = int(val)
        if opt == '--expire':
            expire = int(val)
        if opt == '--vbid':
            vbid = val
        if opt == '--logoId':
            logoId = val
        if opt == '--duration':
            duration = int(val)
    
    print(args_proper)
    prodType = args_proper[0]
    d = Data()
    d.id = id
    d.expire = expire
    if prodType == 'local':
        if len(args_proper) > 1:
            flavor = args_proper[1]
            if len(args_proper) > 2:
                if logoId == None:
                    logoId = args_proper[2]
        d.logoId = logoId
        d.flavor = flavor
        d.vbid = vbid
        d.durationFrames = durationFrames
        if duration > 0:
            d.duration = duration
        else:
            flavorMap = {'D': 60, 'E': 60, 'F': 58, 'S': 57, 'K': 90, 'O': 90, 'P': 90, 'N': 120, 'L': 120, 'M': 120}
            d.duration = flavorMap[flavor]
    if prodType == 'tag':
        if len(args_proper) > 1:
            mediaNum = args_proper[1]
            if len(args_proper) > 2:
                duration = int(args_proper[2])
                if len(args_proper) > 3:
                    durationFrames = int(args_proper[3])
        d.mediaNum = mediaNum
        d.duration = duration
        d.durationFrames = durationFrames
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 7245))
    nh._socksend(sock, ("jsonload " + prodType + " "+json.dumps(d.__dict__)).encode())
    sock.close()
    #wxdata.loadData(prodType, d)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())