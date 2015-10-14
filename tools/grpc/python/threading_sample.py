__author__ = 'yokoi-h'

from threading import Condition, Thread, enumerate
import time

class SampleThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        print "  === start sub thread ==="

        cond = Condition()
        with cond:
            cond.wait()

        print "  === end sub thread ==="


class ThreadMonitor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        print "  === start sub thread ==="

        while True:
            print("")
            tlist=enumerate()
            for t in tlist:
                print(t)
            #print(traceback.extract_stack(sys._current_frames()))
            time.sleep(1)

        print "  === end sub thread ==="


if __name__ == '__main__':

    t = SampleThread()
    t.setDaemon(True)
    t.start()

    s = ThreadMonitor()
    s.setDaemon(True)
    s.start()


    time.sleep(5)

    # while True:
    #     print("sleep")
    #     tlist=enumerate()
    #     for t in tlist:
    #         print(t)
    #     #print(traceback.extract_stack(sys._current_frames()))
    #     time.sleep(1)

