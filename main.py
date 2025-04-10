#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
import time
import random
from tkinter import messagebox, simpledialog
from threading import Thread
from gcode_v3_new import *
from image_processing_using_template_matching import *

# Global variables
colour1 = '#222448'
colour2 = '#54527E'
current_page = 0
pages = []
connection_count = 0
page_button_count = 0
HUMAN = -1
COMP = +1
HUMAN_TURNS = +5
COMP_TURNS = +5
moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2],
    4: [1, 0], 5: [1, 1], 6: [1, 2],
    7: [2, 0], 8: [2, 1], 9: [2, 2],
}
h_choice = None
first = None

# Functions for rules page
def connect_printer():
    global connection_count
    connected = True
    if connection_count == 5:
        exit()
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200)
        connected = False
    except:
        connection_count += 1
    return connected, ser

# Initialization of printer to home
def init_game(ser):
    ser.write(init_gcode.encode())
    time.sleep(5)
    return False

# Toggle fullscreen and windowed mode
def half_screen():
    global page_button_count, page_button, photo_fullscreen, photo_windowed
    if page_button_count % 2 == 0:
        root.attributes('-fullscreen', False)
        page_button.config(image=photo_windowed)
    else:
        root.attributes('-fullscreen', True)
        page_button.config(image=photo_fullscreen)
    page_button_count += 1

def show_page():
    global current_page
    pages[current_page]()
def stop():
    global root
    root.quit()

def prev_page():
    global current_page, pages
    if current_page == 1:
        current_page -= 1
        bg_canvas.delete(ruletit2_text)
        bg_canvas.delete(rule4_text)
        bg_canvas.delete(rule5_text)
        bg_canvas.delete(rule6_text)
        bg_canvas.delete(prev2_window)
        bg_canvas.delete(next2_window)
        show_page()

def next_page():
    global current_page, pages
    if current_page == 0:
        current_page += 1
        bg_canvas.delete(rule_text)
        bg_canvas.delete(rule1_text)
        bg_canvas.delete(rule2_text)
        bg_canvas.delete(rule3_text)
        bg_canvas.delete(prev1_window)
        bg_canvas.delete(next1_window)
        show_page()
def select_shape(shape):
    global triangle_canvas, circle_canvas, h_choice
    h_choice = shape.upper()
    if shape == "Triangle":
        triangle_canvas.config(background="black")
        circle_canvas.config(background='white')
    else:
        circle_canvas.config(background="black")
        triangle_canvas.config(background="white")

def start_game():
    time.sleep(5)
    global first,h_choice,start_var,ser
    first =start_var.get().upper()
    print(first)
    print(h_choice)
    if first not in ['HUMAN', 'COMPUTER']:
        messagebox.showerror("Error", "Invalid choice for starting first. Please enter Yes or No.")
        return

    if h_choice is None:
        messagebox.showerror("Error", "Please select a shape.")
        return

    if h_choice == 'TRIANGLE':
        c_choice = 'CIRCLE'
    else:
        c_choice = 'TRIANGLE'
    bg_canvas.delete(shape_label_window)
    bg_canvas.delete(triangle_window)
    bg_canvas.delete(circle_window)
    bg_canvas.delete(start_label_window)
    bg_canvas.delete(start_option_window)
    bg_canvas.delete(game_window)
    game_thread = Thread(target=play_game, args=(h_choice, c_choice,first))
    game_thread.start()

def play_game(h_choice, c_choice, first):
        # Your game logic goes here
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    
    def empty_cells(state):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def valid_move(x, y):
        if [x, y] in empty_cells(board):
            return True
        else:
            return False

    def set_moveless3(move_n,xn, yn, COMP):
        shape = ''
        gcode = ''
        turn = 0

        global COMP_TURNS,ser
        
        if valid_move(xn, yn):
            board[xn][yn] = COMP
            shape = c_shape
            gcode = position[move_n]
            COMP_TURNS = COMP_TURNS - 1
            turn = COMP_TURNS
            #time.sleep(5)
            ser.write(shape.encode())
            #time.sleep(10)
            Pick_up(turn)
            ser.write(gcode.encode())
            #time.sleep(5)
            Drop()
            return True
        else:
            return False
    def set_movegreat3(move_n,move_o,xn, yn, COMP):
        shape = ''
        gcode = ''
        turn = 0

        global COMP_TURNS
        
        if valid_move(xn, yn):
            board[xn][yn] = COMP
            shape = c_shape
            gcode = position[move_n]
            
            #time.sleep(5)
            #ser.write(shape.encode())
            #time.sleep(5)
            Pick_up1(move_o)
            ser.write(gcode.encode())
            #time.sleep(5)
            Drop()
            return True
        else:
            return False
    def wins(state, player):
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(state):
        return wins(state, HUMAN) or wins(state, COMP)
    
    def check_draw(board):
        return all (board[i][j]!=0 for i in range(3) for j in range(3))


    def clean():
        pass
        
                

    def human_turn( h_choice,move_count):
        print('human turn',move_count)
        if move_count<3:
            #time.sleep(5)
            ser.write(h_turn.encode())
            #time.sleep(5)
            messagebox.showinfo("Tic Tac Toe Game", "Click OK if you have made your move.")

            moves = {
                1: [0, 0], 2: [0, 1], 3: [0, 2],
                4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 9: [2, 2],
            }
            ser.write(camera.encode())
            #time.sleep(5)
            tri_loc_img = shape_detect(h_choice)
            print(tri_loc_img)
            tri_loc_brd=[]
    
            for i in range(3):
                for j in range(3):
                    if board[i][j]==-1:
                        for move_k,move_v in moves.items():
                            if move_v==[i,j]:
                                tri_loc_brd.append(move_k)
            for i in tri_loc_img:
                if i not in tri_loc_brd:
                    move_n=i
            coord = moves[move_n]
            board[coord[0]][coord[1]] = HUMAN
            #time.sleep(1)
        else:
            #time.sleep(5)
            ser.write(h_turn.encode())
            #time.sleep(5)
            messagebox.showinfo("Tic Tac Toe Game", "Click OK if you have made your move.")

            moves = {
                1: [0, 0], 2: [0, 1], 3: [0, 2],
                4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 9: [2, 2],
            }
            ser.write(camera.encode())
            time.sleep(5)
            tri_loc_img = shape_detect(h_choice)
            print(tri_loc_img)
            tri_loc_brd=[]
    
            for i in range(3):
                for j in range(3):
                    if board[i][j]==-1:
                        for move_k,move_v in moves.items():
                            if move_v==[i,j]:
                                tri_loc_brd.append(move_k)
            print('old triangle positions in brd',tri_loc_brd)
            for i in tri_loc_img:
                if i not in tri_loc_brd:
                    move_n=i
            coord = moves[move_n]
            board[coord[0]][coord[1]] = HUMAN
            #time.sleep(1)
            for j in tri_loc_brd:
                if j not in tri_loc_img:
                    move_o=j
            print('human new', move_n)
            print('human old',move_o)
            oldcoord=moves[move_o]
            board[oldcoord[0]][oldcoord[1]]=0
            
            
    def ai_turn(board,COMP,HUMAN,move_count):
            print('ai turns',move_count)
            if move_count < 3:
                best_move = find_best_move(board,COMP,HUMAN,move_count)
                if best_move:
                    xn,yn=best_move[0],best_move[1]
                for move_n in moves:
                    if moves[move_n] == [xn,yn]:
                        break
                    else:
                        continue
                print('move_n',best_move[0],best_move[1],move_n)
                set_moveless3(move_n,xn, yn, COMP)
                time.sleep(1)
            else:
                best_move = find_best_move(board,COMP,HUMAN,move_count)
                if best_move:
                    source, dest = best_move
                    xn,yn=dest[0],dest[1]
                    xo,yo=source[0],source[1]
                    board[xo][yo] = 0

                for move_n in moves:
                    if moves[move_n] == [xn,yn]:
                        break
                    else:
                        continue
                for move_o in moves:
                    if moves[move_o] == [xo,yo]:
                        break
                    else:
                        continue
                print('new position: ',move_n)
                print('old position',move_o)
                set_movegreat3(move_n,move_o,xn, yn, COMP)
            #time.sleep(1)
    def find_best_move(board, COMP, HUMAN, move_count):
        best_move = None
        best_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        if move_count < 3:
            for move in empty_cells(board):
                board[move[0]][move[1]] = COMP
                eval = minimax(board, 0, False,COMP, HUMAN, alpha, beta)
                board[move[0]][move[1]] = 0
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
        else:
            for coin in [(i, j) for i in range(3) for j in range(3) if board[i][j] == COMP]:
                for move in empty_cells(board):
                    if abs(coin[0] - move[0]) + abs(coin[1] - move[1]) == 1:
                        board[coin[0]][coin[1]] = 0
                        board[move[0]][move[1]] = COMP
                        eval = minimax(board, 0, False, COMP, HUMAN, alpha, beta)
                        board[coin[0]][coin[1]] = COMP
                        board[move[0]][move[1]] = 0
                        if eval > best_eval:
                            best_eval = eval
                            best_move = (coin, move)
        return best_move
    def minimax(board, depth, maximizing_player, computer_char, player_char, alpha, beta):
        if wins(board, computer_char):
            return 10 - depth
        elif wins(board, player_char):
            return depth - 10
        elif check_draw(board):
            return 0
        if maximizing_player:
            max_eval = float('-inf')
            for move in empty_cells(board):
                board[move[0]][move[1]] = computer_char
                eval = minimax(board, depth + 1, False, computer_char, player_char, alpha, beta)
                board[move[0]][move[1]] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in empty_cells(board):
                board[move[0]][move[1]] = player_char
                eval = minimax(board, depth + 1, True, computer_char, player_char, alpha, beta)
                board[move[0]][move[1]] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def main():
        global h_choice, c_shape, COMP, HUMAN, HUMAN_TURNS, COMP_TURNS, moves
        h_choice = h_choice  # This line isn't necessary, as it's just referencing the global variable.

        if h_choice is None:
            raise ValueError("Shape choice must be set before starting the game.")

        if h_choice == 'TRIANGLE':
            c_choice = 'CIRCLE'
            h_shape = Goto_triangle
            c_shape = Goto_circle
        else:
            c_choice = 'TRIANGLE'
            h_shape = Goto_circle
            c_shape = Goto_triangle

        move_count = 0
        while not game_over(board):
            if first == 'COMPUTER':
                ai_turn(board, COMP, HUMAN, move_count)
                if wins(board, HUMAN):
                    messagebox.showinfo("Game Over", "YOU WIN!")
                    break
                elif wins(board, COMP):
                    messagebox.showinfo("Game Over", "YOU LOSE!")
                    break
                human_turn(h_choice, move_count)
                if wins(board, HUMAN):
                    messagebox.showinfo("Game Over", "YOU WIN!")
                    break
                elif wins(board, COMP):
                    messagebox.showinfo("Game Over", "YOU LOSE!")
                    break
                move_count += 1
            else:
                human_turn(h_choice, move_count)
                if wins(board, HUMAN):
                    messagebox.showinfo("Game Over", "YOU WIN!")
                    break
                elif wins(board, COMP):
                    messagebox.showinfo("Game Over", "YOU LOSE!")
                    break
                ai_turn(board, COMP, HUMAN, move_count)
                if wins(board, HUMAN):
                    messagebox.showinfo("Game Over", "YOU WIN!")
                    break
                elif wins(board, COMP):
                    messagebox.showinfo("Game Over", "YOU LOSE!")
                    break
                move_count += 1
        init_game(ser)
        ser.close()
        exit()


    main()

    

def launch():
    # Deleting windows in the launch page
    bg_canvas.delete(ruletit2_text)
    bg_canvas.delete(rule4_text)
    bg_canvas.delete(rule5_text)
    bg_canvas.delete(rule6_text)
    bg_canvas.delete(prev2_window)
    bg_canvas.delete(next2_window)

    # Shape selecting label
    global shape_label_window
    shape_label_window = bg_canvas.create_text(800, 200, text="Choose a shape:", font=('algerian', 20, 'bold'), fill='white')

    # Triangle and circle canvas
    global triangle_window, circle_window,start_label_window,start_option_window,game_window,triangle_canvas,circle_canvas
    triangle_canvas = Canvas(root, width=100, height=100, bg="white", highlightthickness=3, highlightbackground="white")
    triangle_canvas.create_polygon(50, 10, 10, 90, 90, 90, fill='#48CAE4')
    triangle_canvas.bind("<Button-1>", lambda event: select_shape("Triangle"))
    triangle_window = bg_canvas.create_window(650, 400, window=triangle_canvas)

    circle_canvas = Canvas(root, width=100, height=100, bg="white", highlightthickness=3, highlightbackground="white")
    circle_canvas.create_oval(10, 10, 90, 90, fill='#FFAAFF')
    circle_canvas.bind("<Button-1>", lambda event: select_shape("Circle"))
    circle_window = bg_canvas.create_window(950, 400, window=circle_canvas)

    # Selecting who is gonna start first
    start_label_window = bg_canvas.create_text(800, 550, text='Choose who starts first:', font=('Algerian', 20, 'bold'), fill='white')


    # Creating drop boxes for choices
    global start_var
    start_var = StringVar()
    start_var.set("Human")

    colour_bg1 = 'WHITE'
    colour_fg1 = '#6330ff'
    colour_bg2 = 'black'
    colour_fg2 = '#cbbaff'

    global caret_down_image
    caret_down_image = ImageTk.PhotoImage(Image.open(r'/home/pcblab/Downloads/caret_rect.png').resize((10,10)))
    start_option = OptionMenu(root, start_var, "Human", "Computer")
    start_option.config(bg=colour_bg2, fg=colour_fg2, activebackground=colour_bg1, activeforeground=colour_fg1, font=('castellar', 10, 'bold'), border=0, highlightthickness=1, highlightbackground=colour_bg2, indicatoron=0, compound=RIGHT, image=caret_down_image,padx=30)
    start_option['menu'].config(bg=colour_bg1, fg=colour_fg1, activebackground=colour_bg2, activeforeground=colour_fg2, font=('castellar', 10, 'bold'), border=0)
    start_option_window = bg_canvas.create_window(800, 630, window=start_option)

    game_button = Button(root, bg='white', fg='dark blue', activebackground=colour1, activeforeground='white', highlightthickness=2, highlightbackground='white', highlightcolor='dark blue', width=10, height=1, text='Next', font=('Arial', 14, 'bold'), command=start_game,cursor='spider')
    game_window = bg_canvas.create_window(1200, 700, window=game_button)

# Define pages content
def page1():
    global rule_text, rule1_text, rule2_text, rule3_text, prev1_window, next1_window
    rule_text = bg_canvas.create_text(900, 200, text='Rules of the game', font=('algerian', 24, 'bold'), fill='white')
    rule1_text = bg_canvas.create_text(490, 300, text='↠ Select your shape', font=('times', 20), fill='white', justify=LEFT)
    rule2_text = bg_canvas.create_text(595, 350, text='↠ Choose whether you want to start first', font=('times', 20), fill='white', justify=LEFT)
    rule3_text = bg_canvas.create_text(790, 400, text='↠ For first 3 moves, you can place your coins in empty slots at alternate turns', font=('times', 20), fill='white', justify=LEFT)
    prev_button = Button(root, background='white', foreground='dark blue', activebackground=colour1, activeforeground='white', disabledforeground=colour2, highlightthickness=0, width=10, relief=FLAT, height=1, font=('Arial', 16, 'bold'), state=DISABLED, text='Previous', command=prev_page, cursor='spider')
    next_button = Button(root, background='white', foreground='dark blue', activebackground=colour1, activeforeground='white', disabledforeground='#3B3A56', highlightthickness=0, width=10, relief=FLAT, height=1, font=('Arial', 16, 'bold'), text='Next', command=next_page, cursor='spider')
    prev1_window = bg_canvas.create_window(550, 600, window=prev_button)
    next1_window = bg_canvas.create_window(1200, 610, window=next_button)

def page2():
    global ruletit2_text, rule4_text, rule5_text, rule6_text, prev2_window, next2_window
    ruletit2_text = bg_canvas.create_text(900, 200, text='Rules of the game', font=('algerian', 24, 'bold'), fill='white')
    rule4_text = bg_canvas.create_text(900, 300, text='↠ After 3 moves you are only allowed to change the places of your coin as given below', font=('times', 20), fill='white', justify=LEFT)
    rule5_text = bg_canvas.create_text(605, 350, text='↠ One step horizontal or vertical', font=('times', 20), fill='white', justify=LEFT)
    rule6_text = bg_canvas.create_text(870, 400, text='↠ You win if you place three coins in a straight line(horizontal, vertical, diagonal)', font=('times', 20), fill='white', justify=LEFT)
    prev_button = Button(root, background='white', foreground='dark blue', activebackground=colour1, activeforeground='white', disabledforeground=colour2, highlightthickness=0, width=10, height=1, relief=FLAT, font=('Arial', 16, 'bold'), state=NORMAL, text='Previous', command=prev_page, cursor='spider')
    next_button = Button(root, background='white', foreground='dark blue', activebackground=colour1, activeforeground='white', disabledforeground='#3B3A56', highlightthickness=0, width=10, height=1, relief=FLAT, font=('Arial', 16, 'bold'), text='Launch', command=launch, cursor='spider')
    prev2_window = bg_canvas.create_window(550, 600, window=prev_button)
    next2_window = bg_canvas.create_window(1200, 610, window=next_button)

pages.extend([page1, page2])

# Main window settings
root = Tk()
root.geometry('1900x1000')
root.title('XCONNECT')
root.iconbitmap("@/home/pcblab/Downloads/game.xbm")

# Background
bg_canvas = Canvas(root, height=900, width=1900, border=0, highlightthickness=0)
bg_canvas.pack(fill='both', expand=True)
temp = Image.open(r"/home/pcblab/Downloads/XCON_EXT_BG.png")
bg = ImageTk.PhotoImage(temp)
bg_canvas.create_image(0,0, image=bg, anchor='nw')
title_text = bg_canvas.create_text(630, 300, text="XCONNECT", font=('Times roman', 50, "bold"), anchor='nw', fill='white')

# Exit button
im = Image.open(r'/home/pcblab/Downloads/exitimg2.png')
im = im.resize((30, 30))
photo_exit = ImageTk.PhotoImage(im)
exit_button = Button(root, image=photo_exit, command=stop, height=20, width=20, background='dark blue', relief=FLAT,cursor='spider')
exit_window = bg_canvas.create_window(1550, 20, window=exit_button)

# Toggle fullscreen button
im_fullscreen = Image.open(r'/home/pcblab/Downloads/floatingimg.jpg')
im_fullscreen = im_fullscreen.resize((30, 30))
photo_fullscreen = ImageTk.PhotoImage(im_fullscreen)

im_windowed = Image.open(r'/home/pcblab/Downloads/fullscrimg.jpg')
im_windowed = im_windowed.resize((30, 30))
photo_windowed = ImageTk.PhotoImage(im_windowed)

page_button = Button(root, image=photo_fullscreen, command=half_screen, height=20, width=20, background='dark blue', relief=FLAT,cursor='spider')
page_window = bg_canvas.create_window(1520, 20, window=page_button)

# Progress bar (optional, remove if not needed)
progress_bar = customtkinter.CTkProgressBar(root, orientation=HORIZONTAL, height=15, width=300, corner_radius=0, border_width=4, border_color='dark blue', fg_color='dark blue', progress_color='white', determinate_speed=random.choice([15, 16, 14]), mode='determinate')
progress_window = bg_canvas.create_window(830, 550, window=progress_bar)
percent = bg_canvas.create_text(830, 580, text="0%", fill='white', font=('Times new roman', 15))
progress_bar.set(0)
for x in range(0, 3):
    if x==0:
        termination=True
        global ser
        while termination:
            termination,ser=connect_printer()
    progress_bar.step()
    bg_canvas.itemconfig(percent, text=f"{int(progress_bar.get() * 100)}%")
    root.update_idletasks()
    if x < 2:
        time.sleep(1)
connection_count = 0
init_game(ser)
time.sleep(1)

# Deleting widgets in the first page
bg_canvas.delete(progress_window)
bg_canvas.delete(percent)

# Functions
def start():
    bg_canvas.delete(title_text)
    bg_canvas.delete(start_window)
    bg_canvas.delete(quit_window)
    show_page()

# Start button
start_button = Button(root, bg='white', fg='dark blue', activebackground=colour1, activeforeground='white', highlightthickness=2, highlightbackground='white', highlightcolor='dark blue', width=10, height=1, text='Start', font=('Arial', 14, 'bold'), command=start,cursor='spider')
start_window = bg_canvas.create_window(650, 600, window=start_button)

# Quit button
quit_button = Button(root, bg='white', fg='dark blue', activebackground=colour1, activeforeground='white', highlightthickness=2, highlightbackground='white', highlightcolor='dark blue', width=10, height=1, text='Quit', font=('Arial', 14, 'bold'), command=root.quit,cursor='spider')
quit_window = bg_canvas.create_window(1050, 600, window=quit_button)

root.mainloop()
