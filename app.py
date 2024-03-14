from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Assuming a simple JSON file for storing data
DB_FILE = 'customers.json'

def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as file:
        return json.load(file)

def write_db(data):
    with open(DB_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/api/customers', methods=['POST'])
def register_customer():
    customer_data = request.json
    customers = read_db()
    customers.append(customer_data)
    write_db(customers)
    return jsonify(customer_data), 201

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = read_db()
    return jsonify(customers), 200

@app.route('/api/customers/aadhar/<customer_id>', methods=['PATCH'])
def update_customer(customer_id):
    try:
        update_data = request.json
        customers = read_db()
        customer_index = next((i for i, customer in enumerate(customers) if customer['adharNumber'] == customer_id), None)
        
        if customer_index is None:
            return jsonify({"error": "Customer not found."}), 404
        
        for key, value in update_data.items():
            if key in customers[customer_index]:
                customers[customer_index][key] = value
        
        write_db(customers)
        return jsonify(customers[customer_index]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
