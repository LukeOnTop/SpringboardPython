# still need to make this a repository

from flask import Flask, request, render_template, redirect
from flask import session, make_response, flash
from surveys import Survey, Question, satisfaction_survey, personality_quiz
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

survey = satisfaction_survey
total_qs = len(survey.questions)


@app.route("/")
def home():
    session['responses_key'] = "dont_skip"
    session['q_count'] = 0
    return render_template('start.html', survey=survey)


@app.route("/start", methods=["POST"])
def start():
    session['responses_key'] = []

    return redirect("/question/0")


@ app.route("/answer", methods=["POST"])
def answers():
    user_reply = request.form['answer']
    store_session = session['responses_key']
    session['responses_key'] = user_reply
    store_session.append(user_reply)
    session['responses_key'] = store_session
    count = len(store_session)
    session['q_count'] = count

    if count >= total_qs:
        return redirect("/endsurvey")
    else:
        return redirect(f"/question/{count}")


@ app.route("/question/<int:quest>")
def questions(quest):
    num = session['q_count']

    if (session['responses_key'] == "dont_skip"):
        flash('Dont Skip Ahead!!!')
        return redirect('/')

    elif session['q_count'] != quest:
        flash("Please Answer Questions In Order")
        return render_template(f"question.html", survey=survey, num=num)

    return render_template(f"question.html", survey=survey, num=quest)


@ app.route("/endsurvey")
def end_survey():
    all_resp = session['responses_key']

    return render_template("endsurvey.html", all_resp=all_resp)


@ app.route('/clear')
def clear_data():
    session['responses_key'] = []
    return redirect('/')
