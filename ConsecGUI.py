from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import os
import Materials as Mtr

class main:
    def __init__(self, master):
        # Свойства материалов
        self.concrete, self.steel = Mtr.materials()
        self.master = master
        self.master.title('Consec')
        self.master.geometry('350x150+200+150')
        self.label1 = ttk.Label(self.master)
        self.label1.config(text="Выбери режим!")
        self.label1.pack()
        self.label2 = ttk.Label(self.master)
        self.label2.config(text="Выбери файл!")
        self.label2.pack()
        self.main_menu = Menu()
        self.file_menu = Menu()
        self.file_menu.add_command(label="Открыть", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=root.destroy)
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.mode_menu = Menu()
        self.main_menu.add_cascade(label="Режим", menu=self.mode_menu)
        self.mode_menu.add_command(label="Сечение", command=self.mode_switch1)
        self.mode_menu.add_command(label="Плита", command=self.mode_switch2)
        self.help_menu = Menu()
        self.main_menu.add_cascade(label="Помощь", menu=self.help_menu)
        self.help_menu.add_command(label="Помощь", command=self.help)
        self.help_menu.add_command(label="О программе", command=self.about)
        self.run_image = PhotoImage(file="./run.png")
        self.btn1 = ttk.Button(self.master, text="Расчёт", image=self.run_image, compound=LEFT, command=self.run)
        self.btn1.pack()
        root.config(menu=self.main_menu)
        self.master.mainloop()

    def about(self):
        messagebox.showinfo("О программе", "Г. Березин 2024")

    def help(self):
        os.popen("Consec.chm")

    def mode_switch1(self):
        self.label1.config(text="Сечение")
        self.label2.config(text="Выбери файл!")

    def mode_switch2(self):
        self.label1.config(text="Плита")
        self.label2.config(text="Выбери файл!")

    def open_file(self):
        if self.label1.cget("text") == "Сечение":
            f = "f"
        else:
            f = "s"
        self.filepath = filedialog.askopenfilename(initialdir="*/", title="Выбери файл", filetypes=(("Excel файлы", f + "*.xlsx"), ("все файлы", "*.*")))
        self.label2.config(text=self.filepath)

    def data(self):
        section = pd.read_excel(self.filepath, sheet_name="section")
        print("Сечение:")
        print(section)
        rebars = pd.read_excel(self.filepath, sheet_name="rebars")
        print("Арматура:")
        print(rebars)
        loads = pd.read_excel(self.filepath, sheet_name="loads")
        print("Нагрузки:")
        print(loads)
        combo = pd.read_excel(self.filepath, sheet_name="combo")
        print("Комбинация:")
        print(combo)
        return section, rebars, loads, combo

    def run(self):
        try:
            # Свойства сечения
            section, rebars, loads, combo = self.data()
            if self.label1.cget("text") == "Сечение":
                from MemberSection.RConSect import FrameSec
                # Создание нового прямоугольного жб сечения
                rect = FrameSec(self.concrete, self.steel)
                # Создание прямоугольного бетонного сечения
                rect.add_rect_section(section["grade"][0], section["h"][0], section["b"][0], section["nh"][0], section["nb"][0])
                # Создание стержней
                for i in range(0, len(rebars)):
                    rect.add_rebar(rebars["name"][i], rebars["grade"][i], rebars["ds"][i], rebars["X"][i], rebars["Y"][i])
                # Добавить нагрузки
                for i in range(0, len(loads)):
                    rect.add_load(loads["N"][i], loads["Mx"][i], loads["My"][i], case=loads["case"][i])
                # Создание комбинаций
                combos = {}
                for i in range(0, len(combo)):
                    combos[combo["case"][i]] = combo["gf"][i]
                rect.add_load_combo("0", factors=combos)
                rect.analyze("0", section["kt"][0], section["gb3"][0], section["accuracy"][0])
            else:
                from ShellElement.RConShell import ShellElem
                # Создание нового выделенного жб элемента оболочки
                shell = ShellElem(self.concrete, self.steel)
                # Создание выделенного бетонного элемента оболочки
                shell.add_conc_element(section["grade"][0], section["h"][0], section["nh"][0])
                # Создание арматурных слоев
                for i in range(0, len(rebars)):
                    shell.add_ply(rebars["name"][i], rebars["grade"][i], rebars["ds"][i], rebars["ns"][i], rebars["z"][i], rebars["a"][i])
                # Добавить нагрузки
                for i in range(0, len(loads)):
                    shell.add_load(loads["Nxx"][i], loads["Nyy"][i], loads["Nxy"][i], loads["Mxx"][i], loads["Myy"][i], loads["Mxy"][i], case=loads["case"][i])
                # Создание комбинаций
                combos = {}
                for i in range(0, len(combo)):
                    combos[combo["case"][i]] = combo["gf"][i]
                shell.add_load_combo("0", factors=combos)
                shell.analyze("0", section["kt"][0], section["gb3"][0], section["v"][0], section["accuracy"][0])
        except:
            print("Неверные данные !")


# создание окна
root = Tk()

# запуск окна
main(root)
