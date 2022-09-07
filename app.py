from turtle import update
from unicodedata import name
from flask import Flask, render_template,jsonify,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///drinks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Drinks(db.Model):
    __tablename__ = "Drinksapp"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    description = db.Column(db.String(120),unique=True,nullable=False)
  
    def __repr__(self):
        return f"{self.name} - {self.description}"

#Simple documentation in Html
@app.route("/")
def index():
    return render_template("index.html")


#Get all Drinks
@app.route("/drinks",methods=["GET"])    
def get_drinks():
    drink = Drinks.query.all()
    #Rendering out the data
    #Only displays the first element in the list 
    # for drk in drink:
    #     dk = f"name: {drk.name} , description : {drk.description}"
    #     return jsonify(dk)

     # // Method 1
   # return f" 1,{drink[0]}     2,{drink[1]}"

     # //Method 2
    output = []
    for drk in drink:
       dk =  {
        'name' : drk.name , 
       'description' : drk.description 
       }
       output.append(dk) 
    return {"Drinks": output}  


#Get Drink by Id
@app.route("/drinks/<int:id>",methods=["GET"])
def get_drink_by_id(id):
    drink = Drinks.query.get_or_404(id)
    return { "id":drink.id, "name":drink.name , "description":drink.description}
    # Similar method //Not in object format
    # return f"name: {drink.name} , description: {drink.description}"


#Post a new Drink
@app.route("/drinks",methods=["POST"])
def post_drink():
    name =request.json["name"]
    description  =request.json["description"]
    drink = Drinks(name=name ,description=description)
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id ,'name': drink.name,'description': drink.description}   

    # //Posting data to the db manually
    # from app import Drinks
    # db.session.add(Drinks(name="milk",description="nutritious"))
    # db.session.commit() 


#Delete drink by Id
@app.route("/drinks/<int:id>",methods=["DELETE"])    
def delete_drink(id):
    dlt = Drinks.query.get(id)
    if dlt is None:
        return {"404 Error" : "Sorry the id has already been deleted"}
    db.session.delete(dlt)
    db.session.commit()
    return jsonify({"Message" : "Successfully Deleted a Record!!"
    })


#Update a Drink
@app.route("/drinks/<int:id>",methods=["PUT"])
def Update_drink(id):
    update = Drinks.query.get_or_404(id)
    name= request.json["name"]
    description =request.json["description"]
    update.name = name
    update.description = description       
    db.session.commit()
    return {"200 OK":"Successfully Updated a record"}


#Run Server + live reload
if __name__ == '__main__':
    app.run(debug=True)