# Gomoku terminal 
import random
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

def print_board(board):
    # Print column letters
    print("   ", end="")
    for i in range(15):
        # Cycle through colors for column letters
        color = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA][i % 5]
        print(f"{color}{chr(65+i)}{Style.RESET_ALL}", end=" ")
    print()
    
    # Print rows with row numbers
    for i in range(15):
        # Cycle through colors for row numbers
        color = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA][i % 5]
        print(f"{color}{i:2}{Style.RESET_ALL} ", end="")
        for j in range(15):
            if board[i][j] == "B":
                print(f"{Fore.BLACK}● {Style.RESET_ALL}", end="")
            elif board[i][j] == "W":
                print(f"{Fore.WHITE}● {Style.RESET_ALL}", end="")
            else:
                print("· ", end="")
        print()

def check_winner(board, row, col, piece):
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horizontal, vertical, diagonal
    
    for dr, dc in directions:
        count = 1
        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == piece:
            count += 1
            r += dr
            c += dc
        
        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == piece:
            count += 1
            r -= dr
            c -= dc
            
        if count >= 5:
            return True
    return False

def is_valid_move(board, row, col):
    return 0 <= row < 15 and 0 <= col < 15 and board[row][col] == " "

def parse_move(move):
    if len(move) < 2:
        return None, None
    
    col = ord(move[0].upper()) - ord('A')
    try:
        row = int(move[1:])
    except ValueError:
        return None, None
        
    return row, col

def ai_move(board):
    # First try to win
    for i in range(15):
        for j in range(15):
            if board[i][j] == " ":
                board[i][j] = "W"
                if check_winner(board, i, j, "W"):
                    return i, j
                board[i][j] = " "
    
    # Then block player from winning
    for i in range(15):
        for j in range(15):
            if board[i][j] == " ":
                board[i][j] = "B"
                if check_winner(board, i, j, "B"):
                    return i, j
                board[i][j] = " "
    
    # Take center area if available
    center_moves = [(7,7), (7,8), (8,7), (8,8)]
    available_centers = [(i,j) for i,j in center_moves if board[i][j] == " "]
    if available_centers:
        return random.choice(available_centers)
    
    # Take random valid move
    valid_moves = [(i,j) for i in range(15) for j in range(15) if board[i][j] == " "]
    return random.choice(valid_moves)

def main(wallet):
    print(f"{Fore.CYAN}Select game mode:{Style.RESET_ALL}")
    print(f"1. {Fore.GREEN}Player{Style.RESET_ALL} vs {Fore.GREEN}Player{Style.RESET_ALL}")
    print(f"2. {Fore.GREEN}Player{Style.RESET_ALL} vs {Fore.RED}AI{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Current Balance: ${wallet.get_balance()}{Style.RESET_ALL}")
    
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

    # Get bet amount
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

    board = [[" " for _ in range(15)] for _ in range(15)]
    current_player = "B"  # B for Black, W for White
    
    print(f"{Fore.CYAN}Welcome to Gomoku!{Style.RESET_ALL}")
    print("Enter moves in format <column><row> (e.g. A0, B5, O14)")
    print("Enter 'q' or 'exit' to quit.")
    
    while True:
        print_board(board)
        if current_player == "B":
            print(f"{Fore.BLACK}Black{Style.RESET_ALL}'s turn")
        else:
            print(f"{Fore.WHITE}White{Style.RESET_ALL}'s turn")
        
        if current_player == "B" or mode == 1:
            while True:
                move = input("Enter move (e.g. A0): ").lower()
                if move in ['q', 'exit']:
                    print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")
                    return
                    
                row, col = parse_move(move)
                if row is not None and col is not None and is_valid_move(board, row, col):
                    break
                print("Invalid move. Try again.")
        else:
            print("AI is thinking...")
            time.sleep(1)
            row, col = ai_move(board)
            print(f"AI plays: {chr(65+col)}{row}")
        
        board[row][col] = current_player
        
        if check_winner(board, row, col, current_player):
            print_board(board)
            winner = "Black" if current_player == "B" else "White"
            if mode == 2:
                if winner == "White":
                    print(f"{Fore.RED}AI wins!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}You win!{Style.RESET_ALL}")
                    wallet.add_winnings(bet * 2)  # Player wins double their bet against AI
            else:
                if winner == "Black":
                    print(f"{Fore.BLACK}{winner} wins!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{winner} wins!{Style.RESET_ALL}")
                wallet.add_winnings(bet * 2)  # Winner gets double their bet in PvP
            time.sleep(3)
            return
            
        # Check for draw (full board)
        if all(cell != " " for row in board for cell in row):
            print_board(board)
            print(f"{Fore.YELLOW}It's a draw!{Style.RESET_ALL}")
            wallet.add_winnings(bet)  # Return the original bet on draw
            time.sleep(3)
            return
            
        current_player = "W" if current_player == "B" else "B"

if __name__ == "__main__":
    main()
