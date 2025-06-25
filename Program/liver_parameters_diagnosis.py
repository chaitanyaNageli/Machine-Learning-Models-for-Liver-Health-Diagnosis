import pandas as pd
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load data
data = pd.read_excel('liver.xlsx')
col='Predicted Value(Out Come-Patient suffering from liver  cirrosis or not)'
data=data.dropna()
data[col]=data[col].astype(str).str.strip().str.upper().map({'YES': 1, 'NO': 0})
data['Diabetes Result']=data['Diabetes Result'].astype(str).str.strip().str.upper().map({'YES': 1, 'NO': 0})

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


y=data[col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Prediction and evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
predict=model.predict([[0,0,0,0,0,0,0,0,0,0,0,0,0]])

if predict[0]:
    print("you are suffering from liver disease")
else:
    print("you are not suffering from liver disease")



