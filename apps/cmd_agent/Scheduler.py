import queue
import time
import threading
import schedule


jobqueue = None
start_time = None

def job1():
    print("I'm running on thread %s. I am working on job1, it needs 3s. Current time is %s." % (threading.current_thread(), (time.time() - start_time)))
    time.sleep(3)
    print("I'm running on thread %s, I finished job1. Current time is %s." % (threading.current_thread(), (time.time() - start_time)))


def job2():
    print("I'm running on thread %s. I am working on job2, it needs 2s. Current time is %s." % (threading.current_thread(), (time.time() - start_time)))
    time.sleep(2)
    print("I'm running on thread %s, I finished job2. Current time is %s." % (threading.current_thread(), (time.time() - start_time)))


# worker watch the jobqueue, if any job available in jobqueue, fetch it and start working
def worker(jobqueue):
    while 1:
        _job_func = jobqueue.get()
        if _job_func is None:
            break
        _job_func()
        jobqueue.task_done()


def assignJobs(jobqueue):
    schedule.every(1).seconds.do(jobqueue.put, job1)
    schedule.every(1).seconds.do(jobqueue.put, job2)


def scheduler(num_worker_threads=2):
    _worker_threads = []
    # create worker threads. And make it watch on the job queue.
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(jobqueue,))
        t.start()
        _worker_threads.append(t)

    # add jobs in jobqueue, worker thread watches jobqueue and get job from jobqueue
    assignJobs(jobqueue)

    # start scheduler
    while 1:
        schedule.run_pending()
        time.sleep(1)


# watchdog
def watchdog():
    t_start = time.time()
    while 1:
        if jobqueue.qsize() > 0:
            print("%s seconds." % (time.time() - t_start))
            print("There are %s jobs need to do." % jobqueue.qsize())
        time.sleep(1)

def main():
    global start_time
    start_time = time.time()
    global jobqueue
    jobqueue = queue.Queue()
    _threads = []

    t_scheduler = threading.Thread(target=scheduler, args=())
    t_scheduler.start()
    _threads.append(t_scheduler)

    t_watchdog = threading.Thread(target=watchdog, args=())
    t_watchdog.start()
    _threads.append(t_watchdog)


if __name__ == '__main__':
    main()

