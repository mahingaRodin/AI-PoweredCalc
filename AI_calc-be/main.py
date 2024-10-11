from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from constants import SERVER_URL, PORT
from apps.calculator.route import router as calculator_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health():
    return {'message': 'Server is running'}

app.include_router(calculator_router, prefix='/calculate', tags=['calculate'])

if __name__ == '__main__':
    uvicorn.run(app, host=SERVER_URL, port=PORT)
