from tkinter import *
import DES
import DES_decrypt
import tripleDES
import tripleDES_decrypt

flag = 0


class MyWindow:
    def __init__(self, win):

        self.lb100 = Label(win, text='ENCRYPTION', font=("Times New Roman", 19, "bold"))  #Set heading

        '''Set of labels'''

        self.lbl1 = Label(win, text='Enter plaintext/ciphertext')
        self.lbl2 = Label(win, text='Ciphertext/plaintext')
        self.lbl3 = Label(win, text='Enter key')

        '''Set of text boxes'''

        self.t1 = Entry()
        self.t2 = Entry()
        self.t3 = Entry()

        self.mbtn1 = Button(win, text='DES', command=self.des)  #button to perform DES
        self.mbtn2 = Button(win, text='3-DES', command=self.trides)  #button to perform 3DES

        '''Setting the coordinates of each component'''

        self.mbtn1.place(x=110, y=70)
        self.mbtn2.place(x=200, y=70)

        self.lb100.place(x=100, y=20)

        self.lbl1.place(x=50, y=130)
        self.lbl3.place(x=50, y=160)
        self.t1.place(x=200, y=130)
        self.t2.place(x=200, y=160)

        self.b1=Button(win, text='Encrypt', command=self.encrypt)  #Encrypt button
        self.b2=Button(win, text='Decrypt', command=self.decrypt)  #Decrypt button

        self.b2.bind('Decrypt', self.decrypt)
        self.b1.place(x=100, y=205)
        self.b2.place(x=200, y=205)

        #self.b3 = Button(win, text='Encrypt')
        #self.b3.place(x=150, y=220)
        self.lbl2.place(x=50, y=260)
        self.t3.place(x=175, y=260)


    def des(self):
        global flag
        flag = 1
        self.mbtn1['state'] = 'disabled'
        self.mbtn2['state'] = 'disabled'

    def trides(self):
        global flag
        flag = 2
        self.mbtn1['state'] = 'disabled'
        self.mbtn2['state'] = 'disabled'

    def encrypt(self):
        global flag
        self.t3.delete(0, END)
        plaintext = str(self.t1.get())
        key = str(self.t2.get())
        if flag == 1:
            ciphertext = DES.DES(plaintext, key)
        elif flag == 2:
            ciphertext = tripleDES.triple_des(plaintext, key)
        else:
            ciphertext = 'Please select the method first'
        self.t3.insert(END, str(ciphertext))


    def decrypt(self):
        global flag
        self.t3.delete(0, END)
        plaintext = str(self.t1.get())
        key = str(self.t2.get())
        if flag == 1:
            ciphertext = DES_decrypt.decrypt_DES(plaintext, key)
        elif flag == 2:
            ciphertext = tripleDES_decrypt.triple_des_decr(plaintext, key)
        else:
            ciphertext = 'Please select the method first'
        self.t3.insert(END, str(ciphertext))


window = Tk()
mywin = MyWindow(window)
window.title('Encryption')
window.geometry("400x300+10+10")
window.mainloop()

