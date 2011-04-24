from Queue import Queue, Empty, Full
from threading import Thread


# TODO: create generator version of iter

def thread_out_work_iter(arg_iterator,f,thread_count=4,
                         work_queue=None,result_queue=None):
    work_queue = work_queue or Queue()
    result_queue = result_queue or Queue()

    # we are going to create our threads
    # from the function / queues
    threads = []
    for i in xrange(thread_count):
        thread = thread_out_function(f,work_queue,result_queue)
        threads.append(thread)

    # now start up our threads (as we feed in work)
    active_threads = 0
    for args in arg_iterator():
        # add the args to the work queue
        work_queue.put_nowait(args)

        # start up a thread if there are any left to start
        if active_threads < len(threads):
            threads[active_threads].start()
            active_threads += 1

def thread_out_work(args,f,thread_percentage=.26,fake_it=False):
    results = []
    if fake_it:
        for arg in args:
            results.append(f(*arg))
    else:
        work_queue = Queue()
        result_queue = Queue()
        threads = []
        map(work_queue.put_nowait,args)
        for i in xrange(len(args)*thread_percentage):
            threads.append(thread_out_function(f,work_queue,result_queue))
            threads[-1].start()
        for thread in threads:
            thread.join()
        results = []
        try:
            while True:
                results.append(result_queue.get_nowait())
        except Empty:
            pass
    return results

def thread_out_function(f,in_queue,out_queue,never_ending=False):
    def threaded(f,in_queue,out_queue):
        while True:
            try:
                # we'll wait around a lil bit
                args = in_queue.get(True,5)
                r = f(*args)
                out_queue.put(r,True)

            except Empty, ex:
                # if we are out of work and not never ending
                # than our job is done
                if not never_ending:
                    return True

            except Exception:
                # we'll try again
                raise
                print 're-q:',args
                in_queue.put_nowait(args)
        return True

    return Thread(target=threaded,kwargs={'f': f,
                                          'in_queue':in_queue,
                                          'out_queue':out_queue})


