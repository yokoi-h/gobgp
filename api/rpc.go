// Copyright (C) 2014,2015 Nippon Telegraph and Telephone Corporation.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
// implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package api

import (
	log "github.com/Sirupsen/logrus"
	"github.com/osrg/gobgp/packet"
	pb "github.com/osrg/gobgp/proto"
	"google.golang.org/grpc"
	"net"
	"strconv"
)

const RPC_PORT = 11111

type RpcRequest struct {
	RequestType int
	RemoteAddr  string
	RouteFamily bgp.RouteFamily
	ResponseCh  chan *RpcResponse
	Err         error
}

func NewRpcRequest(reqType int, remoteAddr string, rf bgp.RouteFamily) *RpcRequest {
	r := &RpcRequest{
		RequestType: reqType,
		RouteFamily: rf,
		RemoteAddr:  remoteAddr,
		ResponseCh:  make(chan *RpcResponse),
	}
	return r
}

type RpcResponse struct {
	ResponseErr error
	Data        []interface{}
}

type RpcServer struct {
	port        int
	bgpServerCh chan *RpcRequest
}

func NewRpcServer(port int, bgpServerCh chan *RpcRequest) *RpcServer {
	rs := &RpcServer{
		port:        port,
		bgpServerCh: bgpServerCh}
	return rs
}

func (rs RpcServer) ListNeighbor(p *pb.RequestType, stream pb.NeighborService_ListNeighborServer) error {

	// get neighbor addresses
	req := NewRpcRequest(REQ_NEIGHBORS, "", 0)
	rs.bgpServerCh <- req

	res := <-req.ResponseCh
	for _, item := range res.Data {
		log.Debugf("item: %v", item)
		n := item.(*pb.Neighbor)
		if err := stream.Send(n); err != nil {
			return err
		}
	}
	return nil
}

func (rs *RpcServer) Serve() {
	lis, err := net.Listen("tcp", ":"+strconv.Itoa(rs.port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	server := grpc.NewServer()

	pb.RegisterNeighborServiceServer(server, *rs)
	server.Serve(lis)
}
