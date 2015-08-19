
import gobgp_pb2
import sys

_TIMEOUT_SECONDS = 10


def run(gobgpd):
    with gobgp_pb2.early_adopter_create_Grpc_stub(gobgpd, 8080) as stub:
        peer = stub.GetNeighbor(gobgp_pb2.Arguments(rf=4, name="10.0.0.100"), _TIMEOUT_SECONDS)
        print("*** call GetNeighbor ***")
        print("BGP neighbor is %s, remote AS %d" % (peer.conf.remote_ip, peer.conf.remote_as))
        print("  BGP version 4, remote router ID %s" % ( peer.conf.id))
        print("  BGP state = %s, up for %s" % ( peer.info.bgp_state, peer.info.uptime))
        print("  BGP OutQ = %d, Flops = %d" % (peer.info.out_q, peer.info.flops))
        print("  Hold time is %d, keepalive interval is %d seconds" % ( peer.info.negotiated_holdtime, peer.info.keepalive_interval))
        print("  Configured hold time is %d, keepalive interval is %d seconds" % ( peer.conf.holdtime, peer.conf.keepalive_interval))

        print("")
        print("")
        print("*** call GetNeighbors ***")
        response = stub.GetNeighbors(gobgp_pb2.Arguments(), _TIMEOUT_SECONDS)
        peers = []
        maxaslen = 0
        maxaddrlen = 0
        for p in response:
            maxaslen = len(str(p.conf.remote_as)) if len(str(p.conf.remote_as)) > maxaslen else maxaslen
            maxaddrlen = len(str(p.conf.remote_ip)) if len(str(p.conf.remote_ip)) > maxaddrlen else maxaddrlen
            peers.append(p)

        format = "%-" + str(maxaddrlen) + "s" + " %" + str(maxaslen) + "s" + " %" + str(10) + "s"
        format += " %-15s |%11s %8s %8s"
        print(format % ("Peer", "AS", "Up/Down", "State", "#Advertised", "Received", "Accepted"))
        for p in peers:
            print(format % (p.conf.remote_ip, p.conf.remote_as, p.info.downtime, p.info.bgp_state, p.info.advertized, p.info.received, p.info.accepted))

if __name__ == '__main__':
    gobgpd = sys.argv[1]
    run(gobgpd)