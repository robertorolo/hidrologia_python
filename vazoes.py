from io import StringIO 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_date(s):
    
    splitted = s.split('/')
    ano = splitted[2]
    mes = splitted[1]
    anomes = int(ano+mes)

    return anomes

def create_dic(lines):

    use_lines = lines[4:8]
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
    
    name = int(lines[10].split(':')[-1].replace('\n', ''))
    
    return name

def create_df(lines, d):
    
    list_vals = lines[14:]
    string = StringIO(''.join(list_vals))
    df = pd.read_csv(string, index_col=False, sep=';', names=lines[13][:-1].split(';'))
    df['NivelConsistencia'] = df['NivelConsistencia'].map(d['NivelConsistencia'])
    df['MediaDiaria'] = df['MediaDiaria'].map(d['MediaDiaria'])
    df['MetodoObtencaoVazoes'] = df['MetodoObtencaoVazoes'].map(d['MetodoObtencaoVazoes'])
    for i in range(1,32):
        string = str(i)
        if len(string) == 1:
            string = str(0)+string
        column_name = 'Vazao{}Status'.format(string)
        df[column_name] = df[column_name].map(d['Status'])
            
    return df

class Estacao:
    
    def __init__(self, file, area=None):

        f = open(file, 'r')
        lines = f.readlines()

        d = create_dic(lines)
        self.code = codigo(lines)
        self.data = create_df(lines, d)
        self.area = area
        
class Estacoes:

    def __init__(self, base, estacao_lts):
        
        self.base = base
        self.estacao_lts = estacao_lts

        #datas da base
        todas = np.concatenate([e.data['Data'].values for e in estacao_lts])
        todas = np.concatenate([base.data['Data'].values, todas])
        todas = np.array([read_date(t) for t in todas])
        todas = np.unique(todas)
        todas = np.sort(todas)

        datavazao = pd.DataFrame()
        datavazao['Data'] = todas

        #preenchendo vazoes
        estacoes = estacao_lts
        estacoes.append(base)

        for idx, row in datavazao.iterrows():
            for e in estacoes:
                datavazao[e.code] = float('nan')
                anomes = read_date(e.data['Data'])

                for idxe, value in enumerate(anomes):
                    pass


    def disponibilidade():
        
        fig, ax = plt.subplots()

        #plotando base
        

