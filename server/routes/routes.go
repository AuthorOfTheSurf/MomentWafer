package routes

import (
	"github.com/AuthorOfTheSurf/TMATL/server/api"
	"github.com/ant0ine/go-json-rest/rest"
)

func NewHandler(menu api.Api, disableLogs bool) (rest.ResourceHandler, error) {
	handler := rest.ResourceHandler{
		EnableRelaxedContentType: true,
		DisableLogger:            disableLogs,
	}

	err := handler.SetRoutes(
		&rest.Route{"POST", "/signup", menu.Signup},
	)

	return handler, err
}
