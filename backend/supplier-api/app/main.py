from fastapi import FastAPI, Request
from app.supplier import handle_restock_request  # ✅ Correct import
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI()

@app.post("/restock")
async def restock(request: Request):
    data = await request.json()
    product = data.get("product")
    quantity = data.get("quantity")
    correlation_id = request.headers.get("x-correlation-id")

    response = await handle_restock_request(product, quantity, correlation_id)
    return response
