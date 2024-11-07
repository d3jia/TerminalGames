# create a blackjack game
import os
from colorama import Fore, Style, init

# Initialize colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck

def calculate_hand(hand):
    value = 0
    aces = 0
    
    for card in hand:
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            aces += 1
        else:
            value += int(rank)
    
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
            
    return value

def print_hand(hand, hide_first=False):
    cards = []
    for i, (rank, suit) in enumerate(hand):
        if i == 0 and hide_first:
            cards.append('??')
        else:
            if suit in ['♥', '♦']:
                cards.append(f"{Fore.RED}{rank}{suit}{Style.RESET_ALL}")
            else:
                cards.append(f"{rank}{suit}")
    return ' '.join(cards)

def main(wallet):
    import random
    
    while True:
        clear_screen()
        print(f"{Fore.GREEN}Welcome to Blackjack!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Current Balance: ${wallet.get_balance()}{Style.RESET_ALL}")
        
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
        
        # Create and shuffle deck
        deck = create_deck()
        random.shuffle(deck)
        
        # Initial deal
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        # Game loop
        while True:
            clear_screen()
            print(f"\nDealer's hand: {print_hand(dealer_hand, hide_first=True)}")
            print(f"Your hand: {print_hand(player_hand)} (Value: {calculate_hand(player_hand)})")
            
            if calculate_hand(player_hand) > 21:
                print(f"\n{Fore.RED}Bust! You lose!{Style.RESET_ALL}")
                break
                
            action = input("\nWhat would you like to do? (h)it, (s)tand, or (q)uit: ").lower()
            
            if action == 'q':
                print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")
                return
            elif action == 'h':
                player_hand.append(deck.pop())
            elif action == 's':
                # Dealer's turn
                while calculate_hand(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                
                clear_screen()
                print(f"\nDealer's hand: {print_hand(dealer_hand)} (Value: {calculate_hand(dealer_hand)})")
                print(f"Your hand: {print_hand(player_hand)} (Value: {calculate_hand(player_hand)})")
                
                dealer_value = calculate_hand(dealer_hand)
                player_value = calculate_hand(player_hand)
                
                if dealer_value > 21:
                    print(f"\n{Fore.GREEN}Dealer busts! You win!{Style.RESET_ALL}")
                    wallet.add_winnings(bet * 2)  # Return original bet plus winnings
                elif dealer_value > player_value:
                    print(f"\n{Fore.RED}Dealer wins!{Style.RESET_ALL}")
                elif dealer_value < player_value:
                    print(f"\n{Fore.GREEN}You win!{Style.RESET_ALL}")
                    wallet.add_winnings(bet * 2)  # Return original bet plus winnings
                else:
                    print(f"\n{Fore.YELLOW}Push! It's a tie!{Style.RESET_ALL}")
                    wallet.add_winnings(bet)  # Return original bet
                break
        
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
