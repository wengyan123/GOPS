################################################################
#
# start client to listen specific queue
# celery -A tasks worker -l info -Q host1
#
################################################################

from celery import Celery
from celery import task
from celery.utils.log import get_task_logger


app = Celery('client', broker='pyamqp://guest@localhost//')
logger = get_task_logger(__name__)


@task(name='sum_of_two_numbers', bind=True)
def add(self, x, y):
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y


def print_result(result):
    if result.ready():
        print("Task has run")
        if result.successful():
            print("Result was: %s" % result.result)
        else:
            if isinstance(result.result, Exception):
                print("Task failed due to raising an exception")
                raise result.result
            else:
                print("Task failed without raising exception")
    else:
        print("Task has not yet run")
