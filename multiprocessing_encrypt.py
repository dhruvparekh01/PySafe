from functools import partial
import DES
import functions
import numpy as np
import bitarray
import time
import multiprocessing
import key_scheduler
import pad
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
import hash
import DES_decrypt


obj = functions.Functions()


if __name__ == "__main__":
    win = Tk()
    win.geometry("300x450")

    fun = functions.Functions()

    plaintext = bitarray.bitarray([])
    flag = 0
    no_of_processes = 0
    file_selected = 0
    data_checked = False
    out_dir = ''


    def encrypt_pressed():
        global flag
        flag = 1


    def decrypt_pressed():
        global flag
        flag = 2


    def sel_dir():
        global out_dir
        out_dir = filedialog.askdirectory(parent=win, mode='rb', title='Choose a file')


    def browse():
        global plaintext
        global file_selected
        file = filedialog.askopenfile(parent=win, mode='rb', title='Choose a file')
        in_bytes = np.fromfile(file, dtype="uint8")
        in_bits = np.unpackbits(in_bytes)
        bit_list = in_bits.tolist()
        plaintext = bitarray.bitarray(bit_list)
        file_selected = 1


    l1 = Label(win, text='PySafe', font=("Times New Roman", 19, "bold"))
    l2 = Label(win, text='Choose speed')
    cb = Combobox(win, values=['Slow (Low CPU usage)', 'Medium (default)', 'Fast (High CPU usage)'], state='readonly')
    l3 = Label(win, text='Select the file to encrypt/decrypt')
    b1 = Button(win, text='Browse', command=browse)
    l4 = Label(win, text='Enter the password')
    t1 = Entry(show='*')
    l5 = Label(win, text='Name of encrypted/decrypted file')
    t2 = Entry()
    b2 = Button(win, text='Encrypt', command=encrypt_pressed)
    b3 = Button(win, text='Decrypt', command=decrypt_pressed)
    l6 = Label(win, text='', font=("Ariel", 9, "bold"))

    l1.place(x=100, y=20)
    l2.place(x=50, y=75)
    cb.place(x=50, y=100)
    l3.place(x=50, y=145)
    b1.place(x=50, y=170)
    b1.configure(borderwidth='1')
    l4.place(x=50, y=215)
    t1.place(x=50, y=240)
    l5.place(x=50, y=275)
    t2.place(x=50, y=300)
    b2.place(x=50, y=345)
    b3.place(x=150, y=345)
    l6.place(x=30, y=385)
    l6.configure(foreground='red')
    l6.config(text='')

    cb.current(1)


    def speed_sel():
        global no_of_processes
        selected = cb.get()
        if selected == 'Slow (Low CPU usage)':
            no_of_processes = 1
        elif selected == 'Medium (default)':
            no_of_processes = 3
        elif selected == 'Fast (High CPU usage)':
            no_of_processes = 6


    win.update()


    def get_data():
        while flag == 0:
            win.update()

        global password, out_name
        speed_sel()
        password = t1.get()
        out_name = t2.get()


    get_data()


    def check_data():
        global flag, data_checked, password, out_name

        while file_selected == 0:
            flag = 0
            l6.config(text='Please select the file')
            win.update()

        if password == '':
            flag = 0
            l6.config(text='Please enter the password')
            get_data()

        if out_name == '':
            flag = 0
            l6.config(text='Please the output file name')
            get_data()

        if flag != 0:
            data_checked = True


    while not data_checked:
        check_data()


    def demo():
        win.update()

    k = hash.hash_pass(password)

    plaintext = pad.bit_pad(plaintext)
    plaintext = pad.byte_pad(plaintext)

    p = []
    for i in range(0, len(plaintext), 64):
        p.append(plaintext[i:i+64])

    win.update()

    pool = multiprocessing.Pool(processes=no_of_processes)

    rkey = key_scheduler.round_key_generator(k)

    start = time.time()

    if flag == 1:
        abc = partial(DES.des, key=rkey)
    else:
        abc = partial(DES_decrypt.decrypt_DES, k=rkey)

    ciphertext = pool.map_async(abc, p)
    pool.close()

    total_tasks = ciphertext._number_left

    s = '['
    for i in range(50):
        s += ' '

    perc_old = 0
    while True:
        if ciphertext.ready():
            break
        # print(str(ciphertext._number_left))
        perc_new = int((total_tasks-ciphertext._number_left) / total_tasks * 100)
        # l6.config(text=perc)
        # win.update()
        if perc_new != perc_old:
            s = '['
            for i in range(perc_new//2):
                s += '|'
            for i in range(50-perc_new//2):
                s += ' '

        if flag == 1:
            l6.config(text='Encrypting... ' + s + ']' + str(perc_new) + '%')
        else:
            l6.config(text='Decrypting... ' + s + ']' + str(perc_new) + '%')
        win.update()

        perc_old = perc_new

    end = time.time()
    time_taken = end-start

    c = bitarray.bitarray([])

    for i in ciphertext.get():
        c.extend(i)

    # print(c)

    ciphertext_list = c.tolist()
    out_bytes = np.packbits(ciphertext_list)
    out_bytes.tofile('Processed files/'+out_name)

    size = len(plaintext)
    speed = (size/time_taken)/1024
    l6.config(text='Process complete!!. Speed: ' + "{:5.2f}".format(speed) + ' kbps')
    # l6.place(x=50, y=375)

    closed = 0

    def close_win():
        global closed
        closed = 1
        win.destroy()

    b4 = Button(win, text='Exit', command=close_win)
    b4.place(x=50, y=410)

    while closed == 0:
        win.update()

