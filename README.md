# backend

## Install

    python -m venv env

Run the right script inside `env/Scripts/` to activate the virtual environment (according to your OS and shell)

Install dependencies:

    pip install -r requirements.txt

Create a file named `.env` containging:

    secret = "secret key"
    algorithm = "HS256"
    DB_USER = "user"
    DB_PASSWORD = "password"
    DB_HOST = "host"
    DB_NAME = "db_olms"

## Start Server

    uvicorn main:app

## Start Dev Server

    uvicorn main:app --reload

----------

# API

## Is Online?

### Request

`GET /`

    Used to check if server is online

### Response
    {
      "online": true
    }

## Login

### Request

`POST /user/login`

Header

    Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiIiwiaWF0IjoxLCJleHAiOjF9.EDlEYFy92fI9WBNCYyyLZkr7xUq4UyOfNMV3Akm1sn8"

Body

    {
      "email": "string",
      "password": "string"
    }

### Response
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiIiwiaWF0IjoxLCJleHAiOjF9.EDlEYFy92fI9WBNCYyyLZkr7xUq4UyOfNMV3Akm1sn8"
    }

## Register

### Request

`POST /user/register`

Body

    {
      "name": "string",
      "email": "string",
      "password": "string",
      "phone_number": "string",
      "address": "string",
      "user_type": int
    }

### Response
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiIiwiaWF0IjoxLCJleHAiOjF9.EDlEYFy92fI9WBNCYyyLZkr7xUq4UyOfNMV3Akm1sn8"
    }
