import b3_parser as b3
import pandas as pd
import sqlite3

if __name__ == '__main__':
    b3.CreateCSV('COTAHIST_A2019.TXT')
    conn = sqlite3.connect('data_acoes.db')
    df = pd.read_csv('COTAHIST_A2019.csv')

    df = df.loc[:, ['DATA', 'CODNEG', 'PREABE', 'PREMAX', 'PREMIN', 'PREULT']].drop([779229])
    df.iloc[:, 2:] = df.iloc[:, 2:].astype(float).div(100)
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y%m%d')
    df.iloc[:, 0] = df.iloc[:, 0].dt.strftime('%Y-%m-%d')
    df.to_sql('acoes_b3', conn, if_exists='replace', index=False)

    conn.close()