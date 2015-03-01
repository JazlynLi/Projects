from queue import Queue
from threading import Thread, Lock
from datetime import datetime
from hog import play
import json
import os

class Player:
    def __init__(self, name):
        self.name=name
        self.queue = Queue()
    def MakeMove(self, dice):
        """
        Puts <dice> as the next move in this player's queue.
        This unblocks the play() thread, because the queue is
        non-empty.
        """
        self.queue.put(dice)

class Game:
    counter = 0
    def __init__(self):
        Game.counter += 1
        self.player0 = None
        self.player1 = None
        self.score0 = 0
        self.score1 = 0
        self.HasScore = False
        self.state = 0
    def AddPlayer(self, p):
        """
        Adds player <p> to the game.
        """
        if self.player0 == None:
            self.player0 = p
        elif self.player1 == None:
            self.player1 = p
        else:
            assert(False)
    def DoMove(self,player_id,dice):
        """
        Makes <player_id> roll <dice> dice.
        """
        self.HasScore = False
        if player_id == 0:
            self.player0.MakeMove(dice)
        elif player_id == 1:
            self.player1.MakeMove(dice)
        else:
            assert(False)
        while not self.HasScore:
            pass
        return self.score0, self.score1
    def Start(self):
        """
        Starts a game of Hog in parallel with the server using a thread. The two
        strategy functions pull rolls from a python Queue, which is a data
        structure for multithreaded python programs. The queue blocks the
        current thread if the current thread attempts to dequeue an element.
        This essentially forces play()'s thread to wait for each player to make
        a move before continuing.

        For more information on threads:
        https://docs.python.org/3/library/threading.html

        For more information on queues:
        https://docs.python.org/3/library/queue.html
        """
        def Strategy0(score, opponent_score):
            """
            Player0's strategy. Updates this game's internal state with score
            and opponent_score.
            """
            self.score0 = score
            self.score1 = opponent_score
            self.state = 0
            self.HasScore = True
            return self.player0.queue.get()
        def Strategy1(score, opponent_score):
            """
            Player1's strategy. Updates this game's internal state with score
            and opponent_score.
            """
            self.score1 = score
            self.score0 = opponent_score
            self.state = 1
            self.HasScore = True
            return self.player1.queue.get()
        def RunGame():
            """
            A wrapper function that runs the Hog game.
            """
            self.score0, self.score1 = play(Strategy0, Strategy1)
            self.state = -1
            self.HasScore = True
        # Run RunGame in a separate thread. This one runs function RunGame
        # concurrently with the rest of the code.
        self.game_thread = Thread(target = RunGame)
        self.game_thread.start()

    def CanPlay(self, player_id):
        print(self.ready, self.state, player_id)
        return self.ready and self.state == player_id

    def Turn(self):
        """
        Find out who's turn it is. If the game is over or hasn't started, return -1.
        """
        if self.player0 == None or self.player1 == None:
            return -1
        return self.state

    def Winner(self):
        """
        Return the winer of this game, or 
        """
        if self.state != -1:
            return False
        elif self.score0 >= 100:
            return 0
        elif self.score1 >= 100:
            return 1
        else:
            assert(False)

    def Score(self, player_id):
        """
        Return <player_id>'s score.
        """
        if player_id == 0:
            return self.score0
        elif player_id == 1:
            return self.score1
        else:
            assert(False)

    def Player(self,player_id):
        """
        Return <player_id>'s name.
        """
        if player_id == 0:
            if self.player0 != None:
                return self.player0.name
            else:
                return False
        elif player_id == 1:
            if self.player1 != None:
                return self.player1.name
            else:
                return False
        else:
            assert(False)

    @property
    def ready(self):
        return self.player0 != None and self.player1 != None

class HogOnline:
    def __init__(self):
        self.games = {}
        self.state_lock = Lock()
    def Join(self, name):
        """
        Return the id of an empty game and the id of the player within the game.
        """
        player_id = None
        game_id = None
        with self.state_lock:
            player = Player(name)
            for key in self.games:
                if not self.games[key].ready:
                    self.games[key].AddPlayer(player)
                    self.games[key].Start()
                    game_id = key
                    player_id = 1
            if game_id == None:
                # No empty games. Open a new one.
                game_id = Game.counter
                self.games[game_id] = Game()
                self.games[game_id].AddPlayer(player)
                player_id = 0
        return json.dumps({
            'id':player_id,
            'game':game_id,
        })
    def RollDice(self, game, player_id, dice):
        """
        Rolls <dice> dice for <player_id> in <game>.
        Returns an error if the it is not <player_id>'s turn.
        """
        if int(dice) < 0 or int(dice) > 10:
            return json.dumps({'error':True})
        if self.games[int(game)].CanPlay(int(player_id)):
            score0, score1 = self.games[int(game)].DoMove(int(player_id),int(dice))
            return json.dumps({'error':False,'score0':score0,'score1':score1})
        else:
            return json.dumps({'error':True})
    def GameStatus(self, game):
        """
        Returns the status of game <game>.
        """
        if int(game) not in self.games:
            return json.dumps({})
        game = self.games[int(game)]
        return json.dumps({
            'player0':game.Player(0),
            'player1':game.Player(1),
            'score0':game.Score(0),
            'score1':game.Score(1),
            'turn':game.Turn(),
            'winner':game.Winner(),
            })

hog = HogOnline()
