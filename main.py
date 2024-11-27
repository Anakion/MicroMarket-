import uvicorn
from fastapi import FastAPI
from app.routers import category, products

app = FastAPI()


@app.get("/")
async def welcome_market() -> dict:
    return {"message": "Welcome to MicroMarket"}


app.include_router(category.router)
app.include_router(products.router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)