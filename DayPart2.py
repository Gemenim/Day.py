import os
from tkinter import *
from tkinter import ttk
import time as t
from tkinter.messagebox import *
from threading import *


class Day:

    root = Tk()
    root.title('Ежедненвик')
    root.geometry('680x160')
    root.resizable(width=False, height=False)

    weekDays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    EW = BooleanVar()
    EW.set(False)
    ED = BooleanVar()
    ED.set(False)

    def get_time_nuw(self):
        self.time_now = t.strftime('%H%M%S%a', t.localtime())
        self.H = int(self.time_now[:2])
        self.M = int(self.time_now[2:4])
        self.S = int(self.time_now[4:6])
        self.weekday = self.time_now[6:]
        return self.time_now, self.H, self.M, self.S, self.weekday

    def open_file(self, day, time):
        file_HM = open(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{o}'.format(d = day, o = time), 'r')
        showinfo('Время {H}:{M}'.format(H=time[:2], M=time[2:4]), file_HM.read())
        file_HM.close()
        if time[4:6] != 'ew' or time[4:6] != 'ed':
            os.remove(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{o}'.format(d = day, o = time))

    def time_calculet(self):
        self.Hm = self.H * 60 * 60
        self.Mm = self.M * 60
        self.Sm = 60 - self.S
        return self.Hm, self.Mm, self.Sm

    def time_d_calculet(self, namefile):
        self.nHm = int(namefile[:2]) * 60 * 60
        self.nMm = int(namefile[2:4]) * 60
        return  self.nHm, self.nMm

    def calculet_sleep(self):
        self.time_sleep = (86401 - (self.Hm + self.Mm + self.Sm))
        return self.time_sleep

    def time_sleep_calculet(self, files_day, time_now):
        for i in files_day:
            if int(time_now[:4]) < int(i[:4]):
                self.time_calculet()
                self.time_d_calculet(i)
                self.time_sleep = ((self.nHm + self.nMm) - (self.Hm + self.Mm + self.Sm))
                break
            else:
                self.time_calculet()
                self.calculet_sleep()
        return self.time_sleep

    def sleep_next(self):
        t.sleep(self.time_sleep)

    def day_cycle(self):
        while True:
            self.get_time_nuw()
            files_day = os.listdir(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}'.format(d=self.weekday))
            if len(files_day) > 0:
                if self.time_now[:4] + '.txt' in files_day:
                    self.open_file(self.weekday, self.time_now[:4] + '.txt')
                elif self.time_now[:4] + 'ed.txt' in files_day:
                    self.open_file(self.weekday, self.time_now[:4] + 'ed.txt')
                    t.sleep(60)
                else:
                    self.time_sleep_calculet(files_day, self.time_now)
                    t.sleep(self.time_sleep)
            else:
                self.time_calculet()
                self.calculet_sleep()
                self.sleep_next()

    def open_for_save(self, day, time, text, idDW=''):
        file = open(
            r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{o}{ed}{l}'.format(d=day, o=time, ed=idDW, l='.txt'),
            'w')
        file.write(str(text))
        file.close()

    def save(self):
        day = self.comDay.get()
        time = self.time_text.get('1.0', 'end-1c')
        text = self.text_d.get('1.0', 'end-1c')
        if len(time) == 4:
            try:
                time_int = int(time)
                if self.EW.get():
                    self.open_for_save(day, time, text, 'ew')
                    showinfo('Сохранено', 'Запись создана')
                    self.start_cycle()
                    self.call_scroll_bar('<<ListboxSelect>>')
                elif self.ED.get():
                    for i in self.weekDays[:7]:
                        self.open_for_save(i, time, text, 'ed')
                    showinfo('Сохранено', 'Запись создана')
                    self.start_cycle()
                    self.call_scroll_bar('<<ListboxSelect>>')
                else:
                    self.open_for_save(day, time, text)
                    showinfo('Сохранено', 'Запись создана')
                    self.start_cycle()
                    self.call_scroll_bar('<<ListboxSelect>>')
            except:
                showerror('Error', 'Не верный формат времени')
        else:
            showerror('Error', 'Не верный формат времени')

    def listbox_call(self, event):
        selected_imdices = self.listbox.curselection()
        selected_time = ','.join([self.listbox.get(i) for i in selected_imdices])
        if len(selected_time) > 5:
            if selected_time[9] == 'н':
                file = open(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{t}ew.txt'.format(d='Mon',
                                                                                                  t=str(selected_time[
                                                                                                        :2] + selected_time[
                                                                                                              3:5])))
                self.check_ED.deselect()
                self.check_EW.select()
            elif selected_time[9] == 'д':
                file = open(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{t}ed.txt'.format(d=self.comDay.get(),
                                                                                                  t=str(selected_time[
                                                                                                        :2] + selected_time[
                                                                                                              3:5])))
                self.check_EW.deselect()
                self.check_ED.select()
        else:
            file = open(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{t}.txt'.format(d=self.comDay.get(), t=str(selected_time[:2] + selected_time[3:5])))
            self.check_EW.deselect()
            self.check_ED.deselect()
        self.text_d.delete(1.0, END)
        self.text_d.insert(1.0, file.read())
        file.close()
        self.time_text.delete(1.0, END)
        self.time_text.insert(1.0, selected_time[:2] + selected_time[3:5])

    def creat_scroll(self):
        self.scrollday = self.comDay.get()
        file_scroll = []
        for i in os.listdir(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}'.format(d=self.scrollday)):
            if i[4:6] == 'ew':
                file_scroll.append(f'{i[:2]}:{i[2:4]} Еженедельно')
            elif i[4:6] == 'ed':
                file_scroll.append(f'{i[:2]}:{i[2:4]} Ежедневно')
            else:
                file_scroll.append(f'{i[:2]}:{i[2:4]}')
        file_scroll_var = StringVar(value=file_scroll)
        self.listbox = Listbox(self.frame_2, height=7, listvariable=file_scroll_var)
        self.listbox.grid(row=0, column=1)
        self.listbox.bind('<<ListboxSelect>>', self.listbox_call)

        self.scrollbar = ttk.Scrollbar(self.frame_2, orient='vertical', command=self.listbox)
        self.scrollbar.grid(row=0, column=2, stick='NS')

    def call_scroll_bar(self, event):
        [child.destroy() for child in self.frame_2.winfo_children()]
        self.creat_frame_2()

    def deselect_ED(self):
        self.check_ED.deselect()

    def deselect_EW(self):
        self.check_EW.deselect()

    def start_cycle(self):
        thread_day = Thread(target=self.day_cycle)
        thread_day.start()

    def dell_save(self):
        selected_imdices = self.listbox.curselection()
        selected_time = ','.join([self.listbox.get(i) for i in selected_imdices])
        if len(selected_time) > 5:
            if selected_time[9] == 'н':
                os.remove(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{t}ew.txt'.format(d=self.comDay.get(),
                                                                                                  t=str(selected_time[
                                                                                                        :2] + selected_time[
                                                                                                              3:5])))
                self.check_ED.deselect()
                self.check_EW.deselect()
            elif selected_time[9] == 'д':
                os.remove(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{t}ed.txt'.format(d=self.comDay.get(),
                                                                                                  t=str(selected_time[
                                                                                                        :2] + selected_time[
                                                                                                              3:5])))
                self.check_EW.deselect()
                self.check_ED.deselect()
        else:
            os.remove(r'C:\Users\gemen\OneDrive\Рабочий стол\Ежедненвик\{d}\{t}.txt'.format(d=self.comDay.get(),t=str(selected_time[:2] + selected_time[3:5])))
            self.check_EW.deselect()
            self.check_ED.deselect()
        [child.destroy() for child in self.frame_2.winfo_children()]
        self.creat_frame_2()

    def creat_frame_2(self):

        self.creat_scroll()

        self.but_del = Button(self.frame_2, text='Удалить', command=self.dell_save)
        self.but_del.grid(row=2, column=1)

    def creat_widgets(self):
        self.frame_1 = Frame(self.root)
        self.frame_1.grid(row=1, column=1)

        self.label_1 = Label(self.frame_1, text='Введите день недели и время , без пробелов (ЧЧ ММ)')
        self.label_1.grid(row=0, column=0)

        self.comDay = ttk.Combobox(self.frame_1, values=self.weekDays)
        self.comDay.grid(row=0, column=1)
        self.comDay.current(0)
        self.comDay.bind('<<ComboboxSelected>>', self.call_scroll_bar)

        self.time_text = Text(self.frame_1, width=7, height=1)
        self.time_text.grid(row=0, column=2)

        self.text_d = Text(self.frame_1, width=20, height=5)
        self.text_d.grid(row=1, column=0, columnspan=3, stick='we')

        self.but_save = Button(self.frame_1, text='Сохранить', width=10, height=1, command=self.save)
        self.but_save.grid(row=2, column=0, sticky=EW)

        self.check_EW = Checkbutton(self.frame_1, text='Еженедельно', variable=self.EW, offvalue=False, onvalue=True, command=self.deselect_ED)
        self.check_EW.grid(row=2, column=1, sticky=EW)

        self.check_ED = Checkbutton(self.frame_1, text='Ежедневно', variable=self.ED, offvalue=False, onvalue=True, command=self.deselect_EW)
        self.check_ED.grid(row=2, column=2, sticky=EW)

        self.frame_2 = LabelFrame(self.root, text='Запланировано')
        self.frame_2.grid(row=1, column=2)

        self.creat_frame_2()

    def start(self):
        self.start_cycle()
        self.creat_widgets()
        Day.root.mainloop()

day = Day()
day.start()