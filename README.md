# backend

## Install

    python -m venv env

Run the right script inside `env/Scripts/` to activate the virtual environment (according to your OS and shell)

Install dependencies:

    pip install -r requirements.txt

Copy `.env.template` to `.env` and edit it to your needs.

## Start Server

    uvicorn main:app

## Start Dev Server

    uvicorn main:app --reload

----------

# Create a admin user

`GET /admin/first-access`

- This will retur a token to:

1) Create the first admin
2) Confirm the first admin
3) Give the first admin the maximum permission

(this token will be invalid after one hour)
