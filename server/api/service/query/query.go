package query

import (
	"github.com/dchest/uniuri"
	"github.com/jmcvetta/neoism"
	"time"
)

type Query struct {
	Db *neoism.Database
}

// Constructor, use this for all instantiations of Query
func NewQuery(uri string) *Query {
	neo4jdb, err := neoism.Connect(uri)
	panicIfErr(err)
	return &Query{neo4jdb}
}

//
// Utility functions
//

// Preforms a Cypher query, catching any unexpected behavior in a panic.
// It is ok to panic in this case as a panic at the db query level almost
// always indicates an incorrectly constructed query.
func (q Query) cypherOrPanic(query *neoism.CypherQuery) {
	panicIfErr(q.Db.Cypher(query))
}

func panicIfErr(err error) {
	if err != nil {
		panic(err)
	}
}

//
// Calculated Values
//

func Now() time.Time {
	return time.Now().Local()
}

func NewUUID() string {
	return uniuri.NewLen(uniuri.UUIDLen)
}

//
// Create
//

func (q Query) CreateUser(username, email, passwordHash string) (time.Time, bool) {
	created := []struct {
		Joined time.Time `json:"joined"`
	}{}
	now := Now()
	q.cypherOrPanic(&neoism.CypherQuery{
		Statement: `
			CREATE (u:User {
				username: {username},
				email: {email},
				password: {password},
				joined: {joined}
			})
			RETURN u.joined AS joined
		`,
		Parameters: neoism.Props{
			"username": username,
			"email":    email,
			"password": passwordHash,
			"joined":   now,
		},
		Result: &created,
	})
	if ok := len(created) > 0; !ok {
		return time.Time{}, ok
	} else {
		return now, ok
	}
}

//
// Read
//

func (q Query) UsernameExists(username string) bool {
	found := []struct {
		Username string `json:"username"`
	}{}
	q.cypherOrPanic(&neoism.CypherQuery{
		Statement: `
			MATCH   (u:User)
			WHERE   u.username = {username}
			RETURN  u.username AS username
		`,
		Parameters: neoism.Props{
			"username": username,
		},
		Result: &found,
	})
	return len(found) > 0
}

func (q Query) EmailExists(email string) bool {
	found := []struct {
		Email string `json:"email"`
	}{}
	q.cypherOrPanic(&neoism.CypherQuery{
		Statement: `
			MATCH   (u:User)
			WHERE   u.email = {email}
			RETURN  u.email AS email
		`,
		Parameters: neoism.Props{
			"email": email,
		},
		Result: &found,
	})
	return len(found) > 0
}

//
// Update
//

//
// Delete
//
