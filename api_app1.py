from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (in-memory for testing) including sensitive data for simulation
users = {
    1: {
        'name': 'John Doe',
        'email': 'john@example.com',
        'ssn': '123-45-6789',  # Example of GDPR/HIPAA violation
        'credit_card': '4111 1111 1111 1111',  # Example of PCI-DSS violation
        'health_record': 'Hypertension, medication: Amlodipine'  # HIPAA violation simulation
    },
    2: {
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'ssn': '987-65-4321',  # Example of GDPR/HIPAA violation
        'credit_card': '5500 0000 0000 0004',  # Example of PCI-DSS violation
        'health_record': 'Diabetes, medication: Metformin'  # HIPAA violation simulation
    }
}

products = {
    101: {'name': 'Laptop', 'price': 1000},
    102: {'name': 'Smartphone', 'price': 500}
}

# API Endpoint 1: Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

# API Endpoint 2: Get a user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

# API Endpoint 3: Create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    new_user = request.json
    user_id = max(users.keys()) + 1
    users[user_id] = new_user
    return jsonify({'message': 'User created', 'user_id': user_id}), 201

# API Endpoint 4: Update a product's price by product ID
@app.route('/api/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    new_price = request.json.get('price')
    if new_price:
        product['price'] = new_price
        return jsonify({'message': 'Product price updated', 'product': product})
    else:
        return jsonify({'message': 'Invalid price input'}), 400

# API Endpoint 5: Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Main entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
