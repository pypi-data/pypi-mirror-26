from .loadump import Loadumper, OpenMode

def load(filename, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(OpenMode.READ, filename=filename, encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def loads(s, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(OpenMode.READ, s=s, encoding=encoding, errors=errors, buffering=buffering, **kwargs)
