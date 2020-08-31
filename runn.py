from flask import Flask, render_template, redirect, url_for, request, session

from flask_sqlalchemy import SQLAlchemy
import csv
app = Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Integer,nullable = False)
    category = db.Column(db.String(30), nullable = False)
    subcategory=db.Column(db.String(30), nullable = False)
    barcode=db.Column(db.String(30))
    def __repr__(self):
        return f"Product('{self.title}', '{self.price}')"
class Enquiry(db.Model):
    sn = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(40), nullable = False)
    company = db.Column(db.String(40), nullable = False)
    city = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(40), nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(40), nullable = False)
    subcategory = db.Column(db.String(40), nullable = False)
    #remarks = db.Column(db.Text, nullable = False)
    def __repr__(self):
        return f"Enquiry('{self.name}', '{self.company}')"
@app.route("/")
def home():
    return render_template('home.html')
@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        subcategory = request.form["subcategory"]
        price = request.form["price"]
        barcode = request.form["barcode"]
        cat = {"BARCODE":"1", "PRINTER":"2"}
        sub = {"SHEET":"1", "BARCODE PRINTER":"2", "SCANNER":"3", "INKJET":"1", "NORMAL":"2", "TYPE 3":"3"}
        def count(para):
            if para in session:
                session[para] = session[para] +1
            else:
                session[para] = 1
            return session[para]

        c = count(subcategory)
        barcode = cat[category] + sub[subcategory] + '0' + str(c)


        row = [str(title), str(category), str(subcategory), str(price), str(barcode)]
        with open('data.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row)
        product=Products(category=category, subcategory=subcategory, title=title, price=price, barcode=barcode)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template('add_product.html')
@app.route("/view_product", methods=["POST", "GET"])
def view_product():
    if request.method == "POST":
        c = request.form["category"]
        s=request.form["subcategory"]
        bc = str(request.form["barcode"])
        if(bc):
            return render_template('show.html', values = Products.query.filter_by(barcode = bc).all())
        elif(c == 'SHOW_ALL'):
            return render_template('show.html', values = Products.query.all())
        else:
            return render_template('show.html', values = Products.query.filter_by(category = c, subcategory = s).all())
    else:
        return render_template('view_product.html')
@app.route("/add_enquiry", methods=["POST", "GET"])
def add_enquiry():
    if request.method == "POST":
        name = request.form["name"]
        company = request.form["company"]
        city = request.form["city"]
        email = request.form["email"]
        phone = request.form["phone"]
        category = request.form["category"]
        subcategory = request.form["subcategory"]
        #remarks = request.form["remarks"]
        enquiry = Enquiry(name=name, company=company, city=city, email=email, phone=phone, category=category, subcategory=subcategory)
        db.session.add(enquiry)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add_enquiry.html')
@app.route("/view_enquiry", methods = ["POST", "GET"])
def view_enquiry():
    return render_template('show2.html', values = Enquiry.query.all())

if __name__ =='__main__':
    app.run(debug=True)
