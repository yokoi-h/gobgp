// core_manager.go
package main

import (
	"fmt"
	"gobgp/config"
	"time"
)

/*
	make chanel
	c_rs
	  ->RouteServer Configration channel
	c_ne
	  ->Neighbors Configration channel
*/
//var c_rs = make(chan *config.RServer)
//var c_ne = make(chan *config.Neighbors)

func thread_manager() {
	fmt.Println("config_manager_th start")

	go config_manager_th()
	time.Sleep(10 * time.Minute)

	fmt.Println("config_manager_th end")
}

func config_manager_th() {
	config.Config_for_Rest()
}
