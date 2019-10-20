import time
from flask import request, g

LocalTime = time.strftime('%Y-%m-%d-%H%M',time.localtime(time.time()))

DEBUG = True
TEMPLATES_AUTO_RELOAD = True
# MAX_CONTENT_LENGTH = 50 * 1024 * 1024

VAD_PATH = "vad/"
PLOT_SRC = 'plot/'
WAKEUP_SRC = 'wakeup/'
PCM_SRC = "wakeup/pcm/"
DATA_AREA = "DataArea/"
PLOT_RESULT = "plot/result"
RESULT_PATH = "wakeup/result/"
CONFIG_SRC = "wakeup/config/"
FILE_TYPE = ["pcm", "txt", "q"]
SECRET_KEY = 'hard to guess string'
RESULT_SRC = "wakeup/result/wakeup_test.log"
WAKEUP_FOLDER = 'wakeup/' + LocalTime + '/'
RM_PLOT_FILE = " *.pcm *.png *.txt png_result/"
NOWAKEUP_SRC = "wakeup/result/no_wakeup_list.txt"

g.name = request.cookies.get("remember_token").split("|")[0] + "_"