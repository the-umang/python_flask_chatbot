from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os

# Init app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World!!', 'pop': {'lol': 'popop'}})


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Welcome Class/Model
class Welcome(db.Model):
    __tablename__ = 'welcometable'
    id = db.Column(db.Integer, primary_key=True)
    requestid = db.Column(db.String(200))
    chatid = db.Column(db.String(200),unique=True)
    requestclass = db.relationship('RequestClass', backref='parent')
    __table_args__ = (db.UniqueConstraint('chatid'),)

    def __init__(self, requestid,chatid, intent, message):
        self.requestid = requestid
        self.chatid = chatid
        RequestClass.__init__(self, intent, message)


class RequestClass(db.Model):
    __tablename__ = 'requestclasstable'
    id = db.Column(db.Integer, primary_key=True)
    intent = db.Column(db.String(200))
    message = db.Column(db.String(200))
    welcomeId = db.Column(db.Integer, db.ForeignKey('welcometable.id'))

    def __init__(self, intent, message):
        self.intent = intent
        self.message = message


# Welcome Schema
class WelcomeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'requestid','chatid', 'intent', 'message')


# Init schema
welcome_schema = WelcomeSchema()


# Chat ID Schema
class ChatIDSchema(ma.Schema):
    class Meta:
        fields = ('id','chatid')


# Init schema
chat_ID_schema = ChatIDSchema(many=True)
welcome_all_schema = WelcomeSchema(many=True)


# Create a welcome
@app.route('/welcome', methods=['POST'])
def add_welcome():

    requestobj = request.json['requestobj']

    # check if the chat id is present or not
    all_chat_ID = Welcome.query.all()
    result = chat_ID_schema.dump(all_chat_ID)
    chatIDExistOrNot = False
    for x in result:
        chatIDExistOrNot = chatIDExistOrNot  or x['chatid']==request.json['chatid']
    
    if chatIDExistOrNot==False:
        new_welcome = Welcome(
        request.json['requestid'],request.json['chatid'], 'ORDER', requestobj["message"])
    else:    
        new_welcome = Welcome(
        request.json['requestid'],request.json['chatid'], requestobj["intent"], requestobj["message"])

    db.session.add(new_welcome)
    db.session.commit()

    message_respone = {'message':'welcome'}

    return welcome_schema.jsonify(new_welcome)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
