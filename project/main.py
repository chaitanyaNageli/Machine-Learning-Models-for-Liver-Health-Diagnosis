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
        polymorphs = float(request.form['polymorphs'])
        lymphocytes = float(request.form['lymphocytes'])
        monocytes = float(request.form['monocytes'])
        eosinophils = float(request.form['eosinophils'])
        albumin = float(request.form['albumin'])
        globulin = float(request.form['globulin'])
        al_phosphatase = float(request.form['al_phosphatase'])
        sgot = int(request.form['sgot'])
        sgpt = int(request.form['sgpt'])
    except ValueError:
        return "Please enter valid numeric values in all fields."

   
    data = pd.read_excel('liver.xlsx')
    data=data.dropna()

    data = data.applymap(lambda x: 1 if str(x).strip().upper() == 'YES' else (0 if str(x).strip().upper() == 'NO' else x))

    columns=data.columns
    X=data[columns[:-1]]

    y=data[columns[-1]]


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    
    user_input = [[
        age, duration, quantity, diabetes,
        polymorphs, lymphocytes, monocytes, eosinophils,
        albumin, globulin, al_phosphatase, sgot, sgpt
    ]]

    prediction = model.predict(user_input)
    result="NO"
    if prediction[0] == 1:
        result = "You might be suffering from liver cirrhosis."
    else:
        result = " You are not likely suffering from liver cirrhosis."

    return render_template("result.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
