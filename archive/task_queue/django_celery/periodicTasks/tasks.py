from celery import task


@task()
def add(x, y):
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
