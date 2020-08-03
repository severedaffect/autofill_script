import pandas as pd
import tkinter as tk


input_fields = ["linkU01DSC", "linkU18DSC"]
route_fields = ["linkU01RA","linkU18RA"]
frequency_field = ["linkU01FR", "linkU18RA"]

# input_string = 'linkU{}DSC'
# route_string = 'linkU{}RA'
# frequency_string = 'linkU{}FR'

row_num = 18

input_fields = []
route_fields = []
frequency_field = []

class AutoFillGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # -------------- Core Variables ---------------------
        # --------------- Resoluation
        self.res_ten_eighty = [1920, 1080]
        self.res_ten_eighty_half = [960, 540]
        self.res_current = self.res_ten_eighty_half.copy()
        self.geometry("{}x{}+0+0".format(self.res_current[0], self.res_current[1]))

        # ------------- Colors
        self.green = "#00ff00"
        self.pastel_green = '#bbfaac'
        self.dark_pastel_green = '#84b079'
        self.lime_green = '#84ff82'
        self.dark_lime = '#60ba5f'
        self.yellow = "#ffff66"
        self.red = "#ff0000"
        self.mulled_blue = "#4d4dff"
        self.dark_blue = "#004080"
        self.light_lavender = '#e3c5fa'
        self.lavender = '#c278fa'
        self.dark_lavender = '#7b4c9e'

        # -------------- In app uses -----------------------
        self.hex_str = ''
        # -------------- core objects -----------------------
        self.background = tk.Canvas(self)
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.background.create_rectangle(0, 0, self.res_current[0], self.res_current[1], fill=self.dark_pastel_green)
        self.background.create_line(0, 0, 1000, 1000)

        self.hex_input = tk.Entry(self)
        self.hex_input.place(relx=0.25, rely=0.4, relwidth=.3, relheight=0.1)
        #self.hex_input.place(relx=0.25, rely=0.4, relwidth=.5, relheight=0.2)

        self.search_button = tk.Button(self, text='Generate JS Autofill',  command= lambda: self.pull_data())
        self.search_button.place(relx=0.35, rely=0.6, relwidth=0.25, relheight=0.2)

        self.backend = AutoFillPopulator()

    def pull_data(self):
        self.hex_str = self.hex_input.get()
        print(self.hex_str)
        self.backend.intake_hex(self.hex_str)
        self.backend.pull_medications()

        self.export_data()

        self.confirm_outcome()

    def export_data(self):
        self.backend.generate_js()
        self.backend.compile_text_file()
        self.backend.export_js()

    def confirm_outcome(self):
        self.top_layer = tk.Toplevel(self, width=self.res_current[0], height=self.res_current[1])
        self.top_layer.title('Summary of Output')

        #self.summary_message = tk.Text(self.top_layer, text=self.backend.js_txt)
        self.summary_message = tk.Label(self.top_layer, text=self.backend.js_txt, justify=tk.LEFT)
        self.summary_message.place(relx=0, rely=0)

        self.sum_dismiss = tk.Button(self.top_layer, text='OK', command=self.top_layer.destroy)
        self.sum_dismiss.place(relx=0.4, rely=0.8)

class AutoFillPopulator():
    def __init__(self):
        self.excel_name = 'emarfatad.xls'
        self.col_names = ['Medication', 'Route', 'Frequency']
        self.js_name = 'auto_fill.txt'
        self.id_tags = ["'linkU{}DSC'", "'linkU{}RA'", "'linkU{}FR'"]
        self.core_function = "document.getElementById({0}).value = {1};"

        self.hex_num = ''
        self.list = None
        self.js_string_list = []
        self.js_txt = ''

    def intake_hex(self, _hex):
        #self.hex_num = input('What is the number you would like to query?')
        self.hex_num = _hex
        print('Hex acquired: ', self.hex_num)

    def pull_medications(self):
        excel_workbook = pd.read_excel(self.excel_name, index_col=0, header=None, names=self.col_names)
        print(excel_workbook)
        self.list = excel_workbook.loc[self.hex_num]
        print('List compiled: ', self.list)

    def generate_js(self):

        js_code_m = "document.getElementById('linkU{}DSC').value = {};"
        js_code_r = "document.getElementById('linkU{}RA').value = {};"
        js_code_f = "document.getElementById('linkU{}FR').value = {};"

        _meds = self.list[self.col_names[0]].tolist()
        _routes = self.list[self.col_names[1]].tolist()
        _freqs = self.list[self.col_names[2]].tolist()

        # _num_of = len(_meds)
        line_list = []

        # For each med, create the js for it, the route and the freq
        for _num, _m in enumerate(_meds):
            if _num + 1 < 10:
                _num_str = '0' + str(_num + 1)
            else:
                _num_str = str(_num + 1)

            temp_m = js_code_m.format(_num_str, _m)
            temp_r = js_code_r.format(_num_str, int(_routes[_num]))
            temp_f = js_code_f.format(_num_str, _freqs[_num])

            line_list.append([temp_m, temp_r, temp_f])

        self.js_string_list = line_list

    def compile_text_file(self):
        js_script = ''
        js_len = len(self.js_string_list)

        for _num, _l in enumerate(self.js_string_list):
            for _c in _l:
                js_script += _c

                if _num != js_len - 1 or _c != _l[-1]:
                    js_script += '\n'

        self.js_txt = js_script
        print('String file compiled: ', self.js_txt)

    def export_js(self):
        with open(self.js_name, 'w') as _file:
            _file.write(self.js_txt)
            _file.close()
        print('.txt exported successfully')

def generate_rows():
    # This was designed to generate the initial .ini files based off the ID codes
    # Initial variables
    _row_num = 18
    input_string = 'linkU{}DSC'
    route_string = 'linkU{}RA'
    frequency_string = 'linkU{}FR'
    file_list = [input_string, route_string, frequency_string]

    _input_list = ''
    _route_list = ''
    _freq_list = ''

    string_list = [_input_list, _route_list, _freq_list]

    filename_list = ['input.ini', 'route.ini', 'freq.ini']

    # double loops to generate numbered increments
    for _n in range(_row_num):
        _n += 1
        for _index in range(len(string_list)):
            if len(str(_n)) < 2:
                _n = '0' + str(_n)
            _str = file_list[_index].format(_n)
            _str += '\n'
            string_list[_index] += _str

    # Loop for exporting three separate .ini files
    for _n, _filename in enumerate(filename_list):
        with open(_filename, 'w') as _file:
            _file.write(string_list[_n])
            _file.close()

def pull_medications(_hex):
    excel_name = 'emarfatad.xls'
    _col_names = ['Medication', 'Route', 'Frequency']
    excel_workbook = pd.read_excel(excel_name, index_col=0, header=None, names=_col_names)
    print(excel_workbook)
    return excel_workbook.loc[_hex]

def generate_js(_list):
    js_code_m = "document.getElementById('linkU{}DSC').value = {};"
    js_code_r = "document.getElementById('linkU{}RA').value = {};"
    js_code_f = "document.getElementById('linkU{}FR').value = {};"

    _meds = _list['Medication'].tolist()
    _routes = _list['Route'].tolist()
    _freqs = _list['Frequency'].tolist()

    #_num_of = len(_meds)
    line_list = []
    for _num, _m in enumerate(_meds):

        if _num + 1 < 10:
            _num_str = '0' + str(_num+1)
        else:
            _num_str = str(_num + 1)

        temp_m = js_code_m.format(_num_str, _m)
        temp_r = js_code_r.format(_num_str, int(_routes[_num]))
        temp_f = js_code_f.format(_num_str, _freqs[_num])
        line_list.append([temp_m, temp_r, temp_f])

    return line_list

def compile_text_file(js_list):
    js_script = ''
    js_len = len(js_list)

    for _num, _l in enumerate(js_list):
        for _c in _l:
            js_script += _c

            if _num != js_len - 1 or _c != _l[-1]:
                js_script += '\n'

    return js_script

med_list = pull_medications('d')
_list = generate_js(med_list)
script = compile_text_file(_list)



auto = AutoFillGui()
auto.mainloop()

