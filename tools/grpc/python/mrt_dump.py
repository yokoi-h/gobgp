import gobgp_pb2
import sys
import netaddr
import signal
from datetime import datetime

_TIMEOUT_SECONDS = 100000
AFI_IP = 1
AFI_IP6 = 2
SAFI_UNICAST = 1


def check_address_family(neighbor):
    ip = netaddr.IPAddress(neighbor)
    if ip.version == 6:
        rf = AFI_IP6 << 16 | SAFI_UNICAST
        af = "ipv6"
    else:
        rf = AFI_IP << 16 | SAFI_UNICAST
        af = "ipv4"

    return rf, af


def run(gobgpd, resource, args):
    with gobgp_pb2.early_adopter_create_Grpc_stub(gobgpd, 8080) as stub:

        if resource == "global":
            interval = 0
            if len(args) > 0:
                interval = int(args[0])

            af = "ipv4"
            a = gobgp_pb2.MrtArguments(resource=0, interval=interval)

        elif resource == "neighbor":
            neighbor_address = args[0]
            interval = 0
            rf, af = check_address_family(neighbor_address)
            if len(args) > 1:
                interval = int(args[1])

            a = gobgp_pb2.MrtArguments(resource=1, rf=rf,
                                       neighbor_address=neighbor_address,
                                       interval=interval)
        else:
            print("unknown resource type: %s" % resource)
            return

        try:
            print('call GetMrt')
            dumps = stub.GetMrt(a, _TIMEOUT_SECONDS)

            if dumps:
                def receive_signal(signum, stack):
                    print('signal received:%d' % signum)
                    dumps.cancel()
                    print('stream canceled')

                print('register signal handler')
                signal.signal(signal.SIGINT, receive_signal)
                #print(dir(dumps))

                for dump in dumps:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = "rib_%s_%s" % (af, ts)
                    print("mrt dump: %s" % filename)
                    with open(filename, 'wb') as f:
                        f.write(dump.data)

        except Exception as err:
            dumps.cancel()
            print(err)

if __name__ == '__main__':
    g = sys.argv[1]
    r = sys.argv[2]
    run(g, r, sys.argv[3:])