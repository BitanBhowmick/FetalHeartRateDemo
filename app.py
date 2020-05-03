from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    weeks = int(request.form['weeks'])
    fhr = int(request.form['fhr'])
    mhr = int(request.form['mhr'])
    dia = int(request.form['dia'])
    sys = int(request.form['sys'])
    weight = int(request.form['weight'])
    height = int(request.form['height'])
    cp = str(request.form['cp'])
    stress = int(request.form['stress'])

    if cp == "Yes" or cp == "yes":
            cp = 1
    else:
            cp = 0

    height = (height/100)**2
    bmi = (weight/height)
    
    if (bmi<18.5):
            cor = -1
            bmi_result = "Underweight"
            print(bmi_result)
    elif 18.5<=bmi<=24.9:
            cor = 1
            bmi_result = "Normal"
            print(bmi_result)
    elif 25<=bmi<=29.9:
            cor = -1
            bmi_result = "Overweight"
            print(bmi_result)
    elif bmi>30:
            cor = -1
            bmi_result = "Obese"
            print(bmi_result)


    if 0<=stress<=35:
            out = 1
    elif 35<=stress<=45:
            out = 0.5
    elif 45<=stress<=60:
            out = 0
    elif 60<=stress<=80:
            out = -0.5
    elif stress>80:
            out = -1

    dataset = pd.read_csv('mhr fhr.csv')
    x = dataset.iloc[:, 0:5].values
    y = dataset.iloc[:, 5].values

    lin_reg = LinearRegression()
    lin_reg.fit(x, y)


    regressor = RandomForestRegressor(n_estimators = 500, random_state = 0)
    regressor.fit(x, y)


    poly_reg = PolynomialFeatures(degree = 4)
    x_poly = poly_reg.fit_transform(x)
    poly_reg.fit(x_poly, y)
    lin_reg_2 = LinearRegression()
    lin_reg_2.fit(x_poly, y)


    pred = lin_reg_2.predict(poly_reg.fit_transform([[weeks, mhr, fhr, dia, sys]]))
    output1 = (pred[0])

    y_pred = regressor.predict([[weeks, mhr, fhr, dia, sys]])

    output = (y_pred[0])

    print(output)

    output = round(output, 1)
    if(output < 0):
        output = abs(output)
        if 0 <= output <= 0.3:
            output = -0.5
            message = "CONSULT" + " " + bmi_result
            print(message)
        elif 0.3 <= output <= 0.7:
            output = -0.75
            message = "CHECK" + " " + bmi_result
            print(message)
        elif 0.7 <= output <= 1:
            output = -1
            message = "QUICK" + " " + bmi_result
            print(message)
    else:
        if 0.7 <= output <= 1:
            output = 1
            message = "GOOD" + " " + bmi_result
            print(message)
        elif 0.3 <= output <= 0.7 :
            output = 0.5
            message = "FINE" + " " + bmi_result
            print(message)
        elif 0 <= output <= 0.3 :
            output = 0
            message = "OK" + " " + bmi_result
            print(message)

    if 3 <= weeks <= 12 and fhr <=105:
        mes = "Fetal bradycardia"
        print(mes)
    elif 175 <= fhr <= 220:
        mes = "Fetal tachycardia"
        print(mes)
    else:
        mes = " "

    stress_out = np.asarray([-1,-1,-1,-1,
                         -0.5,-0.5,-0.5,-0.5,
                         0,0,0,0,
                         0.5,0.5,0.5,0.5,
                         1,1,1,1,])

    fhr_out = np.asarray([-0.9,-1,-0.7,-.81,
                      -0.2,-0.45,-0.5,-0.31,
                      0,0.1,0.05,0.02,
                      0.5,0.45,0.55,0.5,
                      1,0.99,0.95,0.96])

    out_23 = np.asarray([-1,-1,-1,-1,
                         -1,-1,-1,-1,
                         -0.5,-0.35,-0.47,-.5,
                         0,0.1,-0.1,0.03,
                         1,1,1,1])

    combined_23 = np.vstack((stress_out,fhr_out)).T


    
    regressor_23 = RandomForestRegressor(n_estimators = 300, random_state = 0)
    regressor_23.fit(combined_23, out_23)

    # Predicting a new result
    y_pred_23 = (regressor_23.predict([[stress,output]]))
    print(y_pred_23)
    a3 = str(y_pred_23[0])
    #classifier_kn = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    #classifier_kn.fit(x, y)
    #y_pred_kn = classifier_kn.predict(x)

    return (a3)


if __name__ == '__main__':
   app.run(debug = True)
