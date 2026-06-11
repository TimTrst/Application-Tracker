from fastapi import FastAPI
from routes.applications import router as application_router
from routes.statuses import router as status_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router=application_router, prefix="/api/applications")
app.include_router(router=status_router, prefix="/api/statuses")
