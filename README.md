To start the server ->
"python3 app.py"

To create a new db
Delete the db.sqlite file and 
On bash

->python3
>>> from app import db
>>> db.create_all()
>>> db.session.commit()



Server will be starting on port 5000
http://127.0.0.1:5000/

Post request -> http://127.0.0.1:5000/welcome

body ->
{
    "requestid":"1234",
    "chatid" : "2378",
    "requestobj": {
        "intent": "WELCOME", 
		"message": "hi"
    }
}