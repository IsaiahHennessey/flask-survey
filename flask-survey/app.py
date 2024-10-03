from flask import Flask, session, redirect, render_template, request
from surveys import surveys


app = Flask(__name__)
app.secret_key = "some_secret_key"


@app.route('/')
def home():
    return redirect('/survey/0')

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/survey/<int:qid>', methods=['GET', 'POST'])
def survey(qid):
    survey = surveys['satisfaction']
    question = survey.questions[qid]

    if request.method == 'POST':
        answer = request.form.get('answer')
        responses = session.get('responses', [])
        responses.append(answer)
        session['responses'] = responses

        if qid + 1 >= len(survey.questions):
            return redirect('/thankyou')
        
        return redirect(f'/survey/{qid + 1}')

    return render_template('question.html', question=question)
