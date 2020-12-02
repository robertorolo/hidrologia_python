from io import StringIO 
import pandas as pd

def create_dic(lines):

    use_lines = lines[4:7]
    dic = {}
    for l in use_lines:
        splitted = l.split(':')
        dic[splitted[0]] = {}
        elements = splitted[1:][0].split(',')
        for e in elements:
            code = int(e.split('=')[0])
            name = e.split('=')[1][:]
            name = name.replace(' ', '')
            name = name.replace('\n', '')
            dic[splitted[0]][code] = name
    
    return dic

def codigo(lines):
    
    name = int(lines[9].split(':')[-1].replace('\n', ''))
    
    return name

def create_df(lines, d):
    
    list_vals = lines[13:]
    string = StringIO(''.join(list_vals))
    df = pd.read_csv(string, index_col=False, sep=';', names=lines[12][:-1].split(';'))
    df['NivelConsistencia'] = df['NivelConsistencia'].map(d['NivelConsistencia'])
    df['TipoMedicaoChuvas'] = df['TipoMedicaoChuvas'].map(d['TipoMedicaoChuvas'])
    for i in range(1,32):
        string = str(i)
        if len(string) == 1:
            string = str(0)+string
        column_name = 'Chuva{}Status'.format(string)
        df[column_name] = df[column_name].map(d['Status'])
            
    return df

class Station:
    
    def __init__(self, file):

        f = open(file, 'r')
        lines = f.readlines()

        d = create_dic(lines)
        self.code = codigo(lines)
        self.data = create_df(lines, d)