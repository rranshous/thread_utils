def thread_out_work(args,f,thread_percentage=.25,fake_it=False):
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
        results = [x for x in result_queue.get_nowait()]
    return results

def thread_out_function(f,in_queue,out_queue):
    def threaded(f,in_queue,out_queue):
        while not in_queue.empty() or out_queue.empty():
            try:
                args = in_queue.get(True,2)
                r = f(*args)
                out_queue.put(r,True)
            except Empty, ex:
                print 'empty'
        return True

    return Thread(target=threaded,kwargs={'f': f,
                                          'in_queue':in_queue,
                                          'out_queue':out_queue})

