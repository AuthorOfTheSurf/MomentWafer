package util

import (
	"github.com/AuthorOfTheSurf/TMATL/server/types"
	"github.com/ant0ine/go-json-rest/rest"
)

type Util struct{}

func (u Util) SimpleJsonReason(w rest.ResponseWriter, code int, message string) {
	w.WriteHeader(code)
	w.WriteJson(types.Json{
		"reason": message,
	})
}

func (u Util) SimpleValidationReason(w rest.ResponseWriter, code int, err []error) {
	errorMessage := decodeValidatorErrors(err)
	w.WriteHeader(code)
	w.WriteJson(types.Json{
		"reason": errorMessage,
	})
}

func (u Util) PatchValidationReason(w rest.ResponseWriter, code int, err []error, index int) {
	errorMessage := decodeValidatorErrors(err)
	w.WriteHeader(code)
	w.WriteJson(types.Json{
		"index":  index,
		"reason": errorMessage,
	})
}

// Validation helper
func decodeValidatorErrors(err []error) []string {
	errorMessage := make([]string, len(err))
	for i := range err {
		errorMessage[i] = err[i].Error()
	}
	return errorMessage
}
