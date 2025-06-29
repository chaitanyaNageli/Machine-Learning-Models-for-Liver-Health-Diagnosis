from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get values from form
    try:
        age = int(request.form['age'])
        duration = int(request.form['duration'])
        quantity = int(request.form['quantity'])
        diabetes = int(request.form['diabetes'])
        polymorphs = int(request.form['polymorphs'])
        lymphocytes = int(request.form['lymphocytes'])
        monocytes = int(request.form['monocytes'])
        eosinophils = int(request.form['eosinophils'])
        albumin = float(request.form['albumin'])
        globulin = float(request.form['globulin'])
        al_phosphatase = float(request.form['al_phosphatase'])
        sgot = int(request.form['sgot'])
        sgpt = int(request.form['sgpt'])
    except ValueError:
        return "Please enter valid numeric values in all fields."

    # Load and prepare data
    data = pd.read_excel('liver.xlsx')
    col = 'Predicted Value(Out Come-Patient suffering from liver  cirrosis or not)'
    data = data.dropna()
    data[col] = data[col].astype(str).str.strip().str.upper().map({'YES': 1, 'NO': 0})
    data['Diabetes Result'] = data['Diabetes Result'].astype(str).str.strip().str.upper().map({'YES': 1, 'NO': 0})

    # Features and labels
    X = data[['Age', 'Duration of alcohol consumption(years)',
              'Quantity of alcohol consumption (quarters/day)',
              'Diabetes Result', 
              'Polymorphs  (%) ',
              'Lymphocytes  (%)',
              'Monocytes   (%)', 
              'Eosinophils   (%)', 
              'Albumin   (g/dl)',
              'Globulin  (g/dl)',
              'AL.Phosphatase      (U/L)',
              'SGOT/AST      (U/L)', 
              'SGPT/ALT (U/L)']]
    
    y = data[col]

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predict using real user input
    user_input = [[
        age, duration, quantity, diabetes,
        polymorphs, lymphocytes, monocytes, eosinophils,
        albumin, globulin, al_phosphatase, sgot, sgpt
    ]]
    acc=accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc*100}%")
    prediction = model.predict(user_input)
    result="NO"
    if prediction[0] == 1:
        result = "⚠️ You might be suffering from liver cirrhosis."
    else:
        result = "✅ You are not likely suffering from liver cirrhosis."

    return render_template("result.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
