import logging
from fastapi.responses import JSONResponse

async def handle_restock_request(product, quantity, correlation_id):
    logging.info(f"Received restock request: product={product}, quantity={quantity}, correlation_id={correlation_id}")

    return JSONResponse(content={
        "message": f"Restock received for product {product}",
        "correlation_id": correlation_id
    })
