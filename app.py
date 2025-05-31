from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
db = SQLAlchemy(app)

# Add datetime filter to Jinja2
@app.template_filter()
def format_datetime(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(20), nullable=False)
    results = db.relationship('Result', backref='student', lazy=True)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    student_name = request.form.get('student_name')
    class_level = request.form.get('class_level')
    
    student = Student.query.filter_by(name=student_name, class_level=class_level).first()
    if student:
        results = Result.query.filter_by(student_id=student.id).all()
        return render_template('result.html', 
            student=student, 
            results=results,
            current_time=datetime.now())
    else:
        flash('Student not found!', 'error')
        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/add', methods=['POST'])
def add_marks():
    student_name = request.form.get('student_name')
    class_level = request.form.get('class_level')
    
    student = Student.query.filter_by(name=student_name, class_level=class_level).first()
    if not student:
        student = Student(name=student_name, class_level=class_level)
        db.session.add(student)
        db.session.commit()
    
    subjects = ['Nepali', 'Social', 'Maths', 'Science', 'Wonder', 'Computer', 'Health', 'Reader', 'Serophero', 'GK']
    for subject in subjects:
        marks = request.form.get(subject)
        if marks and marks.isdigit():
            result = Result(student_id=student.id, subject=subject, marks=int(marks))
            db.session.add(result)
    
    db.session.commit()
    flash('Marks added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/reset', methods=['POST'])
def reset_marks():
    student_name = request.form.get('student_name')
    class_level = request.form.get('class_level')
    
    student = Student.query.filter_by(name=student_name, class_level=class_level).first()
    if student:
        # Delete all results for this student
        Result.query.filter_by(student_id=student.id).delete()
        db.session.commit()
        flash('Marks reset successfully!', 'success')
    else:
        flash('Student not found!', 'error')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
