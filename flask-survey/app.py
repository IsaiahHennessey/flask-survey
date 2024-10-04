from flask import Flask, session, redirect, render_template, request, flash
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.secret_key = "some_secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home():
    satisfaction_survey = surveys['satisfaction']
    return render_template('home.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/questions/<int:qid>', methods=['GET'])
def survey(qid):
    """Display the current question based on the number of responses."""
    responses = session.get('responses', [])  # Get responses from session
    survey = surveys['satisfaction']
    question_count = len(survey.questions)

    if len(responses) >= question_count:
        return redirect('/thankyou')

    if qid != len(responses):
        flash("You're trying to access an invalid question.")
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)


@app.route('/answer', methods=['POST'])
def answer():
    """Handle the answer submission and add it to the session."""
    answer = request.form.get('answer')
    responses = session.get('responses', [])  # Get responses from session

    responses.append(answer)  # Add answer to the list
    session['responses'] = responses  # Rebind the updated list to session

    # Check if all questions have been answered
    if len(responses) >= len(surveys['satisfaction'].questions):
        return redirect('/thankyou')

    return redirect(f'/questions/{len(responses)}')


@app.route('/start-survey', methods=['POST'])
def start_survey():
    """Clear the session of responses and start the survey."""
    session['responses'] = []  # Initialize an empty list for responses
    return redirect('/questions/0')


@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)