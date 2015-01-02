package api

import (
	"github.com/AuthorOfTheSurf/TMATL/server/api/service"
	"github.com/AuthorOfTheSurf/TMATL/server/api/util"
	"github.com/AuthorOfTheSurf/TMATL/server/types"
	"github.com/ChimeraCoder/go.crypto/bcrypt"
	"github.com/ant0ine/go-json-rest/rest"
	"github.com/mccoyst/validate"
)

type Api struct {
	Svc       *service.Svc
	Validator *validate.V
	Util      *util.Util
}

// Constructor, use this for all instantiations of Api
func NewApi(uri string) *Api {
	return &Api{
		Svc:       service.NewService(uri),
		Validator: types.NewValidator(),
		Util:      &util.Util{},
	}
}

//
// Users
//

func (a Api) Signup(w rest.ResponseWriter, r *rest.Request) {
	form := types.SignupForm{}

	if err := r.DecodeJsonPayload(&form); err != nil {
		rest.Error(w, "malformed json", 500)
		return
	}

	if err := a.Validator.ValidateAndTag(form, "json"); err != nil {
		a.Util.SimpleValidationReason(w, 400, err)
		return
	}

	username := form.Username
	email := form.Email
	password := form.Password
	confirm := form.Confirm

	if password != confirm {
		a.Util.SimpleJsonReason(w, 400, "passwords do not match")
		return
	}

	if ok := a.Svc.UsernameIsUnique(username); !ok {
		a.Util.SimpleJsonReason(w, 409, "username or email is already taken")
		return
	}

	if ok := a.Svc.EmailIsUnique(email); !ok {
		a.Util.SimpleJsonReason(w, 409, "username or email is already taken")
		return
	}

	if hash, err := bcrypt.GenerateFromPassword([]byte(password), 10); err != nil {
		rest.Error(w, err.Error(), 500)
		return
	} else {
		if json, ok := a.Svc.CreateNewUser(username, email, string(hash)); !ok {
			a.Util.SimpleJsonReason(w, 500, "Unexpected failure to create new user")
			return
		} else {
			w.WriteHeader(201)
			w.WriteJson(json)
		}
	}
}
