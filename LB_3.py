from flask import Flask, jsonify, request, abort, Response

app = Flask(__name__)

# Дані користувачів для Basic Authentication
users = {
    "admin": "password123",
    "user": "userpass"
}

# Каталог товарів (словар для [Easy] реалізації)
catalog = {
    1: {"name": "Arabica", "price": 100.25, "color": "Brown"},
    2: {"name": "Robusta", "price": 80.50, "color": "Black"}
}


# Функція перевірки автентифікації
def check_auth(username, password):
    """Перевірка автентифікації"""
    return username in users and users[username] == password


def authenticate():
    """Відповідь для невірної автентифікації"""
    return Response(
        "Access Denied: Invalid credentials\n", 401,
        {"WWW-Authenticate": "Basic realm='Login Required'"}
    )


@app.before_request
def require_auth():
    """Вимагати автентифікацію для кожного запиту"""
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()


# Ендпоінт /items для роботи з усіма товарами
@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        # Повернути каталог товарів
        return jsonify(catalog)

    if request.method == 'POST':
        # Додати новий товар
        new_item = request.get_json()
        if not new_item or "name" not in new_item or "price" not in new_item or "color" not in new_item:
            abort(400, "Invalid item data. 'name', 'price', and 'color' are required.")
        new_id = max(catalog.keys()) + 1 if catalog else 1
        catalog[new_id] = {
            "name": new_item["name"],
            "price": new_item["price"],
            "color": new_item["color"]
        }
        return jsonify({"id": new_id}), 201


# Ендпоінт /items/<id> для роботи з конкретним товаром
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item(item_id):
    if item_id not in catalog:
        abort(404, "Item not found.")

    if request.method == 'GET':
        # Отримати інформацію про товар
        return jsonify(catalog[item_id])

    if request.method == 'PUT':
        # Оновити товар
        updated_item = request.get_json()
        if not updated_item or "name" not in updated_item or "price" not in updated_item or "color" not in updated_item:
            abort(400, "Invalid item data. 'name', 'price', and 'color' are required.")
        catalog[item_id] = {
            "name": updated_item["name"],
            "price": updated_item["price"],
            "color": updated_item["color"]
        }
        return jsonify({"message": "Item updated successfully."})

    if request.method == 'DELETE':
        # Видалити товар
        del catalog[item_id]
        return jsonify({"message": "Item deleted successfully."})


if __name__ == '__main__':
    app.run(port=5000)
