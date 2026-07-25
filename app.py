# app.py
from flask import Flask, render_template
import random

app = Flask(__name__)

# Predefined face types
FACE_TYPES = ['male', 'female']

@app.route('/')
def index():
    # Randomly select a face type to start
    initial_face_type = random.choice(FACE_TYPES)
    return render_template('index.html', initial_face_type=initial_face_type)

if __name__ == '__main__':
    # Run the Flask app on localhost:5000
    app.run(debug=True)
