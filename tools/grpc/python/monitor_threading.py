import gobgp_pb2
import sys
import signal
import traceback
import time
import os
from threading import Thread, active_count, enumerate

_TIMEOUT_SECONDS = 1000

def run(gobgpd_addr, neighbor_addr):
    with gobgp_pb2.early_adopter_create_GobgpApi_stub(gobgpd_addr, 8080) as stub:
        peers = stub.MonitorPeerState(gobgp_pb2.Arguments(name=neighbor_addr), _TIMEOUT_SECONDS)

        for peer in peers:
            print("  BGP.info.bgp_state :%s" % ( peer.info.bgp_state))


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

    signal.signal(signal.SIGINT, receive_signal)

    t = Thread(target=run, args=(gobgp, neighbor))
    t.daemon = True
    t.start()


    s = ThreadMonitor()
    s.setDaemon(True)
    s.start()

    time.sleep(10)
    print("sleep ended")
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
