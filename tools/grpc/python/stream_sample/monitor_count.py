
import proto.sample_pb2 as pb
import sys

_TIMEOUT_SECONDS = 100000

def run(addr):
    with pb.early_adopter_create_CountService_stub(addr, 8080) as stub:

        arg = pb.Request()
        count = stub.MonitorCount(arg, _TIMEOUT_SECONDS)

        for c in count:
            print(c.number)

if __name__ == '__main__':
    addr = sys.argv[1]
    run(addr)