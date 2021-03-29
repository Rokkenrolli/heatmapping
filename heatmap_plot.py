import re
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Button

import numpy as np
import pandas as pd
import plotly as pl
from plotly.subplots import make_subplots

DEBUG = False
color_scale = 'turbo'
fluorecence = 'fluorecence'
absorbance = 'absorbance'


class FileException(Exception):
    def __init__(self, message="invalid file format. Please select xlsx file"):
        self.message = message
        super().__init__(self.message)
        pass


def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}


"""
Requires data to be in a table on a separate clear excel excel
"""


def plot():
    print('please select excel file to open')
    file_path = select_excel_file()
    print(f'{file_path} chosen.\n Starting heatmap creation')
    shapes = {fluorecence: [4, 6, 8, 10, 12, 12, 12, 12, 10, 8, 6, 4],
              absorbance: [5, 9, 11, 13, 13, 15, 15, 15, 15, 13, 13, 11, 9, 5]}
    mins = {fluorecence: False, absorbance: 0}
    maxs = {fluorecence: False, absorbance: 4}
    shape_string, use_smoothing = select_type(shapes)
    shape = shapes[shape_string]
    data = pd.read_excel(file_path, header=None).transpose().to_numpy()
    frames = create_frames(shape, data)
    square_len = np.sqrt(len(frames))
    x = y = int(square_len) if square_len.is_integer() else int(square_len) + 1
    if DEBUG:
        print(frames)
    fig = make_subplots(cols=x, rows=y)
    for idx, frame in enumerate(frames):
        trace = pl.graph_objs.Heatmap(df_to_plotly(frame), hoverongaps=False, coloraxis="coloraxis",
                                      zsmooth='best' if use_smoothing else False)
        fig.append_trace(trace, col=(idx % x) + 1, row=(int(idx / y) + 1))
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(coloraxis={'colorscale': color_scale, 'cmin': mins[shape_string], 'cmax': maxs[shape_string]},
                      title=f'heatmap with style {color_scale}, {"with" if use_smoothing else "no"} smooothing',
                      width=1600, height=1600)
    print(f'Figures created')
    pathname = input('please enter name for html file, the file is created to this directory\n-')
    fig.write_html(f'{pathname}.html')
    print('File created')
    fig.show()


def create_frames(shape_array, input_array):
    frames = []

    for input_col in input_array:
        maximum_range = max(shape_array)
        if DEBUG:
            print(f'range is {maximum_range}, inputs: {shape_array}, {input_col}')
        rows = {}
        index = 0
        for idx, row_shape in enumerate(shape_array):
            row = []
            minimum = (maximum_range - row_shape) / 2
            maximum = (maximum_range + row_shape) / 2
            if DEBUG:
                print(f'min: {minimum}, max: {maximum}, current row shape: {row_shape}')
            for i in range(maximum_range):
                if minimum <= i < maximum:
                    row.append(input_col[index])
                    index += 1
                else:
                    row.append(None)
                rows[idx] = np.array(row)
        frames.append(pd.DataFrame.from_dict(rows).transpose())
    return frames


def callback(listbox, root, radiovar, returnvalue):
    index = listbox.curselection()[0]
    selection = listbox.get(index)
    root.quit()
    if DEBUG:
        print(selection)
    returnvalue.append(selection)
    returnvalue.append(radiovar.get())


def handle_click(cv):
    cv.set(not cv.get())
    if DEBUG:
        print(f'radiovar was selected to {cv.get()}')


def select_type(shapes):
    root = tk.Tk()
    root.geometry('400x300')
    label = tk.Label(root, text='Choose plot type')
    label.grid(row=0, column=1)
    listbox = tk.Listbox(root)
    returnvalue = []
    for idx, value in enumerate(shapes.keys()):
        listbox.insert(idx, value)
    listbox.grid(row=1, column=1)
    check_var = tk.BooleanVar()
    check_button = tk.Checkbutton(root, text="Use smoothing", variable=check_var,
                                  command=lambda cv=check_var: handle_click(cv))
    check_button.grid(row=2, column=1)
    button = Button(root, text="Confirm", command=lambda lb=listbox: callback(lb, root, check_var, returnvalue))
    button.grid(row=3, column=1)
    root.mainloop()
    return returnvalue[0], returnvalue[1]


def select_excel_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    match = re.search("\.xlsx$", file_path)
    if match:
        return file_path
    else:
        raise FileException(f'Invalid file format. {file_path} is not xlsx file')


plot()
