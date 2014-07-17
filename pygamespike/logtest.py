import logging

logging.basicConfig()
log = logging.getLogger('custom')
log.setLevel(logging.DEBUG)
log.info('hihi')


@log_with()
def test1():
    print 't1'


test1()
