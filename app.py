from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    jsonify,
    json,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:mysecretpassword@20.0.161.2:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mykey"

db = SQLAlchemy(app)

# Models

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("users", lazy="dynamic"))

    def __init__(self, username, email, password, role_id):
        self.name = username
        self.email = email
        self.password = password
        self.role_id = role_id


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    issue_description = db.Column(db.String(50))
    status = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('issues', lazy='dynamic'))
    

    def __init__(self, name, phone, issue_description, status,user_id):
        self.name = name
        self.phone = phone
        self.issue_description = issue_description
        self.status = status
        self.user_id = user_id


def check_role(user, role_name):
    return user.role.name == role_name


# Routes and Views


@app.route("/")
def index():
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)
        if user and check_role(user, "Admin"):
            return render_template("admin.html", username=user.username)
        
    return render_template("login.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["user_id"] = user.id
            flash("Login successful.")
            return redirect("/")
        else:
            error_message = "Invalid username or password."
            return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")
    
@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    current_user_id = session.get("user_id")
    
    if current_user_id:
        current_user = db.session.query(User).get(current_user_id)
        
        if current_user and check_role(current_user, "Admin"):
            try:
                user = db.session.query(User).get(user_id)
                if user is None:
                    return jsonify({"error": "User to delete not found"}), 404
                
                issues = db.session.query(Issue).filter_by(user_id=user_id).all()
                for issue in issues:
                    db.session.delete(issue)
                
                db.session.delete(user)
                db.session.commit()
                
                return jsonify({"message": "User and associated issues deleted successfully"})
                
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
            
        return "You don't have permission to delete the user"
    
    return render_template("login.html")

        


        
    





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8001)
