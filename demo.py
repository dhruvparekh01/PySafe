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

    p_text = []
    for i in range(0, len(plaintext), 64):
        p_text.append(plaintext[i:i + 64])  # Separate the 64 bit blocks

    # Create a pool object passing the number of processes
    pool = multiprocessing.Pool(processes=mywin.no_of_processes)

    # Generate the 16 round key and save them here
    rkey = key_scheduler.round_key_generator(k)

    start = time.time()  # Time tracking to calculate the speed

    # Create a partial
    if mywin.flag == 1:
        cipher = partial(DES.des, key=rkey)
    else:
        cipher = partial(DES_decrypt.decrypt_DES, key=rkey)


    # Start asynchronous multiple processes for encryption/decryption as determined by the partial
    ciphertext = pool.map_async(cipher, p_text)

    pool.close()  # Close the pool object after all the processes finish

    '''Progress tracking code'''

    # Track the number of tasks left to determine the progress
    total_tasks = ciphertext._number_left

    s = '['
    for i in range(50):
        s += ' '  # Create 50 blank blocks for initial process start

    perc_old = 0
    while True:
        if ciphertext.ready():  # if all the processes are complete, stop the tracking
            break

        perc_new = int((total_tasks - ciphertext._number_left) / total_tasks * 100)

        if perc_new != perc_old:  # if there is a change in percentage completed
            s = '['
            for i in range(perc_new // 2):
                s += '|'
            for i in range(50 - perc_new // 2):
                s += ' '

            if mywin.flag == 1:
                mywin.l6.config(text='Encrypting... ' + s + ']' + str(perc_new) + '%')
            else:
                mywin.l6.config(text='Decrypting... ' + s + ']' + str(perc_new) + '%')
            window.update()

        perc_old = perc_new

    end = time.time()
    time_taken = end - start

    ''' End of progress tracking '''

    c = bitarray([])

     # Flatten the 2d array that contains 64 bit blocks into a continuous 1d array
    for i in ciphertext.get():
        c.extend(i)

    # if we did decryption, then remove the paddings
    if mywin.flag == 2:
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
