from fastapi import FastAPI

from routers import user
from routers import admin


app = FastAPI()

app.include_router(user.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    "Used to check if server is online."
    return {
        "online": True
    }
