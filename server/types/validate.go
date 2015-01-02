package types

import (
	"fmt"
	"github.com/mccoyst/validate"
	"regexp"
	"unicode/utf8"
)

const (
	MIN_PASS_LENGTH     = 16
	MAX_PASS_LENGTH     = 256
	MAX_USERNAME_LENGTH = 16
	MAX_EMAIL_LENGTH    = 32
)

// Regexes
var (
	usernameRegex = regexp.MustCompile(`^[\p{L}\p{M}][\d\p{L}\p{M}]*$`)
	emailRegex    = regexp.MustCompile(`^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$`)
)

// Constructor, use this for all instantiations of validate.V
func NewValidator() *validate.V {
	return &validate.V{
		"username": validateUsername,
		"email":    validateEmail,
		"password": validatePassword,
	}
}

//
// Validation functions
//

func validateUsername(i interface{}) error {
	handle := i.(string)
	if handle == "" {
		return fmt.Errorf("Required field for signup")
	} else if utf8.RuneCountInString(handle) > MAX_USERNAME_LENGTH {
		return fmt.Errorf("Too long, max length is %d", MAX_USERNAME_LENGTH)
	} else if !usernameRegex.MatchString(handle) {
		return fmt.Errorf(handle + "contains illegal characters")
	} else {
		return nil
	}
}

func validatePassword(i interface{}) error {
	password := i.(string)
	passlen := utf8.RuneCountInString(password)
	if password == "" {
		return fmt.Errorf("Required field for signup")
	} else if passlen < MIN_PASS_LENGTH {
		return fmt.Errorf("Too short, minimum length is %d", MIN_PASS_LENGTH)
	} else if passlen > MAX_PASS_LENGTH {
		return fmt.Errorf("Too long, maximum length is %d", MAX_USERNAME_LENGTH)
	} else {
		return nil
	}
}

func validateEmail(i interface{}) error {
	email := i.(string)
	if email == "" {
		return fmt.Errorf("Required field for signup")
	} else if utf8.RuneCountInString(email) > MAX_EMAIL_LENGTH {
		return fmt.Errorf("Too long, maximum length is %d", MAX_EMAIL_LENGTH)
	} else if !emailRegex.MatchString(email) {
		return fmt.Errorf(email + " is an invalid email")
	} else {
		return nil
	}
}
