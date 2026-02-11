from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

SECRET_WORD = "Curry"
GUESS_LIMIT = 3

@app.route("/", methods=["GET", "POST"])
def index():
    if "guess_count" not in session:
        session["guess_count"] = 0
        session["game_over"] = False
        session["message"] = ""

    if request.method == "POST":
        if not session["game_over"]:
            guess = request.form.get("guess")

            if session["guess_count"] < GUESS_LIMIT:
                session["guess_count"] += 1

                if guess == SECRET_WORD:
                    session["message"] = "🎉 You Win!"
                    session["game_over"] = True
                elif session["guess_count"] >= GUESS_LIMIT:
                    session["message"] = "❌ Out of guesses, You Lose!"
                    session["game_over"] = True
                else:
                    session["message"] = "Wrong guess! Try again."
    
    return render_template(
        "index.html",
        message=session.get("message"),
        guess_count=session.get("guess_count"),
        guess_limit=GUESS_LIMIT,
        game_over=session.get("game_over")
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
