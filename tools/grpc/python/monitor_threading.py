import gobgp_pb2
import sys
import signal
import time
import os
from threading import Thread

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
    #sys.exit(0)
    #exit(1)

if __name__ == '__main__':
    gobgp = sys.argv[1]
    neighbor = sys.argv[2]

    signal.signal(signal.SIGINT, receive_signal)

    t = Thread(target=run, args=(gobgp, neighbor))
    t.daemon = True
    t.start()

    # sleep 1 sec forever to keep main thread alive
    while True:
        time.sleep(1)
