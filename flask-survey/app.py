# still need to make this a repository

from flask import Flask, request, render_template, redirect
from surveys import Survey, Question, satisfaction_survey, personality_quiz
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

survey = satisfaction_survey
total_qs = len(survey.questions)
responses = []


@app.route("/")
def home():

    return render_template('start.html', survey=survey)


@app.route("/start", methods=["POST"])
def start():
    return redirect("/question/0")


@app.route("/answer", methods=["POST"])
def answers():
    user_reply = request.form["answer"]
    responses.append(user_reply)
    count = len(responses)
    return redirect(f"/question/{count}")


@app.route("/question/<int:quest>")
def questions(quest):
    count = len(responses)

    if count >= total_qs:
        return redirect('/endsurvey')

    elif count != quest:
        return render_template(f"question.html", survey=survey, num=count)

    else:
        return render_template(f"question.html", survey=survey, num=quest)


@app.route("/endsurvey")
def end_survey():
    all_resp = responses
    return render_template("endsurvey.html", all_resp=all_resp)


@app.route('/clear')
def clear_data():
    return redirect('/')
