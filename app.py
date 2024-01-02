from flask import Flask, jsonify
import json
from summarize import summarize
import time
app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': 123}

@app.route('/api/data', methods=['GET'])
def get_data():
    # Your Python script logic goes here
    try:
        with open('ex.json', 'r') as file:
            inputJSON = json.load(file)
            summary = summarize(inputJSON)
            result = {'message': summary}
            return jsonify(result)
    except FileNotFoundError:
        result = {'message': 'File not found'}
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)