from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/{}'.format(TOKEN), methods=['POST'])
# Define a health check route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
