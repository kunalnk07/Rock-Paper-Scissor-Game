import random

def get_winner(user, computer):
    if user == computer:
        return "tie"
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        return "user"
    else:
        return "computer"

def play_best_of_three():
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0

    print("ðŸŽ® Welcome to Rock, Paper, Scissors - Best of 3!")

    while user_score < 2 and computer_score < 2:
        user = input("Enter your choice (rock, paper, scissors): ").lower()

        if user not in choices:
            print("Invalid choice! Try again.")
            continue

        computer = random.choice(choices)
        print(f"Computer chose: {computer}")

        winner = get_winner(user, computer)

        if winner == "tie":
            print("It's a tie this round!")
        elif winner == "user":
            user_score += 1
            print("âœ… You win this round!")
        else:
            computer_score += 1
            print("âŒ Computer wins this round!")

        print(f"Score â†’ You: {user_score} | Computer: {computer_score}\n")

    if user_score > computer_score:
        print("ðŸŽ‰ Congratulations! You won the best of 3 series!")
    else:
        print("ðŸ˜¢ Computer wins the best of 3 series. Better luck next time!")

# Run the game
play_best_of_three()
