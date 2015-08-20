
import gobgp_pb2
import sys

_TIMEOUT_SECONDS = 10


def run(gobgpd):

    with gobgp_pb2.early_adopter_create_Grpc_stub(gobgpd, 8080) as stub:
        resource = sys.argv[2]
        neighbor = ""
        if resource == "global":
            res = 0
        elif resource == "neighbor":
            res = 1
            neighbor = sys.argv[3]
        else:
            print("unknown resource type: %s" % resource)

        arg = gobgp_pb2.MrtArguments(resource=res, rf=4, neighbor_address=neighbor)
        dumps = stub.GetMrt(arg, _TIMEOUT_SECONDS)
        for dump in dumps:
            print(dump.data)


if __name__ == '__main__':
    gobgpd = sys.argv[1]
    run(gobgpd)