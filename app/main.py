"""
Main FastAPI application file.
Define your FastAPI app and include routers here.
"""
from fastapi import FastAPI

from app.config.settings import Base, engine
from app.routes.conversation import conversation_routes
from app.routes.users import user_route

app = FastAPI()

# Include your routers here
# from app.routes import users, items
app.include_router(user_route)
app.include_router(conversation_routes)



Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    '''Root Endpoint'''
    return {"message": "View /docs for Documentation "}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
