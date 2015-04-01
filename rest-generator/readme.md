# rest-generator

This command can be used to generate code which register URL and handler.

# how to use

## for go 1.3

```shell
 cd $GOPATH/src/github.com/osrg/gobgp
 go get github.com/osrg/gobgp/rest-generator
 rest-generator ./api/rest-generator-sample.go ./api/rest-router.go
```

rest-generator generates rest-router.go automatically.
You can find it under the api directory.

## for go 1.4
```shell
 cd $GOPATH/src/github.com/osrg/gobgp
 go get github.com/osrg/gobgp/rest-generator
 cd $GOPATH/src/github.com/osrg/gobgp/api
 go generate
```
