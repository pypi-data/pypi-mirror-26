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

    import time
    from logging import getLogger, INFO
    from cotimelog import ConcurrentTimeRotatingFileHandler

    # Use an absolute path to prevent file rotation trouble.
    logfile = os.path.abspath("mylogfile.log")
    # Rotate log after reaching 512K, keep 5 old copies.
    rotateHandler = ConcurrentTimeRotatingFileHandler(logfile, mode="a", when="S")
    log.addHandler(rotateHandler)
    log.setLevel(INFO)

    log.info("Here is a very exciting log message, just for you")
    log.info("Here is one more very exciting log message, just for you")
    time.sleep(1)
    log.info("This should be in another file")



License
^^^^^^^

`Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_
