import gobgp_pb2
import sys
from ryu.lib.packet.bgp import BGPPathAttributeOrigin
from ryu.lib.packet.bgp import IPAddrPrefix
from ryu.lib.packet.bgp import BGPPathAttributeNextHop


_TIMEOUT_SECONDS = 10
Resource_VRF = 10

def run(gobgpd_addr, vrf_name):
    with gobgp_pb2.early_adopter_create_GobgpApi_stub(gobgpd_addr, 8080) as stub:

        paths = []
        nlri = IPAddrPrefix(addr="30.31.0.0", length=24)
        bin_nlri = nlri.serialize()

        nexthop = BGPPathAttributeNextHop(value="0.0.0.0")
        bin_nexthop = nexthop.serialize()

        origin = BGPPathAttributeOrigin(value=2)
        bin_origin = origin.serialize()

        path = {}
        pattrs = []
        pattrs.append(str(bin_nexthop))
        pattrs.append(str(bin_origin))

        path['nlri'] = str(bin_nlri)
        path['pattrs'] = pattrs
        paths.append(path)

        args = []
        args.append(gobgp_pb2.ModPathArguments(resource=Resource_VRF, name=vrf_name, paths=paths))
        ret = stub.ModPath(args, _TIMEOUT_SECONDS)

        if ret.code == 0:
            print "Success!"
        else:
            print "Error!"


if __name__ == '__main__':
    gobgp = sys.argv[1]
    vrf_name = sys.argv[2]
    run(gobgp, vrf_name)

