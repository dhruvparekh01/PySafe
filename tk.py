from functools import partial
import DES
import numpy as np
from bitarray import bitarray
import time
import multiprocessing
import key_scheduler
import pad
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
import hash
import DES_decrypt


class Gui:
    def __init__(self, win):
        self.exit = False
        self.flag = 0
        self.no_of_processes = 2
        self.plaintext = bitarray()
        self.key = bitarray()
        self.out_dir = './'
        self.file_selected = 0
        self.out_name = 'default'
        self.password = 'admin'

        self.window = win

        self.l1 = Label(win, text='PySafe', font=("Times New Roman", 19, "bold"))
        self.l2 = Label(win, text='Choose speed')
        self.cb = Combobox(win, values=['Slow (Low CPU usage)', 'Medium (default)', 'Fast (High CPU usage)'], state='readonly')
        self.l3 = Label(win, text='Select the file to encrypt/decrypt')
        self.b1 = Button(win, text='Browse', command=self.browse)
        self.l4 = Label(win, text='Enter the password')
        self.t1 = Entry(show='*')
        self.l5 = Label(win, text='Name of encrypted/decrypted file')
        self.t2 = Entry()
        self.b2 = Button(win, text='Encrypt', command=self.encrypt_pressed)
        self.b3 = Button(win, text='Decrypt', command=self.decrypt_pressed)
        self.l6 = Label(win, text='', font=("Ariel", 9, "bold"))

        self.l1.place(x=100, y=20)
        self.l2.place(x=50, y=75)
        self.cb.place(x=50, y=100)
        self.l3.place(x=50, y=145)
        self.b1.place(x=50, y=170)
        self.b1.configure(borderwidth='1')
        self.l4.place(x=50, y=215)
        self.t1.place(x=50, y=240)
        self.l5.place(x=50, y=275)
        self.t2.place(x=50, y=300)
        self.b2.place(x=50, y=345)
        self.b3.place(x=150, y=345)
        self.l6.place(x=30, y=385)
        self.l6.configure(foreground='red')
        self.l6.config(text='')

        # self.b4 = Button(win, text='Exit', command=self.close_win)
        # self.b4.place(x=50, y=410)
        self.b4 = ''

    def encrypt_pressed(self):
        self.flag = 1
        self.get_data()
        # self.window.destroy()

    def decrypt_pressed(self):
        self.flag = 2
        self.get_data()
        # self.window.destroy()

    def sel_dir(self):
        self.out_dir = filedialog.askdirectory(parent=self.window, mode='rb', title='Choose a file')

    def browse(self):
        file = filedialog.askopenfile(parent=self.window, mode='rb', title='Choose a file')
        in_bytes = np.fromfile(file, dtype="uint8")
        in_bits = np.unpackbits(in_bytes)
        bit_list = in_bits.tolist()
        self.plaintext = bitarray(bit_list)
        self.file_selected = 1

    def speed_sel(self):
        selected = self.cb.get()
        if selected == 'Slow (Low CPU usage)':
            self.no_of_processes = 1
        elif selected == 'Medium (default)':
            self.no_of_processes = 2
        elif selected == 'Fast (High CPU usage)':
            self.no_of_processes = 3

    def get_data(self):
        self.speed_sel()
        self.password = self.t1.get()
        self.out_name = self.t2.get()

    def close_win(self):
        self.window.destroy()


if __name__ == '__main__':
    window = Tk()
    mywin = Gui(window)
    window.title('Encryption')
    window.geometry("300x450")

    while mywin.flag == 0:
        window.update()

    plaintext = pad.bit_pad(mywin.plaintext)
    plaintext = pad.byte_pad(plaintext)

    k = hash.hash_pass(mywin.password)

    p = []
    for i in range(0, len(plaintext), 64):
        p.append(plaintext[i:i + 64])  # Separate the 64 bit blocks

    pool = multiprocessing.Pool(processes=mywin.no_of_processes)  # Create a pool object passing the number of processes based on the speed selected by the user

    rkey = key_scheduler.round_key_generator(k)  # Generate the 16 round key and save them here

    start = time.time()  # Time tracking to calculate the speed of encryption/decryption

    if mywin.flag == 1:
        abc = partial(DES.des, key=rkey)  # Create a partial
    else:
        abc = partial(DES_decrypt.decrypt_DES, key=rkey)

    ciphertext = pool.map_async(abc, p)  # Start asynchronous multiple processes for encryption/decryption as determined by the partial

    pool.close()  # Close the pool object after all the processes finish

    total_tasks = ciphertext._number_left  # Track the number of tasks left to determine the progress

    '''Progress tracking code'''
    s = '['
    for i in range(50):
        s += ' '  # Create 50 blank blocks for initial process start

    perc_old = 0
    while True:
        if ciphertext.ready():  # if all the processes are complete, stop the tracking
            break

        perc_new = int((total_tasks - ciphertext._number_left) / total_tasks * 100)  # Determine the percentage of the encryption/decryption finished

        if perc_new != perc_old:  # if there is a change in percentage completed
            s = '['
            for i in range(perc_new // 2):  # Add the percentage of process complete/2 '|'s (divided by 2 because the maximum number of '|'s that can be added is 50 not 100)
                s += '|'
            for i in range(50 - perc_new // 2):  # Fill the rest of the blocks with spaces
                s += ' '

            if mywin.flag == 1:
                mywin.l6.config(text='Encrypting... ' + s + ']' + str(perc_new) + '%')
            else:
                mywin.l6.config(text='Decrypting... ' + s + ']' + str(perc_new) + '%')
            window.update()

        perc_old = perc_new

    end = time.time()
    time_taken = end - start

    c = bitarray([])

    for i in ciphertext.get():  # Flatten the 2d array that contains 64 bit blocks into a continuous 1d array
        c.extend(i)

    if mywin.flag == 2:  # if we did decryption, then remove the paddings
        c = pad.remove_byte_pad(c)
        c = pad.remove_bit_pad(c)

    ciphertext_list = c.tolist()  # convert the bitarray to a python list
    out_bytes = np.packbits(ciphertext_list)
    out_bytes.tofile('Processed files/' + mywin.out_name)

    size = len(plaintext)
    speed = (size / time_taken) / 1024
    mywin.l6.config(text='Process complete!!. Speed: ' + "{:5.2f}".format(speed) + ' kbps')

    mywin.b4 = Button(window, text='Exit', command=mywin.close_win)
    mywin.b4.place(x=50, y=410)
    window.mainloop()

