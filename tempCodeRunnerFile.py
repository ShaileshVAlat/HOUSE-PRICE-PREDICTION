from flask import Flask, render_template, request, flash
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure you have a secret key for flashing messages
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form values
    val1 = request.form.get('bedrooms')
    val2 = request.form.get('bathrooms')
    val3 = request.form.get('floors')
    val4 = request.form.get('yr_built')

    # Check if any value is empty or invalid
    if not val1 or not val2 or not val3 or not val4:
        flash('Please fill in all fields with valid values.', 'error')
        return render_template('index.html')  # Redirect back to the form

    try:
        # Convert the values to floats
        arr = np.array([float(val1), float(val2), float(val3), float(val4)])
    except ValueError:
        flash('Invalid input. Please enter valid numerical values.', 'error')
        return render_template('index.html')  # Redirect back to the form

    # Make the prediction
    pred = model.predict([arr])

    return render_template('index.html', data=int(pred[0]))


if __name__ == '__main__':
    app.run(debug=True)
