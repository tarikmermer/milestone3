import uuid
import json
from azure.storage.queue import QueueClient
from datetime import datetime, timezone


# Replace with your Azure Storage Queue connection string
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=tmermerstorageaccount;AccountKey=H0UyAnEfrjJaqVhOGnFugcmxQJ/Cj9e60QQmg1MMEWDWNnrDAhRfmobty9RLiiUP4iP/qn5aREsQ+AStplyDyw==;EndpointSuffix=core.windows.net"
QUEUE_NAME = "stock-events"

# Initialize the QueueClient
queue_client = QueueClient.from_connection_string(CONNECTION_STRING, QUEUE_NAME)

def emit_stock_event(product_id, quantity):
    correlation_id = str(uuid.uuid4())
    message = {
        "productId": product_id,
        "quantity": quantity,
        "timestamp": datetime.now(timezone.utc).isoformat()
,
        "correlationId": correlation_id
    }

    queue_client.send_message(json.dumps(message))
    print(f"[Backend] Emitted event for {product_id} (Qty: {quantity}) | correlationId: {correlation_id}")

# Simulate stock check
if __name__ == "__main__":
    product = "SKU-123"
    current_quantity = 2  # Simulated stock value
    threshold = 5

    if current_quantity < threshold:
        emit_stock_event(product, current_quantity)
    else:
        print("Stock sufficient, no event emitted.")
