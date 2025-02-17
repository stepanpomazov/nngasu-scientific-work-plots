import math
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        global excel_file
        excel_file = file_path
        load_data()

def remove_elements(arr):
    sign = arr[0] > 0
    prev_index = 0
    result = []
    for i in range(0, len(arr)):
        if sign == True:
            if arr[i] > 0:
                continue
            result.append(max(arr[prev_index:i]))
            prev_index = i
            sign = not sign
        else:
            if arr[i] < 0:
                continue
            result.append(min(arr[prev_index:i]))
            prev_index = i
            sign = not sign
    return result

def load_data():
    try:
        df = pd.read_excel(excel_file, usecols=[0, 1], engine='openpyxl')
        A = []
        B = []
        for row in df.itertuples():
            A.append(row[1])
            B.append(row[2])
        peaks = []
        for i in range(len(B)):
            if B[i] > B[i - 1] and B[i] > B[i + 1]:
                peaks.append(B[i])
        c = 0
        valid_peaks = remove_elements(peaks)
        valid_peaks = valid_peaks[max(enumerate(valid_peaks), key=lambda x: x[1])[0]:]
        if len(valid_peaks) <= 1:
            output_text.insert(tk.END, "Некорректные данные")
            output_text.insert(tk.END, "\n")
        print(peaks)
        print(valid_peaks)
        output_text.delete(1.0, tk.END)  # Очистить текстовое поле
        for i in range(len(valid_peaks) - 1):
            if valid_peaks[i] > abs(valid_peaks[i + 1]):
                flag = True
            else:
                flag = False
        if flag == True:
            output_text.insert(tk.END, "Проверка 1: Затухающая синусоида: ✓")
            output_text.insert(tk.END, "\n")
        else:
            c += 1
            output_text.insert(tk.END, "Проверка 1: Затухающая синусоида: incorrect")
            output_text.insert(tk.END, "\n")
        f = True
        for i in range(len(valid_peaks) - 1):
            index1 = B.index(valid_peaks[i])
            index2 = B.index(valid_peaks[i + 1])
            if index2 - index1 < 10:
                f = False
                break
        if f:
            output_text.insert(tk.END, "Проверка 2: Более 10 промежуточных значений: ✓")
            output_text.insert(tk.END, "\n")
        else:
            c += 1
            output_text.insert(tk.END, "Проверка 2: Более 10 промежуточных значений: incorrect")
            output_text.insert(tk.END, "\n")
        if len(valid_peaks) >= 20:
            output_text.insert(tk.END, "Проверка 3: Более 20 экстремумов: ✓")
            output_text.insert(tk.END, "\n")
        else:
            c += 1
            output_text.insert(tk.END, "Проверка 3: Более 20 экстремумов: incorrect")
            output_text.insert(tk.END, "\n")
        if c != 0:
            output_text.insert(tk.END, "\n")
            output_text.insert(tk.END, "Некорректные значения!")
        else:
            output_text.insert(tk.END, "\n")
            output_text.insert(tk.END, "Проверка пройдена!\n")
            output_text.insert(tk.END, "Выполняю расчёты:\n")
            cou = 0
            for i in range(len(valid_peaks)):
                if valid_peaks[i] > 0:
                    cou += 1
            cou = cou // 2
            indexmin = A[B.index(valid_peaks[0])]
            indexmax = A[B.index(valid_peaks[cou])]
            deltat = indexmax - indexmin
            chast = cou / deltat
            output_text.insert(tk.END, f"ν: {chast} Гц\n")
            om = 2 * math.pi * chast
            output_text.insert(tk.END, f"ω: {om} рад/с\n")
            T = 1 / chast
            output_text.insert(tk.END, f"τ: {T} с\n")
            m = int(entry_b.get())
            ll = int(entry_b2.get())
            J = int(entry_b3.get())
            lamb = int(entry_b4.get())
            Ed = (om ** 2 * m * ll ** 4) / (math.pi ** 4 * J)
            output_text.insert(tk.END, f"Eд: {Ed} Па\n")
            E = abs(1/(10*T) * math.log(A[B.index(valid_peaks[0])]/A[B.index(valid_peaks[9])]))
            output_text.insert(tk.END, f"ε: {E} с^-1\n")
            Y = E*T / math.pi
            output_text.insert(tk.END, f"γ: {Y}\n")
            mu = 1/math.sqrt((1-lamb**2)**2 + Y**2 * lamb**2)
            output_text.insert(tk.END, f"μ: {mu}\n")
    except Exception as e:  # отловка ошибок и вывод их в текстовое поле
        output_text.insert(tk.END, f"Ошибка: {e}")
        output_text.delete(1.0, tk.END)
    plt.plot(A, B)
    #plt.show()
    fig, ax = plt.subplots()
    ax.plot(A, B)
    plt.title("График колебаний по данным акселератора")
    if output_text.get("1.0", "end-1c") == "":  # Проверяем, пуст ли текстовый виджет
        output_text.insert(tk.END, "Ошибка. Проверьте введенные данные, график должен быть типа затухающей синусоиды!")
    # Создаем объект FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    # Размещаем график в tkinter окне
    canvas_widget.grid(row=0, column=5, rowspan=4, **opts)
def grid_configure(widget, row, column):
    widget.grid( row=row, column=column, padx=5, pady=5)
    widget.grid_configure(sticky=tk.W)
# Создаем главное окно
root = tk.Tk()
root.geometry("1020x670")
root.title("Графики")
frame1 = tk.Frame(root, width=500, height=200, background="bisque")
frame1.grid(sticky="w")
global m, ll, J
label_a = tk.Label(frame1, text="Введите массу стержня (m):")
entry_b = tk.Entry(frame1)
label_с = tk.Label(frame1, text="т", bg="orange")
label_a2 = tk.Label(frame1, text="Введите пролёт стержня (l):")
entry_b2 = tk.Entry(frame1)
label_с2 = tk.Label(frame1, text="м", bg="orange")
label_a3 = tk.Label(frame1, text="Введите момент инерции (J):")
entry_b3 = tk.Entry(frame1)
label_с3 = tk.Label(frame1, text="м^4", bg="orange")
label_a4 = tk.Label(frame1, text="Введите λ = θ/ω:")
entry_b4 = tk.Entry(frame1)
label_с4 = tk.Label(frame1, text="ед.", bg="orange")
opts = {'ipadx': 10, 'ipady': 10, 'sticky': 'nswe'}
label_a.grid(row=0, column=0, **opts)
entry_b.grid(row=0, column=1, **opts)
label_с.grid(row=0, column=2, **opts)
label_a2.grid(row=1, column=0, **opts)
entry_b2.grid(row=1, column=1, **opts)
label_с2.grid(row=1, column=2, **opts)
label_a3.grid(row=2, column=0, **opts)
entry_b3.grid(row=2, column=1, **opts)
label_с3.grid(row=2, column=2, **opts)
label_a4.grid(row=3, column=0, **opts)
entry_b4.grid(row=3, column=1, **opts)
label_с4.grid(row=3, column=2, **opts)
button = tk.Button(frame1, text="Ок", command=lambda: load_file())
button.grid(row=4,column=0,columnspan=3,**opts)
output_text = tk.Text(frame1, wrap='word',height=30, width=30)
output_text.grid(row=5,column=0,columnspan=3,**opts)
# Запускаем главный цикл
root.mainloop()
