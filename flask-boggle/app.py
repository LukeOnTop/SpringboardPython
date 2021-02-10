from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board

    return render_template("index.html", board=board)



@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})


@app.route("/score", methods=["POST"])
def score():
    """Logs away current score and updates highscore if score > highscore"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    session["highscore"] = max(score, highscore)

    return jsonify({"highscore": session["highscore"]}) 

@app.route("/plays", methods=["POST"])
def countplays():

    num_games = session.get("num_games", 0)
    session["num_games"] = num_games+1
    return jsonify({"game_count": session["num_games"]})
