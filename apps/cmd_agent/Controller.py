import queue
import time
import threading
import schedule


def job():
    print("I'm running on thread %s" % threading.current_thread())


# worker watch the jobqueue, if any job available in jobqueue, fetch it and start working
def worker(jobqueue):
    while 1:
        job_func = jobqueue.get()
        if job_func is None:
            break
        job_func()
        jobqueue.task_done()
        time.sleep(1)


def assignJobs(jobqueue, job):
    schedule.every(1).seconds.do(jobqueue.put, job)
    schedule.every(1).seconds.do(jobqueue.put, job)
    schedule.every(1).seconds.do(jobqueue.put, job)
    schedule.every(1).seconds.do(jobqueue.put, job)
    schedule.every(1).seconds.do(jobqueue.put, job)


def scheduler(jobqueue, interval=5, num_worker_threads=2):
    threads = []
    # create worker threads
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(jobqueue,))
        t.start()
        threads.append(t)

    # add jobs in jobqueue, worker thread watches jobqueue and get job from jobqueue
    assignJobs(jobqueue, job)

    _round = 0
    # start scheduler
    while 1:
        print("Round: %s" % _round)
        schedule.run_pending()
        print("There are %s jobs need to do." % jobqueue.qsize())
        jobqueue.join()
        print("There are %s jobs rest." % jobqueue.qsize())
        time.sleep(interval)
        _round += 1


def controller():
    jobqueue = queue.Queue()
    scheduler(jobqueue)


controller()

