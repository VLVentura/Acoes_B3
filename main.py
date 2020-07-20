import b3_parser as b3
import pandas as pd
import sqlite3

if __name__ == '__main__':
    b3.CreateCSV('COTAHIST_A2019.TXT')
    conn = sqlite3.connect('data_acoes.db')
    cursor = conn.cursor()
    df = pd.read_csv('COTAHIST_A2019.csv')

    df = df.loc[:, ['DATA', 'CODNEG', 'PREABE', 'PREMAX', 'PREMIN', 'PREULT', 'VOLTOT']] \
           .drop(df.index[-1])
    df.iloc[:, 2:] = df.iloc[:, 2:].astype(float)
    df.iloc[:, 2:6] = df.iloc[:, 2:6].div(100)
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y%m%d')
    df.iloc[:, 0] = df.iloc[:, 0].dt.strftime('%Y-%m-%d')
    # Filter to the stocks negotiated all days of the year
    df = df[df.groupby('CODNEG').DATA.transform('count') > 247]
    df.to_sql('acoes_b3', conn, if_exists='replace', index=False)

    # Query receiving data from a start date and final date
    stockName = 'AALR3'
    dStart = '2019-01-02'
    dEnd = '2019-01-03'

    sql = (
        'SELECT DATA, PREABE, PREMAX, PREMIN, PREULT, VOLTOT FROM acoes_b3 '
        'WHERE "CODNEG" = ? '
        'AND "DATA" BETWEEN ? AND ?'
    )
    pd.read_sql(
        sql, 
        conn, 
        params=(stockName, dStart, dEnd)
    )

    # Query receiving data from a start date + n quotas (it's the same SQL command)
    stockName = 'AALR3'
    dStart = '2019-01-02'
    nQuotas = 7 + 1 # Value given from the user + 1
    dEnd = str(pd.to_datetime(dStart) + pd.Timedelta(days=nQuotas)).split()[0]

    sql = (
        'SELECT DATA, PREABE, PREMAX, PREMIN, PREULT, VOLTOT FROM acoes_b3 '
        'WHERE "CODNEG" = ? '
        'AND "DATA" BETWEEN ? AND ?'
    )
    pd.read_sql(
        sql, 
        conn, 
        params=(stockName, dStart, dEnd)
    )

    cursor.close()
    conn.close()