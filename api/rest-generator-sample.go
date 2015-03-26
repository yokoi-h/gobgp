//go:generate rest-generator $FILE rest-router.go
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
	"net/http"
)

// @rest:/v1/bgp/neighbors
func (rs *RestServer) getNeighbors(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}
func (rs *RestServer) getNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}
func (rs *RestServer) postNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}
func (rs *RestServer) putNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}
func (rs *RestServer) deleteNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}/adj-rib-in/{routeFamily}
func (rs *RestServer) getAdjRibInNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}/adj-rib-out/{routeFamily}
func (rs *RestServer) getAdjRibOutNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}

// @rest:/v1/bgp/neighbor/{remotePeerAddr}/local-rib/{routeFamily}
func (rs *RestServer) getLocalRibNeighbor(w http.ResponseWriter, r *http.Request) {
	rs.neighbor(w, r, REQ_NEIGHBOR)
}
