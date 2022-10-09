# backend

## Install

    pip install -r requirements.txt

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
      "username": "",
      "password": ""
    }

### Response
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiIiwiaWF0IjoxLCJleHAiOjF9.EDlEYFy92fI9WBNCYyyLZkr7xUq4UyOfNMV3Akm1sn8"
    }
