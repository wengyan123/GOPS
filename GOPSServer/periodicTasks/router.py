
class Myrouter(object):
    def routeForTask(self, task, args=None, kwargs=None):
        return {'exchange': 'celery',
                'exchange_type': 'direct',
                'queue': task,
                'routing_key': task
                }