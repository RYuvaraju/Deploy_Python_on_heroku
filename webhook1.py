from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources={r"/webhook": {"origins": "*"}})  # Allow all origins for the /webhook endpoint

# Set up logging
logging.basicConfig(level=logging.INFO)

# The secret key to validate the webhook sender
SECRET_KEY = "6b388568526be0cb94c206e37460ff4f"       # 6b388568526be0cb94c206e37460ff4f


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Check if the secret key is valid
    secret_key = request.headers.get('X-Webhook-Secret')
    if secret_key != SECRET_KEY:
        app.logger.error('Invalid secret key.')
        return jsonify({'message': 'Forbidden: Invalid secret'}), 403

    # Get the JSON data sent by ServiceNow
    webhook_data = request.json

    # Log the received data (for debugging purposes)
    app.logger.info('Received webhook data: %s', webhook_data)

    # Extract incident details
    incident_number = webhook_data.get("incident_number")
    description = webhook_data.get("description")
    priority = webhook_data.get("priority")
    category = webhook_data.get("category")

    print(f"Incident Number: {incident_number}")
    print(f"Description: {description}")
    print(f"Priority: {priority}")
    print(f"Category: {category}")

    # Respond to acknowledge receipt of the webhook
    return jsonify({'message': 'Webhook received successfully, webhook is working'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
