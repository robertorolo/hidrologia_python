from io import StringIO 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def anomes_trans(s):

    splitted = s.split('/')
    ano = splitted[2]
    mes = splitted[1]

    return int(ano+mes)

def dia_mes(anomes):

    dias_mes = {
    '01':31,
    '02':28,
    '03':31,
    '04':30,
    '05':31,
    '06':30,
    '07':31,
    '08':31,
    '09':30,
    '10':31,
    '11':30,
    '12':31
    }
    
    anomes = str(anomes)
    ano = anomes[:4]
    mes = anomes[4:]
    
    if (int(ano)%4==0 and int(ano)%100!=0) or (int(ano)%400==0):
        dias_mes['02'] = 29
    
    lista_dias = [int(ano+mes+str(i)) if len(str(i)) > 1 else int(ano+mes+'0'+str(i)) for i in range(1, dias_mes[mes])]

    return lista_dias

def fill_ano(anomesmin, anomesmax):

    anomin = int(str(anomesmin)[:4])
    mesmin = int(str(anomesmin)[4:])

    anomax = int(str(anomesmax)[:4])
    mesmax = int(str(anomesmax)[4:])

    anorange = [i for i in range(anomin, anomax+1)]

    anomesrange = []

    for idx, ano in enumerate(anorange):
        if idx == 0:
            mesrange = [i for i in range(mesmin, 13, 1)]
            for j in mesrange:
                anomesrange.append(int(str(ano)+str(j)) if len(str(j)) > 1 else int(str(ano)+'0'+str(j)))
        elif idx == len(anorange)-1:
            mesrange = [i for i in range(1, mesmax+1, 1)]
            for j in mesrange:
                anomesrange.append(int(str(ano)+str(j)) if len(str(j)) > 1 else int(str(ano)+'0'+str(j)))
        else:
            mesrange = [i for i in range(1, 13, 1)]
            for j in mesrange:
                anomesrange.append(int(str(ano)+str(j)) if len(str(j)) > 1 else int(str(ano)+'0'+str(j)))

    return anomesrange

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
        self.codigo = codigo(lines)
        self.data = create_df(lines, d)
        self.area = area
        
class Estacoes:

    def __init__(self, base, estacao_lts):

        print('Inicializando objeto Estacoes...')
        
        self.base = base
        self.estacao_lts = estacao_lts

        #estabelencendo o range de datas
        todas = np.concatenate([e.data['Data'].values for e in estacao_lts])
        todas = np.concatenate([base.data['Data'].values, todas])
        todas = np.array([anomes_trans(t) for t in todas])
        todas = np.unique(todas)
        todas = np.sort(todas)
        anomin, anomax = min(todas), max(todas)
        self.anomin, self.anomax = anomin, anomax
        anomesrange = fill_ano(anomin, anomax)
        
        #criando novo dataframe de dias e vazões
        df_lista = estacao_lts
        df_lista.append(base)
        self.df_lista = df_lista
        
        vazao_df = pd.DataFrame()
        
        for i in anomesrange:
            concat_df = pd.DataFrame()
            dia_mes_list = dia_mes(i)
            concat_df['Data'] = dia_mes_list
            dias = str(dia_mes_list[-1])[6:]
            colunas = ['Vazao{}'.format(i) if len(str(i)) > 1 else 'Vazao0{}'.format(i) for i in range(1,int(dias)+1)]
            for df in df_lista:
                codigo_estacao = df.codigo
                for idx, row in df.data.iterrows():
                    anomes = anomes_trans(row['Data'])
                    
                    if anomes == i:
                        valores = row[colunas].values
                        valores = [float(f.replace(',','.')) if isinstance(f, str) else f for f in valores]
                        concat_df[codigo_estacao] = valores
                
            vazao_df = vazao_df.append(concat_df)

        self.vazao_df = vazao_df

        print('Feito!')
        
    def correlacao(self):

        pass
    
    def hidrograma(self):
        
        fig, ax = plt.subplots()

        for i in self.df_lista:
            ax.plot([i for i in range(len(self.vazao_df))], self.vazao_df[i.codigo], label=i.codigo)  

        plt.grid(linestyle='--')
        plt.legend()
        plt.show()     

