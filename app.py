from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Quiz, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_quiz = Quiz(title=title, description=description)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_quiz.html')

@app.route('/take_quiz/<int:quiz_id>')
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = 0
    for question in quiz.questions:
        user_answer = int(request.form.get(f'q{question.id}', -1))
        if user_answer == question.correct_answer:
            score += 1
    return render_template('results.html', score=score, total=len(quiz.questions))

if __name__ == '__main__':
    app.run(debug=True)
