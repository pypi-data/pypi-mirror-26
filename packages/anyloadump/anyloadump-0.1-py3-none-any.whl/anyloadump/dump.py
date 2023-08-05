from .loadump import Loadumper, OpenMode

def dump(obj, filename, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, open_mode=OpenMode.WRITE, filename=filename,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def adump(obj, file, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(
        obj=obj,
        open_mode=OpenMode.APPEND,
        filename=file,
        encoding=encoding,
        errors=errors,
        buffering=buffering,
        **kwargs
    )

def xdump(obj, filename, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(
        obj=obj,
        open_mode=OpenMode.EXCLUSIVE_CREATION,
        filename=filename,
        encoding=encoding,
        errors=errors,
        buffering=buffering,
        **kwargs
    )

def dumps(obj, fmt, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, fmt=fmt, open_mode=OpenMode.WRITE,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def adumps(obj, fmt, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, fmt=fmt, open_mode=OpenMode.APPEND,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)

def xdumps(obj, fmt, *, encoding=None, errors=None, buffering=None, tbs=None, **kwargs):
    ld = Loadumper(tbs)
    return ld.loadump(obj=obj, fmt=fmt, open_mode=OpenMode.EXCLUSIVE_CREATION,
                   encoding=encoding, errors=errors, buffering=buffering, **kwargs)
