import gobgp_pb2
import sys
import netaddr
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


        try:
            print("get")
            dumps = stub.GetMrt(a, _TIMEOUT_SECONDS)
            print("done")
            for dump in dumps:
                print("done2")
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = "rib_%s_%s" % (af, ts)
                print(filename)
                print(dump.data)

            print("done3")
        except Exception as err:
            print 'exception:', err
            sys.exit(1)
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            sys.exit(0)


if __name__ == '__main__':
    gobgpd = sys.argv[1]
    resource = sys.argv[2]
    run(gobgpd, resource, sys.argv[3:])