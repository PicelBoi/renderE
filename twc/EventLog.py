# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.7 (main, Aug 14 2025, 11:12:11) [Clang 17.0.0 (clang-1700.0.13.3)]
# Embedded file name: EventLog.py
# Compiled at: 2007-01-12 11:17:30
import os, time, types, xml.sax.saxutils as saxutils

class IEvent:

    def typeName(self):
        return

    def attributes(self):
        return

    def content(self):
        return


class Event(IEvent):

    def __init__(self, eventType=None, **kw):
        self.__dict__.update(kw)
        self._eventType = eventType
        return

    def typeName(self):
        tn = getattr(self, '_eventType', None)
        if tn == None:
            return self.__class__.__name__
        else:
            return tn
        return

    def attributes(self):
        attrs = self.__dict__.items()
        return list(filter((lambda e: e[0][0] != '_'), attrs))
        return

    def content(self):
        return []
        return


class EventLog:

    def __init__(self, basePath, rotationFreq):
        self.basePath = basePath
        self.workFile = '%s.tmp' % (basePath,)
        self.freq = rotationFreq
        now = int(time.time())
        self.nextRotation = self._calcNextRotationTime(now)
        return

    def write(self, event):
        assert __debug__ and isinstance(event, IEvent)
        self._rotate()
        self._write(event)
        return

    def writeData(self, tag, data):
        self._rotate()
        self._writeData(tag, data)
        return

    def _open(self):
        return open(self.workFile, 'a')
        return

    def _write(self, event):
        s = _xmlifyEvent(event)
        f = self._open()
        f.write(s)
        f.close()
        return

    def _writeData(self, tag, data):
        s = _xmlify(tag, data)
        f = self._open()
        f.write(s)
        f.close()
        return

    def _rotate(self):
        now = int(time.time())
        if now > self.nextRotation:
            if os.path.exists(self.workFile):
                rfname = '%s_%s.log' % (self.basePath, self.nextRotation)
                os.rename(self.workFile, rfname)
            self.nextRotation = self._calcNextRotationTime(now)
        return

    def _calcNextRotationTime(self, now):
        freq = self.freq
        return (now + freq) / freq * freq
        return


INDENT_STR = '   '

def _sortChildrenByType(children):
    attrs = []
    content = []
    for (k, v) in children:
        if hasattr(v, "__dict__"):
            content.append((k, v))
        else:
            attrs.append((k, v))

    return (attrs, content)
    return


def _getChildren(data):
    if isinstance(data, IEvent):
        content = data.content()
        attrs = data.attributes()
        return (attrs, content)
    dtype = type(data)
    if dtype == dict:
        return _sortChildrenByType(data.items())
    elif hasattr(dtype, "__dict__"):
        return _sortChildrenByType(data.__dict__.items())
    return None
    return


def _getDetailStrs(data, indent):
    children = _getChildren(data)
    cntStr = ''
    attrStr = ''
    if children == None:
        cntStr += str(data)
    else:
        (attrs, content) = children
        for (k, v) in content:
            cntStr += '\n' + _xmlifyData(k, v, indent + 1)

    if len(content) > 0:
        cntStr += '\n' + INDENT_STR * indent
    for (k, v) in attrs:
        attrStr += ' %s=%s' % (k, saxutils.quoteattr(str(v)))

    return (attrStr, cntStr)
    return


def _xmlifyData(tag, data, indent):
    (attrStr, cntStr) = _getDetailStrs(data, indent)
    s = INDENT_STR * indent
    if len(cntStr) == 0:
        s += '<%s%s />' % (tag, attrStr)
    else:
        s += '<%s%s>%s</%s>' % (tag, attrStr, cntStr, tag)
    return s
    return


def _xmlify(tag, data):
    return _xmlifyData(tag, data, 0) + '\n'
    return


def _xmlifyEvent(event):
    eventType = event.typeName()
    attrStr = ''
    for (k, v) in event.attributes():
        attrStr += ' %s=%s' % (k, saxutils.quoteattr(str(v)))

    cntStr = ''
    for (k, v) in event.content():
        if isinstance(v, IEvent):
            cntStr += _xmlifyEvent(k, v)
        else:
            cntStr += '<%s>%s</%s>' % (k, saxutils.escape(str(v)), k)

    if len(cntStr) == 0:
        s = '<%s%s />\n' % (eventType, attrStr)
    else:
        s = '<%s%s>%s</%s>\n' % (eventType, attrStr, cntStr, eventType)
    return s
    return

