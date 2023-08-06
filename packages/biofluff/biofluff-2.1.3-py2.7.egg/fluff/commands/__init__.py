__author__ = 'george'

import os
import pkgutil

dirname = os.path.split(__file__)[0]

# Dynamically load all commands
for importer, cmdname, _ in pkgutil.iter_modules([dirname]):
    m = __import__("{0}.{1}".format(__name__, cmdname), globals(), locals(), [cmdname], -1)
    globals()[cmdname] = getattr(m, cmdname)
