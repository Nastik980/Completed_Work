from flask import Flask, request, jsonify

app = Flask(__name__)

# Обробник GET-запиту
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"

# Обробник з параметрами в URL
@app.route("/currency", methods=["GET"])
def get_currency():
    param = request.args.get("param", "default")
    if param == "today":
        return "USD - 41,5"
    elif param == "yesterday":
        return "USD - 41,0"
    else:
        return "Invalid parameter"

# Обробник із заголовками
@app.route("/content", methods=["GET"])
def content():
    content_type = request.headers.get("Content-Type", "text/plain")
    if content_type == "application/json":
        return jsonify({"message": "This is JSON"})
    elif content_type == "application/xml":
        return "<message>This is XML</message>", 200, {'Content-Type': 'application/xml'}
    else:
        return "This is plain text"

if __name__ == '__main__':
    app.run(port=8000)
