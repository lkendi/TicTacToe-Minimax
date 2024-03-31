import tkinter as tk

DARK_GREY = '#333333'
WHITE = '#fcfcfc'
LABEL_FONT = ("Roboto", 20)
MOVES_FONT = ("Roboto", 20)
BUTTON_FONT = ("Roboto", 15)


class TicTacToeGame:
    def __init__(self):
        """Class constructor"""
        self.current_player = "X"
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("360x360")
        self.player_label = tk.Label(self.window, text="", font=LABEL_FONT)
        self.player_label.grid(row=0, columnspan=3)
        self.buttons = [[tk.Button(self.window, font=MOVES_FONT,
                                   command=lambda i=i, j=j: self.make_move(i, j))
                                   for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].grid(row=i+1, column=j, sticky="nsew")
        for i in range(4):
            self.window.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.window.grid_columnconfigure(j, weight=1)

        self.retry_button = tk.Button(self.window, text="Play Again",
                                      font=BUTTON_FONT, command=self.reset_game)
        self.retry_button.grid(row=4, columnspan=3)
        self.retry_button.grid_remove()

    def make_move(self, row, column):
        """Handles player's move and AI's move"""
        button = self.buttons[row][column]
        if button["text"] == "":
            button.config(text=self.current_player, state="disabled")
            self.board[row][column] = self.current_player
            if self.check_game_status():
                return
            self.switch_player()
            if self.current_player == "O":
                ai_row, ai_column = self.get_best_move()
                self.make_move(ai_row, ai_column)

    def switch_player(self):
        """Switches the current player"""
        self.current_player = "X" if self.current_player == "O" else "O"
        self.player_label.config(text=f"It's {self.current_player}'s turn!")

    def check_game_status(self):
        """Checks for win or tie"""
        if self.check_win("X"):
            self.show_winner("X")
            return True
        elif self.check_win("O"):
            self.show_winner("O")
            return True
        elif self.check_tie():
            self.show_tie()
            return True
        return False

    def check_win(self, player):
        """Checks if the player has won"""
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def check_tie(self):
        """Checks if the game ended in a tie"""
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))

    def show_winner(self, player):
        """Displays the winner"""
        self.player_label.config(text=f"Player {player} wins!")
        self.disable_buttons()
        self.retry_button.grid()

    def show_tie(self):
        """Displays tie message"""
        self.player_label.config(text="It's a tie!")
        self.disable_buttons()
        self.retry_button.grid()

    def is_game_over(self):
        """Check if the game is over."""
        return self.check_win("X") or self.check_win("O") or self.check_tie()

    def disable_buttons(self):
        """Disables all buttons"""
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def get_possible_moves(self):
        """Get possible moves in the current state."""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    moves.append((i, j))
        return moves

    def minimax(self, depth, is_maximizing):
        """Minimax algorithm implementation"""
        if self.is_game_over() or depth == 0:
            return self.evaluate()

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves():
                row, col = move
                self.board[row][col] = "X"
                eval = self.minimax(depth - 1, False)
                self.board[row][col] = ''
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves():
                row, col = move
                self.board[row][col] = "O"
                eval = self.minimax(depth - 1, True)
                self.board[row][col] = ''
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self):
        """Use Minimax algorithm to get AI's best move"""
        best_move = None
        best_eval = float('-inf')
        for move in self.get_possible_moves():
            row, col = move
            self.board[row][col] = "X"
            eval = self.minimax(3, False)
            self.board[row][col] = ''
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def evaluate(self):
        """Evaluates the current state of the board"""
        if self.check_win("X"):
            return 1
        elif self.check_win("O"):
            return -1
        else:
            return 0

    def reset_game(self):
        """Resets the game"""
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player_label.config(text="")
        self.retry_button.grid_remove()
        self.current_player = "X"


    def start_game(self):
        """Starts the game"""
        self.window.mainloop()


if __name__ == "__main__":
    """Entry point"""
    new_game = TicTacToeGame()
    new_game.start_game()
