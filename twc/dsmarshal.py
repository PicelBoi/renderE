# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: dsmarshal.py
# Compiled at: 2007-01-12 11:17:30
import sys, twc, twc.DataStoreInterface, twccommon, json, socket, pickle
from io import BytesIO
import nethandler as nh
ds = twc.DataStoreInterface
ds.init()
_TYP_INT = 'int'
_TYP_FLT = 'float'
_TYP_STR = 'str'
_TYP_TUPLE = 'tuple'
_TYP_LIST = 'list'
_TYP_INST = 'struct'
_defaultDict = {}

# Source - https://stackoverflow.com/a
# Posted by ShadowRanger
# Retrieved 2025-12-18, License - CC BY-SA 4.0


def apply(func, args, kwargs=None):
    return func(*args) if kwargs is None else func(*args, **kwargs)


def setDefault(key, data):
    global _defaultDict
    _defaultDict[key] = data
    return

def jsontodata(jsond):
    dt = twccommon.Data()
    dt.__dict__ = json.loads(jsond)
    return dt

def datatojson(dt):
    if isinstance(dt, twccommon.Data):
        jsond = json.dumps(dt.__dict__)
    else:
        jsond = dt.__repr__()
        
    return jsond

def set(key, data, expiration, update=0, session=0):
    if isinstance(data, str):
        ds.set([(key, data, expiration)], session)
        return ''
    if update:
        try:
            oldData = get(key, session)
        except KeyError:
            update = 0

    userData = None
    if update:
        t1 = type(data)
        t2 = type(oldData)
        #todo: what
        if (not hasattr(t1, "__dict__")) or (not hasattr(t2, "__dict__")):
            raise RuntimeError('cannot update non-instance type')
        userData = twc.Data()
        userData.__dict__.update(data.__dict__)
        temp = twc.Data()
        temp.__dict__.update(oldData.__dict__)
        temp.__dict__.update(data.__dict__)
        data = temp
    (formatStr, marshaledEntries) = _set(key, data, expiration, marshalStr=1)
    if update:
        (tmp, marshaledEntries) = _set(key, userData, expiration, marshalStr=1)
        marshaledEntries.append(('%s._dsmarshal' % key, formatStr, expiration))
    ds.set(marshaledEntries, session)
    return formatStr
    return

def rset(key, data, expiration, update=0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 7245))
    buf = BytesIO()
    pickler = pickle.Pickler(buf)
    pickler.dump(data)
    nh._socksend(sock, ((f"rset {key} {expiration} {update} ".encode())+buf.getvalue()))
    res = bytearray()
    while True:
        dat = sock.recv(1024)
        if not dat:
            break
        res.extend(dat)
    sock.close()
    return res.decode()

def defaultedGet(key, default=None, cachingEnabled=None):
    """Get the object referenced by key, else, return default obj if u cant 
find it"""
    try:
        return get(key, cachingEnabled)
    except KeyError:
        return default

    return


def get(key, cachingEnabled=None, session=0):
    try:
        defaultResult = _defaultDict[key]
        if isinstance(defaultResult, twccommon.Data):
            defaultResult = defaultResult.clone()
    except KeyError:
        defaultResult = None

    try:
        formatKey = '%s._dsmarshal' % key
        (rc, data) = ds.get([key, formatKey], cachingEnabled, session)
        print(f"accessing {formatKey}")
        try:
            tokens = data[formatKey].split(' ')
        except KeyError:
            return data[key]

        fields = []
        maker = _parse(key, tokens, fields)
        if fields:
            (rc, data) = ds.get(fields, cachingEnabled, session)
        result = _make(maker, data)
        if isinstance(result, twccommon.Data) and isinstance(defaultResult, twccommon.Data):
            result = twccommon.mergeStructs([result], defaultResult)
        return result
    except KeyError as e:
        if defaultResult != None:
            return defaultResult
        else:
            raise e

    return

def rget(key, cachingEnabled=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 7245))
    nh._socksend(sock, ("rget "+key).encode())
    data = bytearray()
    while True:
        res = sock.recv(1024)
        if not res:
            break
        data.extend(res)
    sock.close()
    return pickle.Unpickler(BytesIO(data)).load()
    
def multiGet(keys, cachingEnabled=None, session=0):
    keyDict = {}
    dsKeys = []
    for key in keys:
        formatKey = '%s._dsmarshal' % key
        dsKeys.append(key)
        dsKeys.append(formatKey)
        d = twc.Data()
        d.formatKey = formatKey
        d.result = None
        d.maker = None
        keyDict[key] = d

    (rc, data) = ds.get(dsKeys, cachingEnabled, session)
    fields = []
    for key in keys:
        d = keyDict[key]
        try:
            tokens = data[d.formatKey].split(' ')
            d.maker = _parse(key, tokens, fields)
        except KeyError:
            try:
                d.result = data[key]
            except KeyError:
                d.result = None

    if fields:
        (rc, data) = ds.get(fields, cachingEnabled, session)
    result = []
    for key in keys:
        d = keyDict[key]
        if d.maker:
            result.append(_make(d.maker, data))
        else:
            result.append(d.result)

    return result
    return


def configGet(key, cachingEnabled=None, session=0):
    """Prepends a "Config.<configVersion>." to the incoming key,
       queries the datastore for the value of that key, and
       returns the value.

       The "configVersion" attribute is stored in the dataStore,
       and updated for each configuration release.  This allows
       us to decouple different config releases in the field."""
    cfgKey = 'Config.' + str(get('configVersion')) + '.' + key
    return get(cfgKey, cachingEnabled, session)
    return


def defaultedConfigGet(key, default=None, cachingEnabled=None):
    cfgKey = 'Config.' + str(get('configVersion')) + '.' + key
    try:
        return get(cfgKey, cachingEnabled)
    except KeyError:
        return default

    return


def getConfigVersion():
    """Returns the current configuration version."""
    return str(get('configVersion'))
    return


def remove(key, session=0):
    fields = []
    try:
        formatKey = '%s._dsmarshal' % key
        (rc, data) = ds.get([formatKey], cachingEnabled=0, session=session)
        tokens = data[formatKey].split(' ')
        maker = _parse(key, tokens, fields)
        fields.append(formatKey)
    except KeyError:
        fields = [key]

    rc = ds.remove(fields, session)
    return


def _set(key, data, expire, marshalStr=0):
    t = data
    if isinstance(t, int):
        return _setAtomicType(key, _TYP_INT, data, expire, marshalStr)
    elif isinstance(t, float):
        return _setAtomicType(key, _TYP_FLT, data, expire, marshalStr)
    elif isinstance(t, str):
        return _setAtomicType(key, _TYP_STR, data, expire, marshalStr)
    elif isinstance(t, tuple):
        fields = map((lambda a, b: (a, b)), range(len(data)), data)
        return _setContainerType(key, _TYP_TUPLE, '', fields, expire, marshalStr)
    elif isinstance(t, list):
        fields = map((lambda a, b: (a, b)), range(len(data)), data)
        return _setContainerType(key, _TYP_LIST, '', fields, expire, marshalStr)
    elif isinstance(t, object):
        cl = data.__class__
        args = '%s %s' % (cl.__module__, cl.__name__)
        return _setContainerType(key, _TYP_INST, args, data.__dict__.items(), expire, marshalStr)
    else:
        raise RuntimeError('%s not supported by dsmarshal' % (str(t),))
    return


def _setAtomicType(key, formatStr, data, expire, marshalStr):
    entries = []
    formatStr = '%s ' % formatStr
    if marshalStr:
        entries.append(('%s._dsmarshal' % key, formatStr, expire))
    entries.append((key, str(data), expire))
    return (formatStr, entries)
    return


def _setContainerType(key, containerType, argsString, fields, expire, marshalStr):
    formatStr = ''
    entries = []
    for (fieldName, val) in fields:
        if val != None:
            (fs, ent) = _set('%s.%s' % (key, fieldName), val, expire)
            formatStr = formatStr + '%s %s' % (fieldName, fs)
            entries = entries + ent

    formatStr = '%s ( %s %s) ' % (containerType, argsString, formatStr)
    if marshalStr:
        entries.append(('%s._dsmarshal' % key, '%s' % formatStr, expire))
    return (formatStr, entries)
    return


def _parse(field, tokens, fields):
    token = _getNextToken(tokens)
    if token == _TYP_INT:
        fields.append(field)
        return (field, _makeInt, ())
    elif token == _TYP_FLT:
        fields.append(field)
        return (field, _makeFlt, ())
    elif token == _TYP_STR:
        fields.append(field)
        return (field, _makeStr, ())
    elif token == _TYP_TUPLE:
        return _parseTuple(field, tokens, fields)
    elif token == _TYP_LIST:
        return _parseList(field, tokens, fields)
    elif token == _TYP_INST:
        return _parseInst(field, tokens, fields)
    else:
        raise RuntimeError('dsmarshal err: unexpected token %s' % token)
    return


def _parseTuple(field, tokens, fields):
    _assume('(', _getNextToken(tokens))
    makers = []
    token = _getNextToken(tokens)
    while token != ')':
        makers.append(_parse('%s.%s' % (field, token), tokens, fields))
        token = _getNextToken(tokens)

    return (field, _makeTuple, (makers,))
    return


def _parseList(field, tokens, fields):
    _assume('(', _getNextToken(tokens))
    makers = []
    token = _getNextToken(tokens)
    while token != ')':
        makers.append(_parse('%s.%s' % (field, token), tokens, fields))
        token = _getNextToken(tokens)

    return (field, _makeList, (makers,))
    return


def _parseInst(field, tokens, fields):
    _assume('(', _getNextToken(tokens))
    moduleName = _getNextToken(tokens)
    className = _getNextToken(tokens)
    makers = []
    token = _getNextToken(tokens)
    while token != ')':
        makers.append(_parse('%s.%s' % (field, token), tokens, fields))
        token = _getNextToken(tokens)

    return (field, _makeInst, (moduleName, className, makers))
    return


def _getNextToken(tokens):
    token = ''
    while token == '':
        token = tokens[0]
        del tokens[0]

    return token
    return


def _assume(expected, got):
    if expected != got:
        raise RuntimeError('dsmarshal err: expected "%s" got "%s"' % (expected, got))
    return


def _make(maker, data):
    (field, makeFn, args) = maker
    args = (field, data) + args
    return apply(makeFn, args)
    return


def _makeInt(field, data):
    try:
        return int(data[field])
    except KeyError:
        return None

    return


def _makeFlt(field, data):
    try:
        return float(data[field])
    except KeyError:
        return None

    return


def _makeStr(field, data):
    try:
        return data[field]
    except KeyError:
        return None

    return


def _makeTuple(field, data, makers):
    res = ()
    for maker in makers:
        obj = _make(maker, data)
        res = res + (obj,)

    return res
    return


def _makeList(field, data, makers):
    res = []
    for maker in makers:
        res.append(_make(maker, data))

    return res
    return

def newinstance(cl, attrs):
    pass

def _makeInst(field, data, moduleName, className, makers):
    dict = {}
    for maker in makers:
        field = maker[0].split('.')[-1]
        dict[field] = _make(maker, data)

    mod = sys.modules[moduleName]
    cl = mod.__dict__[className]
    #makeinst is used for making data and i have no clue why you would ever need it.
    
    isdata = (cl is twccommon.Data)
    if isdata:
        return twccommon.Data(**dict)
    else:
        print("makeinst has been used on not-data. this is very bad.")
        print(cl)
        print(dict)
        sys.exit(1)
        return newinstance(cl, dict)
    return

def rcommit():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 7245))
    nh._socksend(sock, b"rcommit")
    sock.close()