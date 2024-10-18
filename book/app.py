# app.py

from flask import Flask, request, render_template, jsonify
import json
import os
from model import analyze_financial_data

app = Flask(__name__)



@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    file = request.files.get('data_file')

    if file is None:
        return "Missing file: Please upload a file with the name 'data_file'.", 400

    try:
        data = json.load(file)  # Load the JSON data
        print("Data received for analysis:", data)  # Debugging line

        result = analyze_financial_data(data)
        return jsonify(result)

    except ValueError as ve:
        return str(ve), 400  # Return error message for invalid value
    except json.JSONDecodeError:
        return "Invalid JSON format", 400  # Return error message for JSON decode error
    except Exception as e:
        return str(e), 500  # Return generic error message

if __name__ == '__main__':
    app.run(debug=True)
