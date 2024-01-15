from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Building chatterbox api endpoints..."

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    # Handling 'GET' requests; order by created date
    if request.method == "GET":
        messages = []
        for message in Message.query.order_by(Message.created_at.asc()).all():
            message_dict = message.to_dict()
            messages.append(message_dict)
        
        response = make_response(
            jsonify(messages),
            200
        )
        return response
    
    # Handling 'POST' requests
    elif request.method == "POST":
        # How to get data posted using raw json body section in postman
        new_post = Message(
            body = request.get_json().get("body"),
            username = request.get_json().get("username")
        )
        db.session.add(new_post)
        db.session.commit()

        new_post_dict = new_post.to_dict()

        response = make_response(
            jsonify(new_post_dict),
            201
        )
        return response

@app.route('/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    # Retrieve the message
    message = Message.query.filter_by(id=id).first()
    # Handling "GET" requests
    if request.method == "GET":
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        return response
    # Handling 'PATCH' requests; editing the message
    elif request.method == "PATCH":
        for attr in request.form:
            setattr(message, attr, request.form.get(attr))

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        return response
    
    # Handling 'DELETE' requests
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted"
        }
        response = make_response(
            jsonify(response_body),
            200
        )
        return response


if __name__ == '__main__':
    app.run(port=5555)
