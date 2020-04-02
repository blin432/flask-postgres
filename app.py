from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from config import Config

app = Flask(__name__)

ENV = 'dev'

#initialize db
if ENV =='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']=Config['SQLALCHEMY_DATABASE_URI']

else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']=''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#creating database object
db = SQLAlchemy(app)

#creating models (like sequalize)
class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column (db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.String(200))
    comments = db.Column(db.Text())

    #kind of constructor

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POSt'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer,dealer,rating,comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter field')
        #checking if customer exists
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer,dealer,rating,comments)
            return render_template('success.html')
        return render_template('index.html', message='customer already exists')

   
if __name__ == '__main__':
    app.run()