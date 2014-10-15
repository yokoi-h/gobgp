// Copyright (C) 2014 Nippon Telegraph and Telephone Corporation.
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

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"log/syslog"
	"net"
	"os"
	"strconv"
	"github.com/osrg/gobgp/core"
	"sync"
)

const (
	DEFAULT_BGP_PORT = "179"
	EXIT_ERROR = 1
)

type NeighborConfiguration struct {

	ASNumber	int
	PeerAddress	net.Addr
	IPv4Enable	bool
	IPv6Enable	bool
	VPNv4Enable	bool
	VPNv6Enable	bool
	RouteServerClient	bool
}


type BGPProcessor struct {

	coreManager			*core.CoreManager
	destChannel			*chan Destination
	rtdestChannel		*chan Destination
	WorkUnitsPerCycle	int

}

func (processor *BGPProcessor) start(destChannel, rtdestChannel chan Destination){

	processor.destChannel = destChannel
	processor.rtdestChannel = rtdestChannel

	for {
		select{
		case dest := <- destChannel:
			processor.processDest(dest)
		case rtdest := <- rtdestChannel:
			processor.processRtdest(rtdest)
		}
	}
}

func (processor *BGPProcessor) Enqueue(dest Destination){

	if dest.RouteFamily == "RTC_UC" {
		processor.rtdestChannel <- dest
	} else {
		processor.destChannel <- dest
	}
}

func (processor *BGPProcessor) processDest(dest Destination) error {

	// do something
	return nil
}

func (processor *BGPProcessor) processRtdest(dest Destination) error {

	// do something
	return nil
}


type Destination struct {

	RouteFamily	string
	Nlri		net.Addr

}

type Peer struct {

	NeighborConf	NeighborConfiguration
}


func main(){

	ASNumber, err := strconv.Atoi(os.Args[1])
	if err != nil {
		os.Exit(EXIT_ERROR)
	}
	RouterID := os.Args[2]
	PeerAddress := net.ParseIP(os.Args[3])
	RemoteASNumber, err := strconv.Atoi(os.Args[4])
	if err != nil {
		os.Exit(EXIT_ERROR)
	}

	coreConf := new(core.CoreConfiguration)
	coreConf.ASNumber = ASNumber
	coreConf.RouterID = RouterID

	neighConf := new(NeighborConfiguration)
	neighConf.ASNumber = RemoteASNumber
	neighConf.IPv4Enable = true
	neighConf.PeerAddress = PeerAddress

}


