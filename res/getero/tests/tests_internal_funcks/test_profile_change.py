from res.getero.algorithm.dynamic_profile import delete_point, give_coords_from_num
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle


def generate_border_layer(prev_num, next_num, po_chas, curr_x, curr_y):
    delta_x, delta_y = curr_x-1, curr_y-1
    curr_border_layer = np.zeros((3+delta_x, 3+delta_y, 5))
    prev_x, prev_y = give_coords_from_num(prev_num, curr_x, curr_y)
    next_x, next_y = give_coords_from_num(next_num, curr_x, curr_y)
    curr_border_layer[prev_x, prev_y, :] = [1, -1, -1, curr_x, curr_y]
    curr_border_layer[curr_x, curr_y, :] = [1, prev_x, prev_y, next_x, next_y]
    curr_border_layer[next_x, next_y, :] = [1, curr_x, curr_y, -1, -1]
    if po_chas:
        add = 1
    else:
        add = -1
    i = (prev_num+add)%8
    #заполняем пустотой
    while i!=next_num:
        x, y = give_coords_from_num(i, curr_x, curr_y)
        curr_border_layer[x, y, :] = [-1, 0, 0, 0, 0]
        i = (i+add)%8
    i = (prev_num - add) % 8
    # заполняем пустотой
    while i != next_num:
        x, y = give_coords_from_num(i, curr_x, curr_y)
        curr_border_layer[x, y, :] = [0, 0, 0, 0, 0]
        i = (i - add) % 8


    return curr_border_layer.astype(int), prev_x, prev_y, next_x, next_y


def plot_line(bl, axis, prev_x, prev_y, next_x, next_y, curr_x, curr_y, size=10):
    x, y = prev_x, prev_y
    X = []
    Y = []
    while x!=next_x or y!=next_y:
        X.append((x - curr_x + 1.5) * size)
        Y.append((y - curr_y + 1.5) * size)
        x, y = bl[x, y, 3], bl[x, y, 4]
    X.append((x - curr_x + 1.5) * size)
    Y.append((y - curr_y + 1.5) * size)
    circ = Circle(((prev_x - curr_x + 1.5)*size, (prev_y - curr_y + 1.5)*size), 0.2*size, color="k")
    axis.add_patch(circ)
    axis.plot(X, Y, color="k")


#border_layer, prev_x, prev_y, next_x, next_y = generate_border_layer(0, 5, False)


def plot_border(bl,axis, curr_x, curr_y,size=10):
    for i in range(3):
        for j in range(3):
            color = "r"
            if bl[curr_x+i-1,curr_y+j-1,0]==0:
                color="y"
            elif bl[curr_x+i-1,curr_y+j-1,0]==-1:
                color="w"
            rect = Rectangle((i*size, j*size), size, size, color=color)
            axis.add_patch(rect)
            curr_str0 = "curr: " + str(int(i)) + "," + str(int(j))
            curr_str1 = "prev: " + str(int(bl[curr_x+i-1,curr_y+j-1, 1])) + "," + str(int(bl[curr_x+i-1,curr_y+j-1, 2]))
            curr_str2 = "next: " + str(int(bl[curr_x+i-1,curr_y+j-1, 3])) + "," + str(int(bl[curr_x+i-1,curr_y+j-1, 4]))
            #axis.text(i * size + 0.3*size, j * size + 0.7*size, curr_str0, color="k")
            #axis.text(i * size + 0.3*size, j * size + 0.5*size, curr_str1, color="k")
            #axis.text(i * size + 0.3*size, j * size + 0.3*size, curr_str2, color="k")
    axis.axvline(x=size,color="b")
    axis.axvline(x=2*size, color="b")
    #axis.axvline(x=30, color="b")
    axis.axhline(y=size, color="b")
    axis.axhline(y=2*size, color="b")
    axis.set_xlim((0, 3*size))
    axis.set_ylim((0, 3*size))
x_size = 1
y_size = 4
fig, axes = plt.subplots(2*x_size, y_size, figsize=(3*y_size, 6*x_size))
#print(axes.shape)
for i in range(x_size):
    for j in range(y_size):
        prev_num = 0#np.random.randint(0,  8)
        next_num = 6#np.random.randint(0, 8)
        print(prev_num, next_num)
        while np.abs(next_num-prev_num)<=1:
            next_num = np.random.randint(0, 8)
        print(prev_num, next_num)
        #prev_num = 4
        #next_num = 2
        curr_x = 1 + np.random.randint(0, 10)
        curr_y = 1 + np.random.randint(0, 10)

        do_pochas = bool(np.random.randint(0,2))
        border_layer, prev_x, prev_y, next_x, next_y = generate_border_layer(prev_num, next_num, do_pochas, curr_x, curr_y)

        plot_border(border_layer, axes[2*i, j], curr_x, curr_y)
        plot_line(border_layer, axes[2*i, j], prev_x, prev_y, next_x, next_y, curr_x, curr_y)

        border_layer2 = border_layer.copy()
        #print(border_layer2)
        delete_point(border_layer2, is_full_arr, curr_x, curr_y)

        plot_border(border_layer2, axes[2*i+1, j], curr_x, curr_y)
        plot_line(border_layer2, axes[2*i+1, j], prev_x, prev_y, next_x, next_y, curr_x, curr_y)

        axes[i * 2 + 0, j].get_xaxis().set_visible(False)
        axes[i * 2 + 1, j].get_xaxis().set_visible(False)
        axes[i * 2 + 0, j].get_yaxis().set_visible(False)
        axes[i * 2 + 1, j].get_yaxis().set_visible(False)


#plot_border(border_layer, axes[0, 0])
#plot_line(border_layer, axes[0, 0], prev_x, prev_y, next_x, next_y)
#bl2 = border_layer.copy()
#delete_point(bl2, 1, 1)
#plot_border(bl2,ax2)
#plot_line(bl2, ax2, prev_x, prev_y, next_x, next_y)
plt.show()


