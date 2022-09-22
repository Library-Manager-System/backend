# backend

## Install

    pip install "uvicorn[standard]"
    pip install fastapi

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

