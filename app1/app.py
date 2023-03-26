
from flask import Flask, flash, redirect, request, session, render_template
import hashlib, boto3, json
from boto3.dynamodb.conditions import Key, Attr
from flask_session import Session 

accessKey = ""
secretKey = ""
sessToken = ""
sessionBoto = boto3.session.Session(
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey,
    aws_session_token=sessToken,
)

dynamodb = boto3.resource('dynamodb', aws_access_key_id= accessKey, aws_secret_access_key=secretKey, aws_session_token=sessToken)
lambdaConnection = boto3.client('lambda',  region_name= "us-east-1", aws_access_key_id=accessKey,aws_secret_access_key=secretKey, aws_session_token=sessToken)
    
app = Flask(__name__, template_folder='pages', static_folder='styles')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route('/')
def index():
    
    try:
        if session["user"]:
            
            # Grab User's current list of tasks 
            table = dynamodb.Table('tasks')
             
            payload = {"Email" :  session["user"]}
            response = lambdaConnection.invoke(FunctionName= "LambdaUsersTasks", InvocationType='RequestResponse', Payload=json.dumps(payload))
            answer = response["Payload"].read()
            answer = json.loads(answer)
            
            flash(answer)
            
            return render_template("index.html")
        else:
            return redirect("/login")
    except:
        return redirect("/login")    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        password = password.encode()
        password = hashlib.md5(password).hexdigest()
        
        # Pass data to Lambda Function 
        payload = {"Email" : user, "Password" : password}
        response = lambdaConnection.invoke(FunctionName= "lamLoginTest", InvocationType='RequestResponse', Payload=json.dumps(payload))
        answer = response["Payload"].read()
        answer = json.loads(answer)
        
        if(answer == "SUCCESS"):
           session['user'] = user 
           return redirect("/")
        else:
            flash("Failure")    
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        password = password.encode()
        password = hashlib.md5(password).hexdigest()
        
        # Pass data to Lambda Function 
        payload = {"Email" : email, "Password" : password, "Name" : name}
        response = lambdaConnection.invoke(FunctionName= "LambdaRegistration", InvocationType='RequestResponse', Payload=json.dumps(payload))
        answer = response["Payload"].read()
        answer = json.loads(answer)
        
        if(answer == "SUCCESS"):
            flash("Success")
            return redirect("/login")
        else:
            flash("Failure")     
                      
    return render_template("register.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect("/")

if __name__=='__main__':
    app.run(debug = True)