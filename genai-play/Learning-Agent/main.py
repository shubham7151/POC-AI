from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.router import router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)



@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
