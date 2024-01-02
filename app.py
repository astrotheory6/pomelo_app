from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Your Python script logic goes here
    result = {'message': 'Data from Python script'}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
