============
cotimelog
============

**cotimelog**, inspired from [ConcurrentLogHandler](https://pypi.python.org/pypi/ConcurrentLogHandler/0.9.1).
To be honest, it is almost the same code. Just edit to make the log file rotated by time.


Installation
============

    pip install cotimelog


ConcurrentTimeRotatingFileHandler
---------------------------------

This class is a log handler which is a drop-in replacement for the python standard log handler
``TimedRotatingFileHandler``.
The TimedRotatingFileHandler will failed to rotate when multiple processes are trying to
write into the same file. You will meet this issue when you use uwsgi.
This ``ConcurrentTimeRotatingFileHandler`` class is mainly developed to fix this issue.

Usage
`````

Using ``ConcurrentTimeRotatingFileHandler`` ::

    import os
    import time
    from logging import getLogger, INFO
    from cotimelog import ConcurrentTimeRotatingFileHandler

    # Use an absolute path to prevent file rotation trouble.
    log = getLogger()
    logfile = os.path.abspath("mylogfile.log")
    # Rotate log after 1 second
    rotateHandler = ConcurrentTimeRotatingFileHandler(logfile, mode="a", when="S", backupCount=5)
    log.addHandler(rotateHandler)
    log.setLevel(INFO)

    [log.info(str(i)) for i in range(10)]
    time.sleep(1)
    [log.info(str(i)) for i in range(10, 100)]




License
^^^^^^^

`Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_
