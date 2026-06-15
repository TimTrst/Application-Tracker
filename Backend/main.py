from fastapi import FastAPI
from routes.applications import router as application_router
from routes.statuses import router as status_router
from routes.phases import router as phase_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


app.include_router(router=application_router, prefix="/api/applications")
app.include_router(router=status_router, prefix="/api/statuses")
app.include_router(router=phase_router, prefix="/api/phases")

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
