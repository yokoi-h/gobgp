import gobgp_pb2
import sys
import signal
import traceback
import time
import os
from threading import Thread, active_count, enumerate

_TIMEOUT_SECONDS = 1000


class ClientThread(Thread):
    def __init__(self, gobgp, neighbor):
        self.gobgpd_addr = gobgp
        self.neighbor_addr = neighbor
        self.canceled = False
        self.stub = None
        Thread.__init__(self)

    def run(self):
        with gobgp_pb2.early_adopter_create_GobgpApi_stub(self.gobgpd_addr, 8080) as stub:
            self.stub = stub
            self.peers = stub.MonitorPeerState(gobgp_pb2.Arguments(name=self.neighbor_addr), _TIMEOUT_SECONDS)

            try:
                for peer in self.peers:
                    print("  BGP.info.bgp_state :%s" % ( peer.info.bgp_state))
            except Exception as e:
                print("exception should be occurred")
                print(e)


    def cancel(self):
        print("cancel called")
        self.peers.cancel()
        self.stub.stop()
        self.canceled = True



def receive_signal(signum, stack):
    print('signal received:%d' % signum)
    print('exit')

    os._exit(0)
    # sys.exit(0)


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
    gobgp = "192.168.31.189" #sys.argv[1]
    neighbor = "172.16.6.102" #sys.argv[2]


    t = ClientThread(gobgp, neighbor)
    t.daemon = True

    def receive_signal2(signum, stack):
        print('signal received:%d' % signum)
        print('cancel')
        t.cancel()
        #sys.exit(0)



    signal.signal(signal.SIGINT, receive_signal2)

    t.start()

    s = ThreadMonitor()
    s.setDaemon(True)
    s.start()


    while True and not t.canceled:
        print("sleep 1")
        time.sleep(1)



    #t.cancel()

    # while True:
    #     time.sleep(1)

    # sleep 1 sec forever to keep main thread alive
    # while True:
    #     print("sleep")
    #     tlist=enumerate()
    #     for t in tlist:
    #         print(t)
    #     #print(traceback.extract_stack(sys._current_frames()))
    #     time.sleep(1)
