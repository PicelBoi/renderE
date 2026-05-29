# uncompyle6 version 3.9.3
# Python bytecode version base 2.2 (60717)
# Decompiled from: Python 3.13.2 (main, Feb  4 2025, 14:51:09) [Clang 16.0.0 (clang-1600.0.26.6)]
# Embedded file name: psp.py
# Compiled at: 2007-01-12 11:17:30
import os.path, rsfix
import nethandler
import traceback

_includePath = ['.']

def setIncludePath(path=[]):
    global _includePath
    _includePath = path
    return

import rendereglobals as rg
newstat = rg.newstat
newaccess = rg.newaccess
from functools import reduce
def evalPage(page, namespace={}, includePath=None):
    """Parses text looking for tags in the spirit of ASP tags and evaluates
    them.  The contexts of the tags are passed to the Python interpreter.
    The page, after evaluating the tags, is returned as the result of this 
    function.  Two type of tags are supported: '<%!...%>'  and '<%=...%>'.
    The contents of the '!' style tags are exec'd and the tag
    is removed from the original page.  The contents of the '=' style tags
    are eval'd and a string representation of the result is placed inline
    in the original text in place of the tag.  The provided namespace is 
    used by the Python interpreter.  Using the default parameter for this
    value causes a unique namespace to be created and used for each call.
    This implies that multiple tags w/in the same page (passed in text)
    share the namespace.  In other words one tag can create global values 
    that can be used by later tags.
    """
    namespace["reduce"] = reduce
    page = page.replace("os.stat", "newstat")
    page = page.replace("os.newaccess", "newaccess")
    page = page.replace("os.path.exists", "newexists")
    page = page.replace("os.path.join", "newjoin")
    if includePath == None:
        includePath = _includePath
    p1 = page.find('<%')
    if p1 == -1:
        return page
    cmd = page[p1 + 2]
    p2 = page.find('%>', p1)
    if p2 == -1:
        return page[:p1]
    sub1 = page[:p1]
    sub2 = page[p1 + 3:p2]
    sub3 = page[p2 + 2:]
    if cmd == '#':
        return sub1 + evalPage(sub3, namespace, includePath)
    elif cmd == '@':
        values = eval(sub2, namespace)
        if not isinstance(values, list):
            values = [values]
        res = sub1
        for val in values:
            if val == None:
                continue
            val = str(val)
            val2 = str(val)
            val2.replace("/usr/twc/domestic", os.environ["RENDEREDOMESTIC"])
            fname = None
            if val2[0] == '/' or val2[1] == ":"  or val2.startswith("C:"):
                if os.path.exists(val2):
                    fname = val
                elif nethandler.requestNetAssetExt(val2):
                    fname = nethandler.requestNetAssetExt(val2)
            
            for path in includePath:
                temp = '%s/%s' % (path, val)
                if os.path.exists(temp):
                    fname = temp
                    break
            if not fname:
                for path in includePath:
                    temp = '%s/%s' % (path, val)
                    fn = nethandler.requestNetAssetExt(temp, check=True)
                    if fn is not None:
                        fname = fn
                        break
            if not fname:
                for path in includePath:
                    temp = '%s/%s' % (path, val)
                    fn = nethandler.requestNetAssetExt(temp)
                    if fn is not None:
                        fname = fn
                        break
            print(fname, " found!")
            if not fname:
                includePath = ["/usr/twc/domestic/products/pm/incl"]
                for path in includePath:
                    temp = '%s/%s' % (path, val)
                    fn = nethandler.requestNetAssetExt(temp)
                    if fn is not None:
                        fname = fn
                        break

            if fname == None:
                raise RuntimeError(f'file {sub2} in PSP include tag not found (searching for {values} in paths {includePath})')
            f = open(fname, 'r')
            sub2 = f.read()
            f.close()
            try:
                res += evalPage(sub2, namespace, includePath)
            except Exception as e:
                raise e

        #res += evalPage(sub3, namespace, includePath)
        try:
            res += evalPage(sub3, namespace, includePath)
        except Exception as e:
            raise e
        return rsfix.fix(res)
    elif cmd == '!':
        #print(sub2[:100])
        try:
            exec(rsfix.fix_if(sub2).replace("os.stat", "newstat").replace("os.newaccess", "newaccess").replace("os.path.exists", "newexists").replace("os.path.join", "newjoin"), namespace)
        except Exception as e:
            with open("sub2explosion.txt", "w") as f:
                f.write(sub2)
            raise e
        return sub1 + evalPage(sub3, namespace, includePath)
    elif cmd == '=':
        return sub1 + str(eval(sub2, namespace)) + evalPage(sub3, namespace, includePath)
    elif cmd == '-':
        try:
            return sub1 + repr(eval(sub2, namespace)) + evalPage(sub3, namespace, includePath)
        except:
            with open("subexplosion.txt", "w") as f:
                f.write(page)
            with open("subexplosione.txt", "w") as f:
                f.write(traceback.format_exc())
            raise
    else:
        raise RuntimeError('invalid psp tag %s' % (cmd,))
    return


def evalRenderScript(page, namespace={}, includePath=None):
    """Same as eval but augments the namespace to include things
    that will be common to render script evaluation.  As an example,
    a get function will be added that retrieves data from the DataStore.
    """
    from twc import DataStoreInterface
    import twc.dsmarshal
    import twc.rsutil as rsutil
    namespace['rsutil'] = rsutil
    namespace['ds'] = DataStoreInterface
    namespace['dsm'] = twc.dsmarshal
    return evalPage(page, namespace, includePath)
