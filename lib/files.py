import os, sys
from lib.config import FILE_TYPE, PLOT_SRC, WAKEUP_FOLDER

def CheckFileType(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPE:
        return True

def SetupFileName(filename):
    i = 1
    while os.path.exists(os.path.join(PLOT_SRC, filename)) or \
            os.path.exists(os.path.join(WAKEUP_FOLDER, filename)):

        name, extension = os.path.splitext(filename)
        filename = '{0}_{1}{2}'.format(name, str(i), extension)
        i += 1
    return filename
