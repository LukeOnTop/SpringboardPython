class BoggleGame {
    constructor(boardId) {
        ;
        this.board = $("#" + boardId);
        this.score = 0;
        this.highscore = 0;
        this.numgames = 0;
        this.goodGuesses = new Set();

        this.timer();

        this.form = document.getElementById("form");

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this))
        $(".replay", this.board).on("click", this.handleReplay.bind(this))
    }

    timer() {
        let sec = 60;
        const timer = setInterval(function () {
            document.getElementById('timer').innerHTML = '00:' + sec;
            sec--;
            if (sec < 0) {
                $(".answer").text("Game Over")
                clearInterval(timer);
                $(".replay", this.board).show()
                $(".add-word", this.board).hide()
            }
        }, 1000);
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        $(".replay", this.board).hide();
        const word = $('.word').val();
        const wordLen = word.length;
        const res = await axios.get("/check-word", { params: { word: word } });

        if (this.goodGuesses.has(word)) {
            return
        }

        if (res.data.result === "ok") {
            $('.guesses').append(`<li>${word}</li>`)
            this.goodGuesses.add(word)
            this.score += wordLen
            $(".answer").text(`"${word}" counts for ${wordLen} points!`)
        }
        else {
            $(".answer").text(`"${word}" is ${res.data.result} dummy!`)
        }

        $(".score", this.board).text(`Score : ` + this.score);
        console.log(res)
        this.form.reset();
    }

    async checkScore() {
        const scoreRes = await axios.post("/score", { score: this.score })
        this.highscore = scoreRes.data.highscore
        $(".highscore", this.board).text(`Highscore : ` + scoreRes.data.highscore);
        console.log(scoreRes)
    }

    async handleReplay(e) {
        e.preventDefault();
        const res = await axios.post("/plays", { numgames: this.numgames })
        location.reload();
    }
}
