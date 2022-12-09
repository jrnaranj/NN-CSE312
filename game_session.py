import random
import logging
from threading import Barrier, Lock

win_conditions = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

class GameSession:
    def __init__(self, id=0):
        self.users = {}
        self.id = id
        self.check_wait = Barrier(2)
        self.lock = Lock()
        self.close_wait = Barrier(2)
    
    def add_user(self, username): 
        self.lock.acquire()
        if len(self.users) < 2:
            self.users[username] = None
            self.lock.release()
            return username
        else:
            print("Too many people in room! get out!")
            self.lock.release()
            return None

    def free_game(self):
        logging.warning("GameSession free: waiting at barrier")
        self.lock.acquire()
        self.users = None
        self.lock.release()
        self.check_wait.wait()
    
    def store_choice(self, username, choice):
        result = None
        if self.users[username]:
            print("Don't cheat!")
        else:
            self.lock.acquire()
            self.users[username] = choice
            self.lock.release()
            result = self.check_result()
        return result

    def reset_choices(self):
        self.lock.acquire()
        for u in self.users:
            self.users[u] = None
        self.lock.release()
    
    def check_result(self) -> str:
        if len(self.users) != 2:
            print("There has to be exactly 2 people in a room")
            return None
        self.check_wait.wait()
        if self.users == None:
            return ""
        prevUser = None
        self.lock.acquire()
        for u in self.users:
            logging.warning("Gamesession check_result: entered loop")
            user_choice = self.users[u]
            if not prevUser: prevUser = u
            else:
                if win_conditions[self.users[prevUser]] == user_choice: 
                    self.lock.release()
                    return prevUser
                elif win_conditions[user_choice] == self.users[prevUser]: 
                    self.lock.release()
                    return u
                else: 
                    self.lock.release()
                    return "<draw>"
        