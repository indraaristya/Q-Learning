import random
from numpy import genfromtxt
import numpy as np
import pandas as pd

#Fungsi ini adalah menentukan arah yang bisa dilalui oleh suatu titik. Sehingga pada saat random, hasil random adalah
#memang arah yang bisa dilalui
def check_possible_direction(row,col):
    direction = ['N','S','W','E']
    if (row == 9):
        if (col == 0):
            direction = ['N','E']
        elif (col == 9):
            direction = ['N', 'W']
        else:
            direction = ['N','E','W']
    if (row == 0):
        if (col == 0):
            direction = ['S','E']
        elif (col == 9):
            direction = ['S','W']
        else:
            direction = ['S', 'E', 'W']
    if (col == 0) and (row != 0) and (row != 9):
        direction = ['N', 'S', 'E']
    if (col == 9) and (row != 0) and (row != 9):
        direction = ['N', 'S', 'W']
    return direction

#Fungsi ini adalah fungsi untuk menentukan nilai next_row atau titik selanjutnya
#Akan dikembalikan row masukkan jika arah tidak sesuai
def next_state_row(direction,row):
    newRow = row
    if (direction == 'N'):
        newRow = row - 1
    elif (direction == 'S'):
        newRow = row + 1
    return newRow

#Fungsi ini adalah fungsi untuk menentukan nilai next_col (next colomn) atau titik selanjutnya
#Akan dikembalikan col (column) masukkan jika arah tidak sesuai
def next_state_col(direction,col):
    newCol = col
    if (direction == 'W'):
        newCol = col - 1
    elif (direction == 'E'):
        newCol = col + 1
    return newCol

#Fungsi merubah arah menjadi state dalam tabel Q
def convert_to_state(x,y):
    x = x*10
    return x+y

#Fungsi ini merubah direction dalam bentuk huruf menjadi angka
def direction_to_state(direction):
    if (direction == 'N'):
        return 0
    elif (direction == 'S'):
        return 1
    elif (direction == 'W'):
        return 2
    elif (direction == 'E'):
        return 3

#Fungsi ini merubah direction dalam bentuk angka menjadi huruf
def index_to_direction(idx):
    direc = ''
    if (idx == 0):
        direc = 'N'
    elif (idx == 1):
        direc = 'S'
    elif (idx == 2):
        direc = 'W'
    elif (idx == 3):
        direc = 'E'
    return direc


# Matrix r bernilai 10x10 sesuai dengan data yang telah diberikan
r = genfromtxt('DataTugasML3.txt', delimiter='\t')

# Matrix q bernilai 4x100, dimana 4 adalah arah dan 100 adalah state
# Saat ingin menggunakan matrix q pada index tertentu, formatnya adalah q.iloc[baris][kolom] atau q[kolom][baris]
q = pd.DataFrame(np.zeros((4, 100)))

gamma = 0.7
alpha = 0.25
eps = 150  # jumlah episode
list_reward = []  # list untuk menyimpan list reward di setiap episode training
list_step = []  # list untuk menyimpan list step di setiap episode training

for i in range(0, eps):
    row = 9
    col = 0
    reward = 0
    step = []
    j = 0
    while (r[row, col] != 100):
        newRow = row
        newCol = col

        # variabel direct akan berisikan arah-arah yang bisa dilalui oleh suatu titik dilihat dari nilai row dan column
        direct = check_possible_direction(row, col)

        # variabel x akan berisikan hasil random dari list variabel direct
        x = random.choice(direct)

        # ditentukan titik selanjutnya berdasar arah yang terpilih dan titik lama.
        # disimpan ke dalam variabel newRow dan newCol
        newRow = next_state_row(x, row)
        newCol = next_state_col(x, col)

        # arah ditambahkan ke dalam list step
        step.append(x)

        # variable arah akan berisi nilai 0-3 sebagai index representasi dari arah x
        arah = direction_to_state(x)

        # variabel state akan merubah row dan column ke dalam bentuk state untuk tabel q.
        # variabel next_state juga akan merubah new row dan new column ke dalam bentuk state untuk tabel q.
        state = convert_to_state(row, col)
        next_state = convert_to_state(newRow, newCol)

        # nilai dari tabel q pada kolom ke-<state> akan disimpan ke variabel check_max
        check_max = [q[next_state][0], q[next_state][1], q[next_state][2], q[next_state][3]]

        # dilakukan update terhadap nilai q
        q[state][arah] = q[state][arah] + alpha * (r[newRow][newCol] + (gamma * (max(check_max) - q[state][arah])))
        reward = reward + r[newRow][newCol]

        # row dan column selanjutnya tadi akan menjadi current row dan column
        row = newRow
        col = newCol
        j += 1

    list_step.append(step)
    list_reward.append(reward)
    print("Reward Episode ",i+1," = ",reward)
print("Best Reward = ", max(list_reward))
print("Direction = ", list_step[list_reward.index(max(list_reward))])

# pengujian dari tabel Q yang didapat

# dibuat variabel road yang berukuran 10x10 bernilai 0
road = r * 0
row = 9
col = 0
reward = 0

# nilai road[9][0] diberi nilai 1 sebagai tanda telah dilewati
road[row][col] = 1
step = []

while (r[row][col] != 100):
    possible_dir = []
    # variabel state akan merubah row dan column ke dalam bentuk state untuk tabel q.
    state = convert_to_state(row, col)

    # akan disimpan nilai dari tabel q dengan column ke-<state> ke dalam variabel idx
    idx = [q[state][0], q[state][1], q[state][2], q[state][3]]

    # ditentukan index tempat nilai terbesar yang ada dalam list idx
    max_q = idx.index(max(idx))

    # mengubah index tersebut menjadi representasi arah dalam huruf
    arah = index_to_direction(max_q)
    step.append(arah)

    # ditentukan next row dan column
    newRow = next_state_row(arah, row)
    newCol = next_state_col(arah, col)

    # nilai road[next row][next column] diubah menjadi 1 sebagai tanda telah dilewati
    road[newRow][newCol] = 1

    # dihitung reward yang didapatkan dengan melewati titik tersebut
    reward = reward + r[newRow][newCol]
    row = newRow
    col = newCol
print("Reward: ", reward)
print(road)
print(step)
print(q)