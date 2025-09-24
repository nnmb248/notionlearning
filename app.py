from flask import Flask, render_template, request, redirect, url_for, session
import json, random, os

app = Flask(__name__)
app.secret_key = "your-secret-key"

JSON_FILE = os.path.join(os.path.dirname(__file__), "concepts.json")

def load_concepts():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for subject, concepts in data.items():
        if not isinstance(concepts, dict):
            data[subject] = {}
    return data

data = load_concepts()

@app.route("/")
def index():
    return render_template("index.html", data=data)

@app.route("/quiz/<subject>")
def quiz(subject):
    concepts = data.get(subject, {})
    if not concepts:
        return render_template("result_none.html", subject=subject)

    selected = random.sample(list(concepts.items()), min(10, len(concepts)))
    session['quiz'] = selected
    session['answers'] = [None] * len(selected)

    index = 0
    total = len(selected)
    prevPercent = 0
    currentPercent = ((index + 1) / total) * 100

    return render_template("quiz.html",
                           subject=subject,
                           concept=selected[0][0],
                           index=index,
                           total=total,
                           prevPercent=prevPercent,
                           currentPercent=currentPercent,
                           answer=None)

@app.route("/answer", methods=["POST"])
def answer():
    index = int(request.form['index'])
    choice = request.form['choice']
    subject = request.form['subject']

    quiz = session.get('quiz', [])
    answers = session.get('answers', [])

    answers[index] = choice
    session['answers'] = answers

    if index + 1 >= len(quiz):
        return redirect(url_for('result'))
    else:
        next_index = index + 1
        total = len(quiz)
        prevPercent = ((index + 1) / total) * 100      # 현재 문제 위치
        currentPercent = ((next_index + 1) / total) * 100  # 이동할 문제 위치
        next_concept = quiz[next_index][0]
        next_answer = answers[next_index]

        return render_template("quiz.html",
                               subject=subject,
                               concept=next_concept,
                               index=next_index,
                               total=total,
                               prevPercent=prevPercent,
                               currentPercent=currentPercent,
                               answer=next_answer)

@app.route("/previous", methods=["POST"])
def previous():
    index = int(request.form['index'])
    subject = request.form['subject']

    quiz = session.get('quiz', [])
    answers = session.get('answers', [])

    if index <= 0:
        return redirect(url_for('quiz', subject=subject))

    prev_index = index
    current_index = index - 1
    total = len(quiz)

    prevPercent = ((prev_index + 1) / total) * 100      # 현재 문제 위치
    currentPercent = ((current_index + 1) / total) * 100  # 이동할 문제 위치

    prev_concept = quiz[current_index][0]
    prev_answer = answers[current_index]

    return render_template("quiz.html",
                           subject=subject,
                           concept=prev_concept,
                           index=current_index,
                           total=total,
                           prevPercent=prevPercent,
                           currentPercent=currentPercent,
                           answer=prev_answer)

@app.route("/result")
def result():
    quiz = session.get('quiz', [])
    answers = session.get('answers', [])
    result_list = []
    for (concept, explanation), user_choice in zip(quiz, answers):
        result_list.append({"concept": concept, "explanation": explanation, "selected": user_choice})
    return render_template("result.html", result=result_list)

if __name__ == "__main__":
    app.run(debug=True)
