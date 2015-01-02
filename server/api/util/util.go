package util

import (
	"github.com/AuthorOfTheSurf/TMATL/server/types"
)

type Util struct{}

func (u Util) SimpleJsonReason(w rest.ResponseWriter, code int, message string) {
	w.WriteHeader(code)
	w.WriteJson(types.Json{
		"reason": message,
	})
}
