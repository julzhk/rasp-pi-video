import functools, logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class log_with(object):
    ENTRY_MESSAGE = 'Entering {}'
    EXIT_MESSAGE = 'Exiting {}'
    
    def __init__(self, logger = None):
        self.logger = logger
    def __call__(self, func):
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wrap(func)
        def wrapper(*args, **kwargs):
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))
            f_results = func(*args,**kwargs)
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__))
            return f_result
        return wrapper
