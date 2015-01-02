package service

import (
	"fmt"
	"github.com/AuthorOfTheSurf/TMATL/server/service/query"
	"github.com/AuthorOfTheSurf/TMATL/server/types"
	"time"
)

const (
	API_URL = "https://api.tmatl.com/"
)

type Svc struct {
	Query *query.Query
}

//
// Utility functions
//

// Service instances must be initialized using this method in
// order to ensure data integrity. Do not instantiate Svc directly.
func NewService(uri string) *Svc {
	return &Svc{
		query.NewQuery(uri),
	}
}

func panicIfErr(err error) {
	if err != nil {
		panic(err)
	}
}

func makeUserUrl(username string) string {
	return API_URL + "/users/" + username
}

//
// Services
//

//
// Creation
//

func (s Svc) CreateNewUser(username, email, passwordHash string) (types.SignupResponse, bool) {
	if joined, ok := s.Query.CreateUser(username, email, passwordHash); !ok {
		return time.Time{}, ok
	} else {
		return types.SignupResponse{
			Url:        makeUserUrl(username),
			Username:   username,
			Email:      email,
			Joined:     joined,
			Activities: []string{},
		}, ok
	}
}
