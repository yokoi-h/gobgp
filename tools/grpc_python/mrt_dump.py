import gobgp_pb2
import sys
import netaddr

_TIMEOUT_SECONDS = 10
AFI_IP = 1
AFI_IP6 = 2
SAFI_UNICAST = 1


def check_address_family(neighbor):
    ip = netaddr.IPAddress(neighbor)
    if ip.version == 6:
        return AFI_IP6 << 16 | SAFI_UNICAST
    else:
        return AFI_IP << 16 | SAFI_UNICAST

def run(gobgpd, resource, args):
    with gobgp_pb2.early_adopter_create_Grpc_stub(gobgpd, 8080) as stub:

        if resource == "global":
            interval = 0
            if len(args) > 0:
                interval = int(args[0])

            a = gobgp_pb2.MrtArguments(resource=0, interval=interval)

        elif resource == "neighbor":
            neighbor_address = args[0]
            interval = 0
            rf = check_address_family(neighbor_address)
            if len(args) > 1:
                interval = int(args[1])

            a = gobgp_pb2.MrtArguments(resource=1, rf=rf,
                                       neighbor_address=neighbor_address,
                                       interval=interval)
        else:
            print("unknown resource type: %s" % resource)

        dumps = stub.GetMrt(a, _TIMEOUT_SECONDS)
        for dump in dumps:
            print(dump.data)


if __name__ == '__main__':
    gobgpd = sys.argv[1]
    resource = sys.argv[2]
    run(gobgpd, resource, sys.argv[3:])