import os
from tkinter import *
from tkinter import ttk
import time
from tkinter.messagebox import *
from threading import *


def save():
    d = comDay.get()
    o = time_text.get('1.0', 'end-1c')
    t = text_d.get('0.0', 'end')
    if len(o) == 4:
        file = open(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{o}{l}'.format(d=d, o=o, l='.txt'), 'w')
        file.write(str(t))
        file.close()
        showinfo('Сохранено', 'Напоминание создано')
    else:
        showerror('Error', 'Не верный формат фремени')


def open_save():
    global time_sleep
    while True:
        tim = str(time.strftime('%H%M%S%a', time.localtime()))
        print(tim)
        H = int(tim[:2])
        M = int(tim[2:4])
        S = int(tim[4:6])
        day = tim[6:]
        files_day = os.listdir(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}'.format(d=day))
        print(files_day)
        if len(files_day) > 0:
            if tim[:4] + '.txt' in files_day:
                file_HM = open(
                    r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{o}'.format(d=day, o=tim[:4] + '.txt'), 'r')
                showinfo('Время {H}:{M}'.format(H=tim[:2], M=tim[2:4]), file_HM.read())
                file_HM.close()
                os.remove(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{o}'.format(d=day, o=tim[:4] + '.txt'))
            else:
                count = 0
                for j in files_day:
                    print(j)
                    if int(tim[:4]) < int(j[:4]):
                        Hm = H * 60 * 60
                        Mm = M * 60
                        Sm = 60 - S
                        nHm = int(j[:2]) * 60 * 60
                        nMm = int(j[2:4]) * 60
                        nSm = 0
                        time_sleep = ((nHm + nMm + nSm) - (Hm + Mm + Sm))
                        print('Новове время ' + str(time_sleep))
                        count += 1
                        continue
                    else:
                        Hm = int(tim[:2]) * 60 * 60
                        Mm = int(tim[2:4]) * 60
                        Sm = 60 - S
                        time_sleep = (86401 - (Hm + Mm + Sm))
                        print('Прежнее время ' + str(time_sleep))
                time.sleep(time_sleep)

        else:
            Hm = H * 60 * 60
            Mm = M * 60
            Sm = 60 - S
            print(Hm + Mm + Sm)
            time.sleep(86401 - (Hm + Mm + Sm))


root = Tk()

thread_day = Thread(target=open_save)
thread_day.start()

weekDays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
start = False

root.title('Day')

label_1 = Label(root, text='Введите день недели и время , без пробелов (ЧЧ ММ)')
label_1.grid(row=1, column=0)

comDay = ttk.Combobox(root, values=weekDays)
comDay.grid(row=1, column=1)
comDay.current(0)

time_text = Text(root, width=7, height=1)
time_text.grid(row=1, column=2)

text_d = Text(root, width=20, height=5)
text_d.grid(row=2, column=0, columnspan=3, stick='we')

but_save = Button(root, text='Сохранить', width=10, height=1, command=save)
but_save.grid(row=3, column=0, columnspan=3)

root.mainloop()
