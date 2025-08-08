import json
import requests
import os
import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="QueueTriggerStockEvent")
@app.queue_trigger(arg_name="msg", 
                   queue_name="stock-events",
                   connection="AzureWebJobsStorage")
def main(msg: func.QueueMessage):
    message_body = msg.get_body().decode('utf-8')
    logging.info(f"Received message: {message_body}")

    try:
        message_json = json.loads(message_body)
        # Accept both snake_case and camelCase
        product = message_json.get('product') or message_json.get('productId')
        quantity = message_json.get('quantity')
        correlation_id = message_json.get('correlation_id') or message_json.get('correlationId')

        supplier_url = os.getenv("SUPPLIER_API_URL", "http://localhost:8000/restock")

        headers = {
            "x-correlation-id": correlation_id,
            "Content-Type": "application/json"
        }

        data = {
            "product": product,
            "quantity": quantity
        }

        response = requests.post(supplier_url, json=data, headers=headers)
        response.raise_for_status()
        logging.info(f"Successfully called supplier API: {response.text}")

    except Exception as e:
        logging.error(f"Error processing message: {e}")
