"""
Main FastAPI application file.
Define your FastAPI app and include routers here.
"""
from fastapi import FastAPI
from app.routes.users import user_route 
from app.routes.conversation import conversation_routes
app = FastAPI()

# Include your routers here
# from app.routes import users, items
app.include_router(user_route)
app.include_router(conversation_routes)

from app.db.base import Base, get_session, engine

Base.metadata.create_all(bind=engine) 

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
