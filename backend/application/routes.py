from flask import current_app as app
from flask import request,render_template
from flask_security import verify_password,auth_required
@app.route('/')
def home():
    return render_template("index.html")
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        return "login first"
    if request.method=="POST":
        email=request.json.get("email")
        pws=request.json.get("password")
        datastore = app.security.datastore
        user= datastore.find_user(email = email)
        if user :
            if verify_password(pws,user.password):
                return {"token" : user.get_auth_token(),"messeage" : "login successful"}
            else:
                return {"messeage" : "invalid password"}
        else:
            return {"messeage" : "user not found"}

@app.route("/dashboard/admin")       
@auth_required("token")
def admin_route():
    return {"message" : "welcome to dashboard"}