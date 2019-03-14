# coding: utf-8
'''
यहां हम अपने आधार स्थापित करते हैं, यानी constants
'''
import datetime
import re
import random
bannertext = '''_______________________
< Xetrapal (क्षेत्रपाल) >
 ----------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||

हिन्दी में सोशियल मीडिया का अध्ययन
'''

helptext = '''
If you can't read the text above, you will probably have trouble with the concepts used in this program.
This is by design
That said, doctrings generally work. If you know how to read those, have fun.
'''

XPAL_FIELD_STYLES = {'hostname': {'color': 'magenta'}, 'programname': {'color': 'cyan'}, 'name': {
    'color': 'cyan', 'bold': True}, 'levelname': {'color': 'green', 'bold': True}, 'asctime': {'color': 'green'}}

XPAL_LEVEL_STYLES = {'info': {'color': 'blue'}, 'notice': {'color': 'magenta'}, 'verbose': {}, 'success': {'color': 'green', 'bold': True}, 'spam': {
    'color': 'green', 'faint': True}, 'critical': {'color': 'red', 'bold': True}, 'error': {'color': 'red'}, 'debug': {'color': 'green'}, 'warning': {'color': 'yellow'}}

XPAL_CONSOLE_FORMAT = "%(asctime)s %(name)s-%(threadName)s-[%(funcName)s] %(levelname)s : %(message)s"

XPAL_LOG_FORMAT = "%(asctime)s %(hostname)s %(name)s-%(threadName)s-[%(funcName)s] %(levelname)s : %(message)s"

XPAL_WAIT_TIME = {"short": 5, "medium": 10, "long": 30}

XPAL_UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()

nospec = re.compile(r"[^A-Za-z0-9\n @.'\-+()]+")
notnum = re.compile(r"[^0-9+()\-]+")
engalpha = re.compile(r"[a-zA-Z]")


def random_of_ranges(*ranges):
    return random.choice(random.choice(ranges))


def get_utc_ts(ts, **kwargs):
    adjts = ts + XPAL_UTC_OFFSET_TIMEDELTA
    return adjts


def get_local_ts(ts, **kwargs):
    adjts = ts - XPAL_UTC_OFFSET_TIMEDELTA
    return adjts
