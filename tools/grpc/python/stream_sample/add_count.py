import proto.sample_pb2 as pb
import sys


_TIMEOUT_SECONDS = 3

def run(addr, number):
    with pb.early_adopter_create_CountService_stub(addr, 8080) as stub:

        arg = pb.Count(number=int(number))
        ret = stub.AddCount(arg, _TIMEOUT_SECONDS)

        if ret.code == 0:
            print "Success!"
        else:
            print "Error!"


if __name__ == '__main__':
    addr = sys.argv[1]
    number = sys.argv[2]
    run(addr, number)

