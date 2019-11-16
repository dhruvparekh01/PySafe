if __name__ == '__main__':
    window = Tk()
    mywin = Gui(window)
    window.title('Encryption')
    window.geometry("300x450")

    while not Gui.exit:
        while Gui.flag == 0:
            window.update()

        plaintext = pad.bit_pad(Gui.plaintext)
        plaintext = pad.byte_pad(plaintext)

        k = hash.hash_pass(Gui.password)

        p = []
        for i in range(0, len(plaintext), 64):
            p.append(plaintext[i:i + 64])  # Separate the 64 bit blocks

        pool = multiprocessing.Pool(processes=Gui.no_of_processes)  # Create a pool object passing the number of processes based on the speed selected by the user

        rkey = key_scheduler.round_key_generator(k)  # Generate the 16 round key and save them here

        start = time.time()  # Time tracking to calculate the speed of encryption/decryption

        if Gui.flag == 1:
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

                if Gui.flag == 1:
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

        if Gui.flag == 2:  # if we did decryption, then remove the paddings
            c = pad.remove_byte_pad(c)
            c = pad.remove_bit_pad(c)

        ciphertext_list = c.tolist()  # convert the bitarray to a python list
        out_bytes = np.packbits(ciphertext_list)
        out_bytes.tofile('Processed files/' + Gui.out_name)

        size = len(plaintext)
        speed = (size / time_taken) / 1024
        mywin.l6.config(text='Process complete!!. Speed: ' + "{:5.2f}".format(speed) + ' kbps')
        Gui.exit = True

    mywin.b4 = Button(window, text='Exit', command=mywin.close_win)
    mywin.b4.place(x=50, y=410)
    window.mainloop()
