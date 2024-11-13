from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import random

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        user='admin1',
        password='Tanyater1904',
        host='databaseht.cby28wu4wa26.eu-north-1.rds.amazonaws.com',
        database='databaseht'
    )

# Create table for recipes
@app.route('/create_table', methods=['POST'])
def create_table():
    conn = None
    cursor = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip_address VARCHAR(45) NOT NULL,
                recipe_text TEXT NOT NULL
            )
        """)
        print("created")
        return jsonify({"message": "Table 'recipe' created successfully!"}), 201
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Add a new recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    ip_address = data.get('ip_address')
    recipe_text = data.get('recipe_text')
    
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipe (ip_address, recipe_text) VALUES (%s, %s)", (ip_address, recipe_text))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recipe added successfully!"}), 201

# Add a random recipe for testing purposes
@app.route('/add_random_recipe', methods=['POST'])
def add_random_recipe():
    ip_address = "192.168.1." + str(random.randint(1, 255))  # Generate a random IP-like string
    random_recipe_texts = [
        "Spaghetti Carbonara Recipe",
        "Chicken Curry Recipe",
        "Vegetable Stir Fry Recipe",
        "Chocolate Cake Recipe",
        "Classic Caesar Salad Recipe"
    ]
    recipe_text = random.choice(random_recipe_texts)

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipe (ip_address, recipe_text) VALUES (%s, %s)", (ip_address, recipe_text))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Random recipe added successfully!", "recipe": {"ip_address": ip_address, "recipe_text": recipe_text}}), 201

# Get all recipes
@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipe")
    recipes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Format data for the response
    recipes_list = [{"id": recipe[0], "ip_address": recipe[1], "recipe_text": recipe[2]} for recipe in recipes]
    
    return jsonify(recipes_list), 200

# Delete all recipes
@app.route('/recipes', methods=['DELETE'])
def delete_all_recipes():
    conn = None
    cursor = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipe")
        conn.commit()  # Confirm changes
        return jsonify({"message": "All recipes deleted successfully!"}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"}), 200

# Run the server
if __name__ == '__main__':
    with app.app_context():
        create_table()
    app.run(host='0.0.0.0', port=5000)  # Adjust the port if needed
