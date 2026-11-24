
import customtkinter as ctk
import game_logic


# ==============================
# APPLICATION SETTINGS
# ==============================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title(" VU Tic Tac Toe ")
app.geometry("480x700")
app.resizable(False, False)
app.configure(fg_color="#101D29")


# ==============================
# GAME VARIABLES
# ==============================

player_name = ""
player_mark = "X"
computer_mark = "O"

player_score = 0
computer_score = 0
draw_score = 0

game_over = False
computer_thinking = False

buttons = []


# ==============================
# SCREEN MANAGEMENT
# ==============================

def show_screen(screen):

    setup_frame.pack_forget()
    game_frame.pack_forget()

    screen.pack(fill="both", expand=True)


# ==============================
# SETUP SCREEN
# ==============================

setup_frame = ctk.CTkFrame(
    app,
    fg_color="#101D29"
)

setup_title = ctk.CTkLabel(
    setup_frame,
    text="VU TIC TAC TOE",
    font=("Arial", 32, "bold"),
    text_color="#2EC4B6"
)
setup_title.pack(pady=(55, 10))


subtitle = ctk.CTkLabel(
    setup_frame,
    text="Play Against AI",
    font=("Arial", 17),
    text_color="#AABBC5"
)
subtitle.pack(pady=5)


name_label = ctk.CTkLabel(
    setup_frame,
    text="ENTER YOUR NAME",
    font=("Arial", 15, "bold")
)
name_label.pack(pady=(45, 10))


name_entry = ctk.CTkEntry(
    setup_frame,
    width=300,
    height=45,
    placeholder_text="Enter your name...",
    font=("Arial", 16),
    justify="center",
    corner_radius=12
)
name_entry.pack(pady=5)


symbol_label = ctk.CTkLabel(
    setup_frame,
    text="CHOOSE YOUR MARK",
    font=("Arial", 16, "bold")
)
symbol_label.pack(pady=(35, 15))


selected_mark = ctk.StringVar(value="X")


symbol_selector = ctk.CTkSegmentedButton(
    setup_frame,
    values=["X", "O"],
    variable=selected_mark,
    width=220,
    height=50,
    font=("Arial", 22, "bold"),
    selected_color="#2EC4B6",
    selected_hover_color="#20A99D"
)
symbol_selector.pack(pady=10)


selection_info = ctk.CTkLabel(
    setup_frame,
    text="You play first!",
    font=("Arial", 13),
    text_color="#AABBC5"
)
selection_info.pack(pady=10)


def updateSelection(value):

    if value == "X":
        selection_info.configure(
            text="You play first!"
        )
    else:
        selection_info.configure(
            text="Computer plays first!"
        )


symbol_selector.configure(
    command=updateSelection
)


status_text = ctk.CTkLabel(
    setup_frame,
    text="",
    font=("Arial", 13),
    text_color="#FF6B6B"
)
status_text.pack(pady=5)


# ==============================
# GAME SCREEN
# ==============================

game_frame = ctk.CTkFrame(
    app,
    fg_color="#101D29"
)


game_title = ctk.CTkLabel(
    game_frame,
    text="VU TIC TAC TOE",
    font=("Arial", 28, "bold"),
    text_color="#2EC4B6"
)
game_title.pack(pady=(20, 5))


player_info = ctk.CTkLabel(
    game_frame,
    text="",
    font=("Arial", 15, "bold")
)
player_info.pack(pady=5)


status = ctk.CTkLabel(
    game_frame,
    text="Your Turn!",
    font=("Arial", 19, "bold"),
    text_color="#2EC4B6"
)
status.pack(pady=12)


score_label = ctk.CTkLabel(
    game_frame,
    text="",
    font=("Arial", 14, "bold"),
    text_color="#FFFFFF"
)
score_label.pack(pady=8)


board_frame = ctk.CTkFrame(
    game_frame,
    fg_color="#172B36",
    corner_radius=15
)
board_frame.pack(pady=15)


# ==============================
# SCOREBOARD
# ==============================

def updateScore():

    score_label.configure(
        text=f"{player_name}: {player_score}   "
             f"DRAW: {draw_score}   "
             f"CPU: {computer_score}"
    )


# ==============================
# UPDATE BOARD
# ==============================

def updateBoard():

    for i in range(3):
        for j in range(3):

            value = game_logic.board[i][j]

            if value == player_mark:

                buttons[i][j].configure(
                    text=value,
                    text_color="#2EC4B6",
                    fg_color="#0714D5",
                    state="disabled"
                )

            elif value == computer_mark:

                buttons[i][j].configure(
                    text=value,
                    text_color="#F5B942",
                    fg_color="#E31010",
                    state="disabled"
                )

            else:

                buttons[i][j].configure(
                    text="",
                    state="normal",
                    fg_color="#203D49"
                )


# ==============================
# RESULT POPUP
# ==============================

def showResultPopup(title_text, message_text):

    popup = ctk.CTkToplevel(app)

    popup.title("Game Result")
    popup.geometry("350x280")
    popup.resizable(False, False)

    popup.configure(fg_color="#172B36")

    popup.transient(app)
    popup.grab_set()

    # Center Popup
    popup.update_idletasks()

    x = app.winfo_rootx() + (
        app.winfo_width() - 350
    ) // 2

    y = app.winfo_rooty() + (
        app.winfo_height() - 280
    ) // 2

    popup.geometry(f"350x280+{x}+{y}")

    # Result Title
    result_title = ctk.CTkLabel(
        popup,
        text=title_text,
        font=("Arial", 25, "bold"),
        text_color="#2EC4B6"
    )
    result_title.pack(pady=(30, 10))

    # Result Message
    result_message = ctk.CTkLabel(
        popup,
        text=message_text,
        font=("Arial", 16, "bold"),
        text_color="white"
    )
    result_message.pack(pady=15)

    # Button Frame
    button_frame = ctk.CTkFrame(
        popup,
        fg_color="transparent"
    )
    button_frame.pack(pady=25)

    # Next Round
    def nextRound():

        popup.destroy()

        global game_over
        global computer_thinking

        game_over = False
        computer_thinking = False

        game_logic.resetBoard()

        updateBoard()

        status.configure(
            text=f"{player_name}'s Turn!"
        )

        if player_mark == "O":
            computerTurn()

    next_button = ctk.CTkButton(
        button_frame,
        text="NEXT ROUND",
        width=130,
        height=40,
        font=("Arial", 13, "bold"),
        fg_color="#F5B942",
        hover_color="#D99C24",
        text_color="#101D29",
        command=nextRound
    )
    next_button.grid(row=0, column=0, padx=8)

    # Quit Game
    quit_button = ctk.CTkButton(
        button_frame,
        text="QUIT",
        width=100,
        height=40,
        font=("Arial", 13, "bold"),
        fg_color="#344955",
        hover_color="#455D69",
        command=app.destroy
    )
    quit_button.grid(row=0, column=1, padx=8)

    # Handle Popup Close
    popup.protocol(
        "WM_DELETE_WINDOW",
        nextRound
    )


# ==============================
# CHECK RESULT
# ==============================

def checkResult():

    global game_over
    global player_score
    global computer_score
    global draw_score

    score = game_logic.evaluate()

    if score == -10:

        game_over = True
        player_score += 1

        status.configure(
            text=f"{player_name} Wins!"
        )

        updateScore()
        updateBoard()

        showResultPopup(
            "YOU WON!",
            f"{player_name} takes the round!"
        )

        return True

    elif score == 10:

        game_over = True
        computer_score += 1

        status.configure(
            text="Computer Wins!"
        )

        updateScore()
        updateBoard()

        showResultPopup(
            "YOU LOST!",
            "Computer takes the round!"
        )

        return True

    elif not game_logic.isMovesLeft():

        game_over = True
        draw_score += 1

        status.configure(
            text="Game Draw!"
        )

        updateScore()
        updateBoard()

        showResultPopup(
            "GAME DRAW!",
            "Nobody wins this round!"
        )

        return True

    return False


# ==============================
# COMPUTER TURN
# ==============================

def computerTurn():

    global computer_thinking

    if game_over:
        return

    computer_thinking = True

    status.configure(
        text="Computer Thinking..."
    )

    def makeMove():

        global computer_thinking

        if game_over:
            computer_thinking = False
            return

        game_logic.computerMove()

        computer_thinking = False

        updateBoard()

        if not checkResult():

            status.configure(
                text=f"{player_name}'s Turn!"
            )

    app.after(400, makeMove)


# ==============================
# PLAYER MOVE
# ==============================

def playerMove(row, col):

    if game_over or computer_thinking:
        return

    value = game_logic.board[row][col]

    if value not in "123456789":
        return

    # Player Move
    game_logic.board[row][col] = player_mark

    updateBoard()

    if checkResult():
        return

    # Computer Move
    computerTurn()


# ==============================
# CREATE GAME BOARD
# ==============================

for i in range(3):

    row = []

    for j in range(3):

        button = ctk.CTkButton(
            board_frame,
            text="",
            width=105,
            height=105,
            font=("Arial", 38, "bold"),
            corner_radius=12,
            fg_color="#203D49",
            hover_color="#315565",
            command=lambda r=i, c=j: playerMove(r, c)
        )

        button.grid(
            row=i,
            column=j,
            padx=5,
            pady=5
        )

        row.append(button)

    buttons.append(row)


# ==============================
# START GAME
# ==============================

def startGame():

    global player_name
    global player_mark
    global computer_mark
    global game_over
    global computer_thinking
    global player_score
    global computer_score
    global draw_score

    player_name = name_entry.get().strip()

    if player_name == "":

        status_text.configure(
            text="Please enter your name!"
        )
        return

    player_mark = selected_mark.get()

    game_logic.setMarks(player_mark)

    computer_mark = game_logic.computer_mark

    # Reset Scores
    player_score = 0
    computer_score = 0
    draw_score = 0

    game_over = False
    computer_thinking = False

    player_info.configure(
        text=f"{player_name} ({player_mark})  VS  "
             f"Computer ({computer_mark})"
    )

    updateScore()
    updateBoard()

    status.configure(
        text=f"{player_name}'s Turn!"
    )

    show_screen(game_frame)

    # Computer starts if Player chooses O
    if player_mark == "O":
        computerTurn()


# ==============================
# RESTART ROUND
# ==============================

def restartGame():

    global game_over
    global computer_thinking

    game_over = False
    computer_thinking = False

    game_logic.resetBoard()

    updateBoard()

    status.configure(
        text=f"{player_name}'s Turn!"
    )

    if player_mark == "O":
        computerTurn()


# ==============================
# BACK TO SETUP
# ==============================

def backToSetup():

    global game_over
    global computer_thinking

    game_over = True
    computer_thinking = False

    name_entry.delete(0, "end")

    status_text.configure(text="")

    show_screen(setup_frame)


# ==============================
# GAME BUTTONS
# ==============================

restart_button = ctk.CTkButton(
    game_frame,
    text="RESTART ROUND",
    width=200,
    height=45,
    font=("Arial", 15, "bold"),
    corner_radius=12,
    fg_color="#2EC4B6",
    hover_color="#20A99D",
    command=restartGame
)
restart_button.pack(pady=15)


back_button = ctk.CTkButton(
    game_frame,
    text="NEW GAME / CHANGE PLAYER",
    width=230,
    height=38,
    font=("Arial", 12),
    fg_color="#344955",
    hover_color="#455D69",
    command=backToSetup
)
back_button.pack(pady=5)


# ==============================
# SETUP BUTTON
# ==============================

start_button = ctk.CTkButton(
    setup_frame,
    text="START GAME",
    width=260,
    height=50,
    font=("Arial", 17, "bold"),
    corner_radius=12,
    fg_color="#F5B942",
    hover_color="#D99C24",
    text_color="#101D29",
    command=startGame
)
start_button.pack(pady=25)


# ==============================
# START APPLICATION
# ==============================

show_screen(setup_frame)

app.mainloop()
