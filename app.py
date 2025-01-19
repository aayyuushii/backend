from flask import Flask, request, jsonify
from emails import emails_bp
from combiner import combiner_bp
from pitch import pitch_bp
import shared_data

app = Flask(__name__)

# Register blueprints
app.register_blueprint(emails_bp, url_prefix='/emails')
app.register_blueprint(combiner_bp, url_prefix='/combiner')
app.register_blueprint(pitch_bp, url_prefix='/pitch')

@app.route('/input', methods=['POST'])
def receive_input():
    """
    Receive input data, store it in shared_data, and send a success message.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    shared_data.shared_input["data"] = data.get("input")
    return jsonify({"message": "Input data stored successfully"})

if __name__ == '__main__':
    app.run(debug=True)
