package main

import (
	"fmt"
	"golang.org/x/net/context"
	"log"
	"net"
	"sync"

	"google.golang.org/grpc"

	pb "./proto"
)

type countService struct {
	count  int32
	mu     sync.Mutex
	chList []chan int32
}

func NewCountService() *countService {
	s := &countService{}
	s.chList = []chan int32{}
	return s
}

func handleResponse(responseCh chan int32, stream pb.CountService_MonitorCountServer) error {

	for number := range responseCh {
		count := &pb.Count{Number: number}
		if err := stream.Send(count); err != nil {
			return err
		}
	}
	return nil
}

func (s *countService) MonitorCount(p *pb.Request, stream pb.CountService_MonitorCountServer) error {

	ch := make(chan int32, 8)
	s.mu.Lock()
	s.chList = append(s.chList, ch)
	s.mu.Unlock()

	return handleResponse(ch, stream)
}

func (s *countService) AddCount(ctx context.Context, c *pb.Count) (*pb.Error, error) {

	s.mu.Lock()
	s.count += c.Number
	fmt.Println("current = ", s.count)
	defer s.mu.Unlock()
	for _, ch := range s.chList {
		ch <- s.count
	}

	return &pb.Error{Code: 0}, nil
}

func main() {
	listen, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	server := grpc.NewServer()
	pb.RegisterCountServiceServer(server, NewCountService())
	server.Serve(listen)
}
