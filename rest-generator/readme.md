# rest-generator

This command can be used to generate code which register URL and handler.

# how to use

## for go 1.3

```shell
 cd $GOPATH/src/github.com/osrg/gobgp
 go get github.com/osrg/gobgp/rest-generator
 rest-generator ./api/rest-generator-sample.go ./api/rest-router.go
```

## for go 1.4
 We can use go generate subcommand but I'm investigating how to use it.
