# create a menu to select either tictactoe or gomoku
import os
from colorama import Fore, Style, init
from tictactoe import main as tictactoe_main
from gomoku import main as gomoku_main
from blackjack import main as blackjack_main
from wallet import Wallet

# Initialize colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_wallet(wallet):
    print(f"\n{Fore.YELLOW}Current Balance: ${wallet.get_balance()}{Style.RESET_ALL}")

def main():
    wallet = Wallet()  # Initialize wallet with $1000
    
    while True:
        clear_screen()
        print(f"{Fore.CYAN}Welcome to Board Games!{Style.RESET_ALL}")
        display_wallet(wallet)
        print("\nPlease select a game:")
        print(f"1. {Fore.GREEN}Tic Tac Toe{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Gomoku{Style.RESET_ALL}")
        print(f"3. {Fore.BLUE}Blackjack{Style.RESET_ALL}")
        print(f"4. {Fore.RED}Exit{Style.RESET_ALL}")

        try:
            choice = input("\nEnter your choice (1-4): ").lower()
            if choice == '1':
                clear_screen()
                tictactoe_main(wallet)
            elif choice == '2':
                clear_screen()
                gomoku_main(wallet)
            elif choice == '3':
                clear_screen()
                blackjack_main(wallet)
            elif choice in ['4', 'q', 'exit']:
                print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")
                break
            else:
                print("\nInvalid choice. Please enter 1-4.")
                input("\nPress Enter to continue...")
        except ValueError:
            print("\nInvalid input. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
