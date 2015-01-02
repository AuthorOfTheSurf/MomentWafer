# Tracking Muscle Activation Through Layers API

This is the API of the TMATL project


This is an all-JSON API. All requests and responses, except those transferring audio, image, or video content, must have a content-type header set to `application/json`.

All endpoints except signup (`POST /users`) and login (`POST /sessions`) require an `Authorization` header in which you pass in the token that you previously received from a successful login request. For example:

    Authorization: Token 1234567812345678

If the authorization header is missing, or the token is invalid or expired, an HTTP 401 response is returned. After receiving a 401, a client should try to login (`POST /sessions`) again to obtain a new token.

# Group Users

## Signup [/users]

### Signup New Users [POST]
Create a new user with the posted data. The new account will be ready for use upon success.
+ Request
        
        {
            "username": "kobe24",
            "email": "kobe@bball.com",
            "password": "24blackmamba8",
            "confirm_password": "24blackmamba8"
        }
+ Response 201

        {
            "url": "https://api.tmatl.com/users/kobe24",
            "username": "kobe24",
            "email": "kobe@bball.com",
            "joined": "2015-01-02T14:16:01Z",
            "activities": []
        }
+ Response 400

        {
            "reason": ("malformed json"
                      |"username is a required field for signup"
                      |"email is a required field for signup"
                      |"Passwords do no match"
                      |"Passwords must be at least 16 characters long")
        }

+ Response 409

        {
            "reason": "username or email is already taken"
        }

