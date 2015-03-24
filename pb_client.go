package main

import (
	"fmt"
	"io"

	pb "github.com/osrg/gobgp/proto"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"log"
	"os"
	"strings"

	"github.com/peterh/liner"
)

func list() error {
	conn, err := grpc.Dial("127.0.0.1:11111")
	if err != nil {
		return err
	}
	defer conn.Close()
	client := pb.NewNeighborServiceClient(conn)

	stream, err := client.ListNeighbor(context.Background(), new(pb.RequestType))
	if err != nil {
		return err
	}
	for {
		neighbor, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}
		fmt.Println("Neighbor Address:", neighbor.Address, neighbor.State)
	}
	return nil
}

func quit() {

	fmt.Println("exit...")
	fmt.Println("")
	os.Exit(0)
}

var (
	history_fn = "/tmp/.liner_history"
	names      = []string{"neighbors"}
)

func main() {
	line := liner.NewLiner()
	defer line.Close()

	line.SetCompleter(func(line string) (c []string) {
		fmt.Println("completion: ", line)
		for _, n := range names {
			if strings.HasPrefix(n, strings.ToLower(line)) {
				c = append(c, n)
			}
		}
		return
	})

	if f, err := os.Open(history_fn); err == nil {
		line.ReadHistory(f)
		f.Close()
	}

	for {
		c, err := line.Prompt("gobgp> ")
		if err != nil {
			fmt.Printf("Unexpected error: %s\n", err)
			quit()
		}
		fields := strings.Fields(c)

		// switch on the command
		switch fields[0] {
		case "neighbors":
			list()
		case "quit":
			if f, err := os.Create(history_fn); err != nil {
				log.Print("Error writing history file: ", err)
			} else {
				line.WriteHistory(f)
				f.Close()
			}
			quit()
		}
		line.AppendHistory(c)
	}

}
