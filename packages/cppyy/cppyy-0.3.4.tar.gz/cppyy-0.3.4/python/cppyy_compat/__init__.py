"""Compatibility layer for PyPy 5.8 and 5.7
"""

def pypy58_57_compat():
    import imp, os

  # first load and move the builtin cppyy module
    if not 'cppyy' in sys.modules:
        try:
            olddir = os.getcwd()
            from cppyy_backend import loader
            c = loader.load_cpp_backend()
          # move to the location of the backend, just in case '.' is
          # in the dynloader's path
            os.chdir(os.path.dirname(c._name))
            imp.init_builtin('cppyy')
        except ImportError:
            raise EnvironmentError('"%s" missing in LD_LIBRARY_PATH' %\
                                   os.path.dirname(c._name))
        finally:
            os.chdir(olddir)

    sys.modules['_cppyy'] = sys.modules['cppyy']
    del sys.modules['cppyy']

  # now locate and load the pip cppyy module
    decdir = os.path.join(os.path.dirname(__file__), os.path.pardir)
    for path in sys.path:     # walk over sys.path skips builtins
        try:
            fp, pathname, description = imp.find_module('cppyy', [path])
            sys.modules['cppyy'] = imp.load_module('cppyy_', fp, pathname, description)
            break
        except ImportError:
            pass

  # copy over the _cppyy functions into cppyy
    old = sys.modules['_cppyy']
    new = sys.modules['cppyy']
    for name in dir(old):
        if not hasattr(new, name):
            setattr(new, name, getattr(old, name))
    
import sys
version = sys.pypy_version_info
if version[0] == 5 and 6 < version[1] <= 8:
    pypy58_57_compat()
del version, sys
