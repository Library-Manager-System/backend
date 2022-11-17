from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user
from routers import admin
from routers import book
from routers import loan


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(admin.router)
app.include_router(book.router)
app.include_router(loan.router)


@app.get("/")
async def root():
    "Used to check if server is online."
    return {
        "online": True
    }
