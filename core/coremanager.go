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

package core

import "sync"

type CoreConfiguration struct {

	ASNumber	int
	RouterID	string
}

var coreManager *CoreManager

type CoreManager struct {

	coreService			*CoreService
	coreConfiguration	*CoreConfiguration
	neighborsConf		[]*NeighborConfiguration
	//vrfsConf			[]*VrfsConfiguration
	started				bool

}

func initialize() {
	coreManager = new(CoreManager)
}

func GetCoreManager() (*CoreManager, error) {
	if coreManager != nil {
		return coreManager, nil
	}else {
		var err error
		return nil, err
	}
}

type CoreService struct {

	CoreConf		*CoreConfiguration
	neighborsConf	[]*NeighborConfiguration
	//vrfConf		[]*VrfConfiguration
	started			bool
}

func (coreService *CoreService) start(wg *sync.WaitGroup) {

	for {
		//core service
	}
	wg.Done()
}

func (manager *CoreManager) start(wg *sync.WaitGroup){

	coreConf := new(CoreConfiguration)
	var neighConfs []*NeighborConfiguration
	//vrfsConf = []*VrfConfiguration
	coreService := new(CoreService)
	coreService.CoreConf = coreConf
	coreService.neighborsConf = neighConfs

	manager.coreConfiguration = coreConf
	manager.neighborsConf = neighConfs
	//manager.vrfsConf = []*VrfConfiguration
	manager.coreService = coreService

	// start core service
	wg.Add(1)
	coreService.start(wg)
	wg.Wait()

}



