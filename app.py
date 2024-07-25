from flask import Flask,render_template,url_for,request
import joblib,os,pandas,sqlite3



model_1=joblib.load("./models/decision_tree.lb")
model_2=joblib.load("./models/linear_model.lb")
model_3=joblib.load("./models/randomforest.lb")


app=Flask(__name__)

data_insert_query = """
insert into project (age,gender,bmi,children,region,smoker,health,prediction)
values(?,?,?,?,?,?,?,?)
"""

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=="POST":
        age=request.form['age']
        region=request.form['region']
        children=request.form['children']
        health=request.form['health']
        gender=request.form['gender']
        smoker=request.form['smoker']
        bmi=request.form['bmi']

        region_southeast=0
        region_northeast=0
        region_northwest=0
        region_southwest=0
        if region=='northeast':
            region_northeast=1
        elif region=='northwest':
            region_northwest=1
        elif region=='southeast':
            region_southeast=1
        else:
            region_southwest=1

        ls={"age":[age],"gender":[gender],"bmi":[bmi],"child":[children],"smoker":[smoker],"health_category":[health],"region_northeast":[region_northeast],"region_northwest":[region_northwest],"region_southeast":[region_southeast],"region_southwest":[region_southwest]}
        df=pandas.DataFrame(ls)
        x=model_1.predict(df)
        y=model_2.predict(df)
        z=model_3.predict(df)

        conn=sqlite3.connect('insurance.db')
        cur=conn.cursor()
        Data=(age,gender,bmi,children,region,smoker,health,x[0])
        cur.execute(data_insert_query,Data)
        conn.commit()
        cur.close()
        conn.close()


        a=str(x[0])
        b=str(y[0][0])
        c=str(z[0])

        list={"prediction":a,"perdicton":b,"perdiction":c}
        
        return render_template('final.html',output=x[0])
        
                       

if __name__=="__main__":
    app.run(debug=True)


    