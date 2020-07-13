import collections as col
#help(col.OrderedDict)

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

route_table = """
</option><option value="1" selected="selected">1=by mouth (PO)
</option><option value="2">2=sub-lingual (SL)
</option><option value="3">3=intramuscular (IM)
</option><option value="4">4=intravenous (IV)
</option><option value="5">5=subcutaneous (SQ)
</option><option value="6">6=rectal (R)
</option><option value="7">7=topical
</option><option value="8">8=inhalation
</option><option value="9">9=enteral tube
</option><option value="10">10=other
"""
frequency_types = """</option><option value="PR">PR</option><option value="1H">1H</option><option value="2H">2H</option><option value="3H">3H
</option><option value="4H">4H</option><option value="6H">6H</option><option value="8H">8H</option><option value="1D" selected="selected">1D
</option><option value="2D">2D</option><option value="3D">3D</option><option value="4D">4D</option><option value="5D">5D
</option><option value="1W">1W</option><option value="2W">2W</option><option value="3W">3W</option><option value="QO">QO
</option><option value="4W">4W</option><option value="5W">5W</option><option value="6W">6W</option><option value="1M">1M
</option><option value="2M">2M</option><option value="C">C</option><option value="O">O</option><option value="">"""

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

# Example JS
# document.getElementById('startdate_job').value = '01-01-2015';
# document.getElementById('naam_werkgever_id').value = 'Test';
# document.getElementById('plaats_werkgever_id').value = '0Test';
# document.getElementById('functie_id').value = 'Tester';
# document.getElementById('30_regeling').checked = true;

# function setSelectedIndex(s, v) {for (var i = 0; i < s.options.length; i++)
# {if (s.options[i].text == v) {s.options[i].selected = true; return;}}}
# setSelectedIndex(document.getElementById("monthmultiplier"), "maand");

# document.getElementById('enddate_id_job').value = '01-01-2018';
# document.getElementById('loondienst_soort_0').checked = true;
# document.getElementById('loondienst_soort_1').checked = false;