package types

import (
	"time"
)

type Json map[string]interface{}
type JsonArray []Json

//
// Signup
//

type SignupForm struct {
	Username string `json:"username" validate:"username"`
	Email    string `json:"email" validate:"email"`
	Password string `json:"password" validate:"password"`
	Confirm  string `json:"confirm_password" validate:"password"`
}

type SignupResponse struct {
	Url      string    `json:"url"`
	Username string    `json:"username"`
	Email    string    `json:"email"`
	Joined   time.Time `json:"joined"`
	// will be a slice of Activities when that struct is implemented
	Activities []string `json:"activities"`
}
