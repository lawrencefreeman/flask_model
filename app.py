from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
from flask_marshmallow import Marshmallow


app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'kubrick.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+db_path
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def home():
    return jsonify(data='Welcome Home')


# http://127.0.0.1:5000/get_consultant?email=joebloggs@gmail.com
@app.route('/get_consultant')
def get_consultant():
    con = request.args.get('email', 'unknown')
    by_stream = request.args.get('stream', 'unknown')
    # retrieve consultant info from database by name
    if by_stream != 'unknown':
        con_details = Consultant.query.filter_by(stream=by_stream).all()
        result = consultant_schemas.dump(con_details)
    else:
        con_details = Consultant.query.filter_by(email=con).first()
        result = consultant_schema.dump(con_details)
    return jsonify(result)


class Consultant(db.Model):
    __tablename__ = 'consultant'
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    stream = Column(String)
    email = Column(String, unique=True)

class ConsultantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fname', 'lname', 'stream', 'email')

consultant_schema = ConsultantSchema()
consultant_schemas = ConsultantSchema(many=True)

# python scripts have the value '__main__' when being executed (not imported)
if __name__ == '__main__':
    app.run(host='0.0.0.0')