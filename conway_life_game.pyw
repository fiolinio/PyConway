from tkinter import *


PXL_SIZE = 20
DIMS = (45, 80)  # Nombre de lignes, Nombre de colonnes
DELAY = 200
is_playing = False

def on_click(event):
    change_color(get_pixel(get_click(event)))
    return


def get_click(event):
    return (event.x, event.y)


def get_pixel(coords):
    line = coords[1]//PXL_SIZE
    column = coords[0]//PXL_SIZE
    return pixel_map[line][column]


def change_color(pixel):
    pixel_color = canvas.itemcget(pixel, "fill")
    if pixel_color == "white":
        canvas.itemconfigure(pixel, fill='black')
    else:
        canvas.itemconfigure(pixel, fill='white')
    return


def is_correct_coord(height, width):
    if height < 0 or height >= DIMS[0]:
        return False
    if width < 0 or width >= DIMS[1]:
        return False
    return True


def button_action():
    global is_playing
    global button
    is_playing = not is_playing
    if is_playing:
        button.config(text="Pause")
        play()
    else:
        button.config(text="Jouer")


def play():
    check_pixels = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]
    change_pixel = []
    for i in range(DIMS[0]):
        for j in range(DIMS[1]):  #  On teste le pixel au rang i, j
            alive_number = 0
            for p in check_pixels:
                if is_correct_coord(i+p[0], j+p[1]):
                    if canvas.itemcget(pixel_map[i+p[0]][j+p[1]], "fill") == 'black':
                        alive_number += 1
            if canvas.itemcget(pixel_map[i][j], "fill") == 'white' and alive_number == 3:
                change_pixel.append(pixel_map[i][j])
            elif canvas.itemcget(pixel_map[i][j], "fill") == 'black' and (alive_number < 2 or alive_number > 3):
                change_pixel.append(pixel_map[i][j])
    for pixel in change_pixel:
        change_color(pixel)
    if is_playing:
        window.after(DELAY, play)


def reset_grid():
    for i in range(DIMS[0]):
        for j in range(DIMS[1]):
            canvas.itemconfigure(pixel_map[i][j], fill='white')
    global is_playing
    button.config(text="Jouer")
    is_playing = False


pixel_map = []


window = Tk()
window.title("Jeu de la vie")
canvas = Canvas(window, width=PXL_SIZE*DIMS[1], height=PXL_SIZE*DIMS[0])
for i in range(DIMS[0]):
    temp_line = []
    for j in range(DIMS[1]):
        temp_line.append(canvas.create_rectangle(j*PXL_SIZE, i*PXL_SIZE, (j+1)*PXL_SIZE, (i+1)*PXL_SIZE, fill='white'))
    pixel_map.append(temp_line)
del temp_line
canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
canvas.bind("<Button-1>", on_click)
button = Button(window, text="Jouer", command=button_action)
button.grid(row=1, column=0, pady=10, padx=10, sticky='E')
reset = Button(window, text="Réinitialiser", command=reset_grid)
reset.grid(row=1, column=1, pady=10, padx=10, sticky='W')

window.mainloop()
