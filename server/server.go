package main

import (
	"fmt"
	"github.com/AuthorOfTheSurf/TMATL/server/api"
	"github.com/AuthorOfTheSurf/TMATL/server/routes"
	"github.com/jadengore/goconfig"
	"log"
	"net/http"
)

func main() {
	config, err := goconfig.ReadConfigFile("config.cfg")
	panicIfErr(err)
	port, err := config.GetString("default", "server-port")
	panicIfErr(err)
	uri, err := config.GetString("local-test", "url")
	panicIfErr(err)
	a := api.NewApi(uri)
	handler, err := routes.NewHandler(*a, false)
	panicIfErr(err)

	http.Handle("/", &handler)
	fmt.Printf("The TMATL server is listening on port %s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func panicIfErr(err error) {
	if err != nil {
		panic(err)
	}
}
