from flask import Flask, request, jsonify

import random

app = Flask(__name__)

# Game logic
def get_winner(user, computer):
    if user == computer:
        return "tie"
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        return "user"
    else:
        return "computer"

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rock Paper Scissors - Best of 3</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f4f4f4; }
            button { padding: 10px 20px; margin: 10px; font-size: 18px; }
            #result { font-size: 20px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>🎮 Rock, Paper, Scissors - Best of 3</h1>
        <p>First to 2 wins!</p>
        <div>
            <button onclick="play('rock')">🪨 Rock</button>
            <button onclick="play('paper')">📄 Paper</button>
            <button onclick="play('scissors')">✂️ Scissors</button>
        </div>
        <div id="score">You: 0 | Computer: 0</div>
        <div id="result"></div>

        <script>
            let userScore = 0;
            let computerScore = 0;

            function play(choice) {
                fetch('/play?user=' + choice)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('result').innerHTML = data.message;
                    userScore = data.user_score;
                    computerScore = data.computer_score;
                    document.getElementById('score').innerHTML = `You: ${userScore} | Computer: ${computerScore}`;
                    if (data.game_over) {
                        alert(data.final_message);
                        userScore = 0;
                        computerScore = 0;
                        document.getElementById('score').innerHTML = `You: 0 | Computer: 0`;
                        document.getElementById('result').innerHTML = "";
                    }
                });
            }
        </script>
    </body>
    </html>
    """

# Keep scores in memory
user_score = 0
computer_score = 0

@app.route("/play")
def play():
    global user_score, computer_score
    user = request.args.get("user")
    choices = ["rock", "paper", "scissors"]

    if user not in choices:
        return jsonify({"error": "Invalid choice"})

    computer = random.choice(choices)
    winner = get_winner(user, computer)

    if winner == "user":
        user_score += 1
        message = f"✅ You win this round! Computer chose {computer}."
    elif winner == "computer":
        computer_score += 1
        message = f"❌ Computer wins this round! Computer chose {computer}."
    else:
        message = f"🤝 It's a tie! Computer also chose {computer}."

    game_over = False
    final_message = ""
    if user_score == 2 or computer_score == 2:
        game_over = True
        if user_score > computer_score:
            final_message = "🎉 Congratulations! You won the best of 3 series!"
        else:
            final_message = "😢 Computer wins the best of 3 series. Better luck next time!"
        user_score = 0
        computer_score = 0

    return jsonify({
        "message": message,
        "user_score": user_score,
        "computer_score": computer_score,
        "game_over": game_over,
        "final_message": final_message
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
