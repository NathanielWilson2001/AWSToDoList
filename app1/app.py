
from flask import Flask, flash, redirect, request, session, render_template, Markup
import hashlib, json, requests
from flask_session import Session 

 
app = Flask(__name__, template_folder='pages', static_folder='styles')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route('/', methods=["POST", "GET"])
def index():
    
    try:
        if session["user"]:
            
            # Grab User's current list of tasks  using Lambda Function LambdaUserTasks
            payload = {"Email" :  session["user"]}
            answer =  requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/gettasks", json=payload)
            answer = json.loads(answer.text)['body-json']
            
            counter = 0
            for task in answer:

                taskTile = Markup(
                    # To do list item task tile
                    "<h3>" + task['taskName'] + "<button type='button' class='btn-close' data-bs-toggle='modal' data-bs-target='#deleteModal" + str(counter) +"'></button></h3><hr><h5>Description:</h5><p>" + task['description'] + "</p>" + "<h5>Date:</h5><p>" + task['finishDate'] + "</p><hr><button type='button' class='btn btn' data-bs-toggle='modal' data-bs-target='#updateModal" + str(counter) +"'><h5>Update&#43;</h5></button></h1></a>" +
                    # Modal for updating the Item
                    "<div class='modal fade' id='updateModal" + str(counter) +"'><div class='modal-dialog modal-lg'><div class='modal-content'><div class='modal-header'>" + 
                    "<button type='button' class='btn-close' data-bs-dismiss='modal'></button></div><div class='modal-body'><form id='updateItem" +  str(counter) +  "' class='addItem' action='/?type=Update&number=" +  str(counter) +  "'method='POST'><div class='form-outline'>" +
                    "<input type='name' class='form-control disabledName' value='" + task['taskName'] + 
                    "'name='updateName" +  str(counter) +  "' id='updateName" +  str(counter) + "' readonly></input><textarea form='updateItem"+  str(counter) +  "' class='form-control' name='updateDescription" +  str(counter) +  "' id='updateDescription" +  str(counter) +  "' rows='4' placeholder = '" + task['description'] + "'value='" + task['description'] + 
                    "'>"+task['description']+"</textarea>" +"<input type = 'date' name = 'updateDate" +  str(counter) +  "' value='" + task['finishDate'] +
                    "'></div></form></div><div class='modal-footer'><div class='buttonContainer'><input type='submit' class='btn btn-primary update' value='Update&#43;' form='updateItem" +  str(counter) +  "'></div></div></div></div></div>"+
                    # Delete Item Modal
                    "<div class='modal fade' id='deleteModal" + str(counter) +"'><div class='modal-dialog'><div class='modal-content'><div class='modal-header'>" + 
                    "<button type='button' class='btn-close' data-bs-dismiss='modal'></button></div><div class='modal-body'><form id='deleteItem" +  str(counter) +  "' class='deleteItem' action='/?type=Delete&number=" +  str(counter) + "'method='POST'><div class='form-outline'>" +
                    "<h3>Would you like to delete:</h3><input type='name' class='form-control disabledName' value='" + task['taskName'] + 
                    "'name='deleteName" +  str(counter) +  "' id='deleteName" +  str(counter) + "' readonly></form></div><div class='modal-footer'><div class='buttonContainer'><input type='submit' class='btn btn-primary delete'  value='Delete' form='deleteItem" +  str(counter) +  "'></div></div></div></div></div></div>"
                    
                    
                    
                    )
                counter += 1
                flash(taskTile)
         
            if request.method == "POST":
                 
                if  request.args.get("type") == "Add":
                    email  = session["user"]
                    name = request.form.get('name')
                    description = request.form.get('description')
                    date = request.form.get("date")
                    payload = {"Email" : email, "Name" : name, "Description": description, "Date": date }
                    answer =  requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/add", json=payload)
            
                    if(json.loads(answer.text)['Success'] == "ALREADY EXISTS"):
                        session.pop('_flashes', None)
                        flash("ALREADY EXISTS")
                        return redirect("/")
                    else:    
                        session.pop('_flashes', None)
                        return redirect("/")
                    
                if request.args.get("type") == "Update":
                    email  = session["user"]
                    name = request.form.get('updateName' + request.args.get("number"))
                    description = request.form.get('updateDescription' + request.args.get("number"))
                    date = request.form.get("updateDate" + request.args.get("number"))
                    
                    # Send form data to the API gateway which connects to the Lambda function
                    payload = {"Email" : email, "Name" : name, "Description": description, "Date": date }
                    answer =  requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/update", json=payload)
                    session.pop('_flashes', None)
                    return redirect("/")
                
                if request.args.get("type") == "Delete":
                    email  = session["user"]
                    name = request.form.get('deleteName' + request.args.get("number"))

                    # Send form data to the API gateway which connects to the Lambda function
                    payload = {"Email" : email, "Name" : name}
                    answer = requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/delete", json=payload)
                    session.pop('_flashes', None)
                    return redirect("/")
                   
                     
        else:
            return redirect("/login")
    except:
        return redirect("/login")
    return render_template("index.html")


@app.route('/delete', methods=["POST"])
def delete():
    if request.method == "POST":
        taskName = request.args.get("task")
        email  = session["user"]
        payload = {"Email" : email, "Name" : taskName}
        answer = requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/delete", json=payload)
        session.pop('_flashes', None)
        flash(answer)
   
    return redirect("/")
        
    
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        password = password.encode()
        password = hashlib.md5(password).hexdigest()
        
        # Pass data to Lambda Function via the API Gateway 
        payload = {"Email" : user, "Password" : password}
        answer =  requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/login",  json=payload)
        print(answer.text)
    
        if(json.loads(answer.text)['body-json']['Success'] == "true"):
          
           session['user'] = user 
           session['name'] = json.loads(answer.text)['body-json']['Name']
           return redirect("/")
        else:
            flash("Failure")    
    return render_template("login.html")

@app.route("/register",methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        password = password.encode()
        password = hashlib.md5(password).hexdigest()
        
        # Pass data to Lambda Function 
        payload = {"Email" : email, "Password" : password, "Name" : name}
     
    
        answer =  requests.post("https://jszojsq1lb.execute-api.us-east-1.amazonaws.com/Login/reg", json=payload)
       

        if(json.loads(answer.text)['Success'] == "true"):
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