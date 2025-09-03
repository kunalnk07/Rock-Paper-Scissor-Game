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
        <title>🎮 Rock Paper Scissors - Best of 3</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: radial-gradient(circle at top, #1f1f1f, #000);
                color: #fff;
                text-align: center;
                padding: 40px;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                color: #ffcc00;
                text-shadow: 2px 2px #000;
            }
            button {
                background: linear-gradient(145deg, #444, #222);
                border: none;
                color: #fff;
                padding: 15px 30px;
                margin: 10px;
                font-size: 20px;
                border-radius: 12px;
                box-shadow: 0 6px #000;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            button:hover {
                transform: scale(1.05);
                box-shadow: 0 8px #ffcc00;
            }
            #score {
                font-size: 22px;
                margin-top: 20px;
                color: #00ffcc;
            }
            #result {
                font-size: 20px;
                margin-top: 20px;
                min-height: 40px;
            }
            .emoji {
                font-size: 40px;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>🎮 Rock, Paper, Scissors</h1>
        <p>Best of 3 — First to 2 wins!</p>
        <div>
            <button onclick="play('rock')">🪨 Rock</button>
            <button onclick="play('paper')">📄 Paper</button>
            <button onclick="play('scissors')">✂️ Scissors</button>
        </div>
        <div id="score">You: 0 | Computer: 0</div>
        <div id="result"></div>
        <div class="emoji" id="emoji"></div>

        <script>
            let userScore = 0;
            let computerScore = 0;

            function play(choice) {
                fetch('/play?user=' + choice)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('result').innerHTML = data.message;
                    document.getElementById('emoji').innerHTML = data.emoji;
                    userScore = data.user_score;
                    computerScore = data.computer_score;
                    document.getElementById('score').innerHTML = `You: ${userScore} | Computer: ${computerScore}`;
                    if (data.game_over) {
                        setTimeout(() => {
                            alert(data.final_message);
                            userScore = 0;
                            computerScore = 0;
                            document.getElementById('score').innerHTML = `You: 0 | Computer: 0`;
                            document.getElementById('result').innerHTML = "";
                            document.getElementById('emoji').innerHTML = "";
                        }, 500);
                    }
                });
            }
        </script>
    </body>
    </html>
    """

# Score tracking
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

    emoji = ""
    if winner == "user":
        user_score += 1
        message = f"✅ You win this round! Computer chose {computer}."
        emoji = "😎🔥"
    elif winner == "computer":
        computer_score += 1
        message = f"❌ Computer wins this round! It chose {computer}."
        emoji = "🤖💥"
    else:
        message = f"🤝 It's a tie! You both chose {computer}."
        emoji = "😐⚖️"

    game_over = False
    final_message = ""
    if user_score == 2 or computer_score == 2:
        game_over = True
        if user_score > computer_score:
            final_message = "🎉 You crushed it! Victory dance time 🕺💃"
        else:
            final_message = "😢 Computer wins. But hey, even legends lose sometimes!"
        user_score = 0
        computer_score = 0

    return jsonify({
        "message": message,
        "emoji": emoji,
        "user_score": user_score,
        "computer_score": computer_score,
        "game_over": game_over,
        "final_message": final_message
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
