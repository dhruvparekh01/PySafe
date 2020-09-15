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
import threading


class Gui(threading.Thread):
    """
    Define the GUI window to be displayed to the user. Runs on its own separate thread (consider this as the UI thread).
    All the calculations are done in the main thread as is the requirement of the multiprocessing library
    """
    def __init__(self):
        # Call the super class constructor
        threading.Thread.__init__(self)

        # Exit flag: terminate the GUI when set to true
        self.exit = False

        # Encrypt/decrypt flag- 1: encrypt, 2: decrypt
        self.flag = 0

        # Number of parallel processes to be spawned. Set default to 2, changed when user selects in GUI
        self.no_of_processes = 2

        # Plaintext input. Initialize to empty bit array
        self.plaintext = bitarray()

        # Cipher key.  Initialize to empty bit array
        self.key = bitarray()

        # Name of the output file. Initialize to "default"
        self.out_name = 'default'

        # Password entered by user. Initialize to "admin"
        self.password = 'admin'

        # Declare TKinter window instance variable. Initialized later in run method
        self.win = None

        # Declare the labels, text boxes, combo box and buttons for the GUI. Initialized later in run method
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.l4 = None
        self.l5 = None
        self.l6 = None

        self.t1 = None
        self.t2 = None

        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.b4 = None

        self.cb = None

        self.start()

    def exit_callback(self):
        """
        When exit button is pressed, close the GUI window.
        """
        self.win.quit()

    def run(self):
        # Create a Tkinter window and specify title, size and exit callback
        self.win = Tk()
        self.win.title('PySafe')
        self.win.geometry("300x450")
        self.win.protocol("WM_DELETE_WINDOW", self.exit_callback)

        # Set all the UI elements and the callback methods
        self.l1 = Label(self.win, text='PySafe', font=("Times New Roman", 19, "bold"))
        self.l2 = Label(self.win, text='Choose speed')
        self.cb = Combobox(self.win, values=['Slow (Low CPU usage)', 'Medium (default)', 'Fast (High CPU usage)'],
                           state='readonly')
        self.l3 = Label(self.win, text='Select the file to encrypt/decrypt')
        self.b1 = Button(self.win, text='Browse', command=self.browse)
        self.l4 = Label(self.win, text='Enter the password')
        self.t1 = Entry(show='*')
        self.l5 = Label(self.win, text='Name of encrypted/decrypted file')
        self.t2 = Entry()
        self.b2 = Button(self.win, text='Encrypt', command=self.encrypt_pressed)
        self.b3 = Button(self.win, text='Decrypt', command=self.decrypt_pressed)
        self.l6 = Label(self.win, text='', font=("Ariel", 9, "bold"))

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

        # Button for exit to be initialized after the process is over
        self.b4 = Button(self.win, text='Exit', command=self.exit_callback)
        self.b4.place(x=50, y=410)
        self.b4.destroy()
        # self.b4.grid_forget()

        self.win.mainloop()

    def encrypt_pressed(self):
        self.get_data()
        self.flag = 1

    def decrypt_pressed(self):
        self.get_data()
        self.flag = 2

    def browse(self):
        file = filedialog.askopenfile(parent=self.win, mode='rb', title='Choose a file')
        in_bytes = np.fromfile(file, dtype="uint8")
        in_bits = np.unpackbits(in_bytes)
        bit_list = in_bits.tolist()
        self.plaintext = bitarray(bit_list)

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
        self.win.destroy()


if __name__ == '__main__':
    gui_window = Gui()

    while gui_window.flag == 0:
        # Keep checking the UI thread every second to see if the user has pressed the "Encrypt" ir "Decrypt" button
        time.sleep(1)

    # Indicate in the UI that processing has started
    gui_window.l6.config(text='Encrypting... [' + ' ' * 50 + '] 0%')

    plaintext = pad.bit_pad(gui_window.plaintext)
    plaintext = pad.byte_pad(plaintext)

    k = hash.hash_pass(gui_window.password)

    p = []
    for i in range(0, len(plaintext), 64):
        p.append(plaintext[i:i + 64])  # Separate the 64 bit blocks

    # Create a pool object passing the number of processes based on the speed selected by the user
    pool = multiprocessing.Pool(processes=gui_window.no_of_processes)

    # Generate the 16 round key and save them
    round_keys = key_scheduler.round_key_generator(k)

    # Time tracking to calculate the speed of encryption/decryption
    start = time.time()

    if gui_window.flag == 1:
        des_partial = partial(DES.des, key=round_keys)  # Create a partial
    else:
        des_partial = partial(DES_decrypt.decrypt_DES, key=round_keys)

    # Start asynchronous multiple processes for encryption/decryption as determined by the partial
    ciphertext = pool.map_async(des_partial, p)

    pool.close()  # Close the pool object after all the processes finish

    # Track the number of tasks left to determine the progress. Accessing a private instance variable of the map_async
    # but making sure that we dont modify it
    total_tasks = ciphertext._number_left

    # Progress tracking code
    s = '['
    for i in range(50):
        s += ' '  # Create 50 blank blocks for initial process start

    perc_old = 0
    while True:
        if ciphertext.ready():  # if all the processes are complete, stop the tracking
            break

        # Determine the percentage of the encryption/decryption finished
        perc_new = int((total_tasks - ciphertext._number_left) / total_tasks * 100)

        if perc_new != perc_old:  # if there is a change in percentage completed
            s = '['
            # Add the percentage of process complete/2 '|'s (divided by 2 because the maximum number of '|'s that can
            # be added is 50 not 100)
            for i in range(perc_new // 2):
                s += '|'
            # Fill the rest of the blocks with spaces
            for i in range(50 - perc_new // 2):
                s += ' '

            if gui_window.flag == 1:
                gui_window.l6.config(text='Encrypting... ' + s + ']' + str(perc_new) + '%')
            else:
                gui_window.l6.config(text='Decrypting... ' + s + ']' + str(perc_new) + '%')

        perc_old = perc_new
        time.sleep(1)

    end = time.time()
    time_taken = end - start

    c = bitarray([])

    # Flatten the 2d array that contains 64 bit blocks into a continuous 1d array
    for i in ciphertext.get():
        c.extend(i)

    # if we did decryption, then remove the padding
    if gui_window.flag == 2:
        c = pad.remove_byte_pad(c)
        c = pad.remove_bit_pad(c)

    # convert the bitarray to a python list
    ciphertext_list = c.tolist()
    out_bytes = np.packbits(ciphertext_list)
    out_bytes.tofile('Processed files/' + gui_window.out_name)

    size = len(plaintext)
    speed = (size / time_taken) / 1024
    gui_window.l6.config(text='Process complete!!. Speed: ' + "{:5.2f}".format(speed) + ' kbps')

    gui_window.b4 = Button(gui_window.win, text='Exit', command=gui_window.exit_callback)
    gui_window.b4.place(x=50, y=410)
