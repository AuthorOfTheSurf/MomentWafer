package main

import (
	"github.com/AuthorOfTheSurf/TMATL/server/api"
	"github.com/AuthorOfTheSurf/TMATL/server/routes"
	"github.com/jadengore/goconfig"
	"log"
	"os"
)

func main() {
	config, err := goconfig.ReadConfigFile("config.cfg")
	port, err := config.GetString("default", "server-port")
	uri, err := config.GetString("local-test", "url")
	a := api.NewApi(uri)
	handler, err := routes.NewHandler(*a, false)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("The TMATL server is listening on port %s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
