from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# TODO: add CORS   -->    'TODO' is a programers way of writing notes & reminders

# create flask appliaction
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Students.db'
db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stuname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Students %r>' % self.stuname

@app.route('/', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        res=[]
        for stu in Students.query.all():
            res.append({"stuname":stu.stuname, "email":stu.email,"id":stu.id})
        return jsonify(res)
    elif request.method == 'POST': #add row
        student_data = request.get_json()
        student = Students(stuname=student_data['stuname'], email=student_data['email'])
        db.session.add(student)
        db.session.commit()
        return jsonify({'id': student.id})

@app.route('/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def student(student_id):
    student = Students.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    if request.method == 'GET':
        return   {"stuname":student.stuname, "email":student.email,"id":student_id}
        # return jsonify(res)
        # return json.dumps(user.__dict__)
    elif request.method == 'PUT':
        student_data = request.get_json()
        student.stuname = student_data['stuname']
        student.email = student_data['email']
        db.session.commit()
        return jsonify({'id': student.id})
    elif request.method == 'DELETE':
        db.session.delete(student)
        db.session.commit()
        return jsonify({'result': 'Student deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
