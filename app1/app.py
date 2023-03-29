
from flask import Flask, flash, redirect, request, session, render_template, Markup
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

@app.route('/', methods=["POST", "GET"])
def index():
    try:
        if session["user"]:
            
            # Grab User's account information
            payload = {"Email" :  session["user"]}
            response = lambdaConnection.invoke(FunctionName= "LambdaUsersTasks", InvocationType='RequestResponse', Payload=json.dumps(payload))
            answer = response["Payload"].read()
            answer = json.loads(answer)
            
            # Grab User's current list of tasks  using Lambda Function LambdaUserTasks
            payload = {"Email" :  session["user"]}
            response = lambdaConnection.invoke(FunctionName= "LambdaUsersTasks", InvocationType='RequestResponse', Payload=json.dumps(payload))
            answer = response["Payload"].read()
            answer = json.loads(answer)
            
            for task in answer:
                taskTile = Markup("<h3>" + task['taskName'] + "<button type='button' class='btn-close'></button></h3><hr><h5>Description:</h5><p>" + task['description'] + "</p>" + "<h5>Date:</h5><p>" + task['date'] + "</p>")
                flash(taskTile)
                            
            if request.method == "POST":
                email  = session["user"]
                name = request.form.get('name')
                description = request.form.get('description')
                date = request.form.get("date")
                
                # Send form data to the Add Task Lambda function
                payload = {"Email" : email, "Name" : name, "Description": description, "Date": date }
                response = lambdaConnection.invoke(FunctionName= "AddTasks", InvocationType='RequestResponse', Payload=json.dumps(payload))
                answer = response["Payload"].read()
                answer = json.loads(answer)
        
                if(answer == "ALREADY EXISTS"):
                    flash(answer)
                    return render_template("index.html")
                else:    
                    session.pop('_flashes', None)
                    return redirect("/")
        else:
            return redirect("/login")  
    except:
        return redirect("/login")
    return render_template("index.html")

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
        
        if(answer != "FAILURE" and answer != "Invalid Email or Password"):
           session['user'] = user 
           session['name'] = answer
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
    Session(app)
    return redirect("/")

if __name__=='__main__':
    app.run(debug = True)