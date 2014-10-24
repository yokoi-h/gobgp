// bgp_config
package config

import (
	"sync"
)

type RServer struct {
	Router_id string
	Local_as  string
}
type Neighbor struct {
	Neighbor_id string
	Ip_address  string
	Remote_as   string
}
type Neighbors struct {
	sync.RWMutex
	Store map[string]*Neighbor
}
type Path struct {
	Network   string
	Next_hop  string
	Metric    int
	Loc_Prf   int
	Weight    int
	As_path   string
	Community string
}
type LocRib struct {
	Neighbor_id string
	Path_map    map[string]*Path
}
