# Wallet system that tracks the user's balance. user can bet the money in game and win/lose
import os
from colorama import Fore, Style, init

# Initialize colorama
init()

class Wallet:
    def __init__(self):
        self.balance = 1000  # Starting balance of $1000

    def get_balance(self):
        return self.balance

    def add_money(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"{Fore.GREEN}Added ${amount}. New balance: ${self.balance}{Style.RESET_ALL}")
            return True
        return False

    def remove_money(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            print(f"{Fore.YELLOW}Removed ${amount}. New balance: ${self.balance}{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}Insufficient funds! Current balance: ${self.balance}{Style.RESET_ALL}")
        return False

    def place_bet(self, amount):
        return self.remove_money(amount)

    def add_winnings(self, amount):
        return self.add_money(amount)
