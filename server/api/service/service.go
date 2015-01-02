package service

import (
	"github.com/AuthorOfTheSurf/TMATL/server/api/service/query"
	"github.com/AuthorOfTheSurf/TMATL/server/types"
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
		return types.SignupResponse{}, ok
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

//
// Read
//

func (s Svc) UsernameIsUnique(username string) bool {
	return !s.Query.UsernameExists(username)
}

func (s Svc) EmailIsUnique(email string) bool {
	return !s.Query.EmailExists(email)
}

//
// Update
//

//
// Delete
//
