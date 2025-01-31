from fastapi import FastAPI
from app.db.init_db import init_db
from app.db.session import engine
from app.api.v1 import users, books, inventory

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

# initialize a database
init_db(engine)

# include routes
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])