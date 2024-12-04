from flask import Flask, render_template, request, redirect, url_for
import joblib  # Assuming you're using joblib to load your model

app = Flask(__name__)

# Load the model (replace 'model.pkl' with the path to your actual model file)
model = joblib.load('credit_card_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    form_data = [float(request.form.get(f'V{i}')) for i in range(1, 29)]
    amount = float(request.form.get('Amount'))

    # Combine form data and amount into a single input array
    input_data = form_data + [amount]

    # Make prediction using your model
    prediction = model.predict([input_data])[0]  # Assuming the model outputs 0 or 1

    # Convert prediction to readable format
    if prediction == 0:
        result = "Normal Transaction"
        color = "green"
    else:
        result = "Fraudulent Transaction"
        color = "red"

    # Redirect to the result page with the prediction result
    return redirect(url_for('result', prediction=result, color=color))

@app.route('/result')
def result():
    prediction = request.args.get('prediction')
    color = request.args.get('color')
    return render_template('result.html', prediction=prediction, color=color)

if __name__ == '__main__':
    app.run(debug=True)
