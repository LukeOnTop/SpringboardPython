from flask import Flask, request, render_template
from stories import story
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'elliott'
debug = DebugToolbarExtension(app)


@app.route("/")
def ask_questions():
    """Generate and show form to ask words."""

    prompts = story.prompts
    return render_template("questions.html", prompts=prompts)


@app.route("/story")
def show_story():
    """Show story result."""

    text = story.generate(request.args)

    return render_template("story.html", text=text)

# @app.route('/form')
# def show_form():
#    return render_template('form.html')
#
#
# @app.route('/form2')
# def show_form2():
#    return render_template('form2.html')
#
#
#COMPLIMENTS = ["hip", "cool", "nice"]
#
#
# @app.route('/greet')
# def greeting():
#    user = request.args["username"]
#    nice_thing = choice(COMPLIMENTS)
#    return render_template("greet.html", username=user, comp=nice_thing)
#
#
# @app.route('/greet-2')
# def greet2():
#    user = request.args["username"]
#    flatter = request.args.get("wants_compliment")
#    nice = sample(COMPLIMENTS, 3)
#    return render_template('greet-2.html', username=user, flatter=flatter, nice=nice)
#
#
# @app.route('/lucky')
# def lucky_num():
#    num = randint(1, 6)
#    return render_template("temp1.html", lucky_num=num)
