import random
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

def print_board(board):
    for i in range(3):
        row = []
        for j in range(3):
            cell = board[i*3 + j]
            if cell == "X":
                row.append(f"{Fore.GREEN}X{Style.RESET_ALL}")
            elif cell == "O": 
                row.append(f"{Fore.RED}O{Style.RESET_ALL}")
            else:
                row.append(" ")
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("-----------")

def check_winner(board):
    # Check rows, columns and diagonals
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]]
    
    if " " not in board:
        return "Tie"
    return None

def main(wallet):
    print(f"{Fore.CYAN}Select game mode:{Style.RESET_ALL}")
    print(f"1. {Fore.GREEN}Player{Style.RESET_ALL} vs {Fore.GREEN}Player{Style.RESET_ALL}")
    print(f"2. {Fore.GREEN}Player{Style.RESET_ALL} vs {Fore.RED}AI{Style.RESET_ALL}")
    
    # Get game mode
    while True:
        try:
            mode = input("Enter 1 or 2 (or 'q' to quit): ").lower()
            if mode in ['q', 'exit']:
                print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")
                return
            mode = int(mode)
            if mode in [1, 2]:
                break
            print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter 1, 2, or 'q' to quit.")

    # Get bet amount only for PvE mode
    bet = 0
    if mode == 2:
        while True:
            try:
                bet = input("\nEnter bet amount (or 'q' to quit): ").lower()
                if bet in ['q', 'exit']:
                    return
                bet = int(bet)
                if bet > 0 and wallet.place_bet(bet):
                    break
                print("Invalid bet amount.")
            except ValueError:
                print("Please enter a valid number.")
    
    board = [" " for _ in range(9)]
    current_player = "X"
    
    while True:
        print_board(board)
        if current_player == "X":
            print(f"Player {Fore.GREEN}{current_player}{Style.RESET_ALL}'s turn")
        else:
            print(f"Player {Fore.RED}{current_player}{Style.RESET_ALL}'s turn")
        
        if current_player == "X" or mode == 1:
            while True:
                try:
                    move = input("Enter position (1-9) or 'q' to quit: ").lower()
                    if move in ['q', 'exit']:
                        print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")
                        return
                    position = int(move) - 1
                    if 0 <= position <= 8 and board[position] == " ":
                        break
                    print("Invalid position. Try again.")
                except ValueError:
                    print("Please enter a number between 1-9 or 'q' to quit.")
        else:
            position = ai_move(board)
            print(f"AI chooses position {position + 1}")
        
        board[position] = current_player
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "Tie":
                print("It's a tie!")
                time.sleep(1.5)
                if mode == 2:
                    wallet.add_winnings(bet)  # Return bet on tie
            else:
                if mode == 2 and winner == "O":
                    print(f"{Fore.RED}AI wins!{Style.RESET_ALL}")
                    time.sleep(1.5)
                else:
                    if winner == "X":
                        print(f"Player {Fore.GREEN}{winner}{Style.RESET_ALL} wins!")
                        if mode == 2:
                            wallet.add_winnings(bet * 2)  # Double bet for winning
                        time.sleep(1.5)
                    else:
                        print(f"Player {Fore.RED}{winner}{Style.RESET_ALL} wins!")
                        time.sleep(1.5)
            break
            
        current_player = "O" if current_player == "X" else "X"

def ai_move(board):
    # First try to win
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if check_winner(board) == "O":
                return i
            board[i] = " "
    
    # Then block player from winning
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_winner(board) == "X":
                board[i] = "O"
                return i
            board[i] = " "
    
    # Take center if available
    if board[4] == " ":
        return 4
        
    # Take corners if available
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if board[i] == " "]
    if available_corners:
        return random.choice(available_corners)
    
    # Take any available edge
    edges = [1, 3, 5, 7]
    available_edges = [i for i in edges if board[i] == " "]
    if available_edges:
        return random.choice(available_edges)

if __name__ == "__main__":
    print(f"{Fore.CYAN}Welcome to Tic Tac Toe!{Style.RESET_ALL}")
    print("Positions are numbered from 1-9, left to right, top to bottom.")
    main()