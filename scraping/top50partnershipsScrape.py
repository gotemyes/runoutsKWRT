from bs4 import BeautifulSoup
import requests
import pandas as pd

def total_partnership_scrape(format):

    ## format
    if format == 'Test':
        formatID = 1
    elif format == 'ODI':
        formatID = 2
    elif format == 'T20I':
        formatID = 3
    elif format == 'All':
        formatID = 11
    else:
        raise ValueError('Format must be one of "Test", "ODI", "T20I", "All"')

    ## scrape data for highest test partnerships (aggregate) from espncricinfo
    url = f'https://stats.espncricinfo.com/ci/engine/stats/index.html?class={formatID};template=results;type=fow'
    website = requests.get(url)
    soup = BeautifulSoup(website.content,'html.parser')
    data=[]
    idDict = {}
    for tag in soup.find_all('tr'):
        data.append(tag.get_text().split('\n'))
        for newTag in tag.find_all('a',class_='data-link'):
            idDict[newTag.get_text()] = newTag['href'].split('.')[0].split('/')[-1]
    df = pd.DataFrame(data=data)

    ## cleaning
    df.columns = df.iloc[3]
    df.drop(df.index[:4],inplace=True)
    df.reset_index(inplace=True)
    finalInd = df[df['Partners']==''].index.tolist()[0]
    df = df.iloc[:finalInd].copy()
    df = df[[
        'Partners',
        'Span',
        'Inns',
        'NO',
        'Runs',
        'High',
        'Ave',
        '100',
        '50']].copy()

    df['Rank'] = [el+1 for el in df.index.to_list()]
    df['Inns'] = pd.to_numeric(df['Inns'])
    df['NO'] = pd.to_numeric(df['NO'])
    df['HighNO'] = df.apply(lambda row: True if row['High'][-1]=='*' else False, axis=1)
    df['High'] = df.apply(lambda row: int(row['High'][:-1]) if row['HighNO'] else int(row['High']), axis=1)
    df['Runs'] = pd.to_numeric(df['Runs'])
    df['High'] = pd.to_numeric(df['High'])
    df['Ave'] = pd.to_numeric(df['Ave'])
    df['100'] = pd.to_numeric(df['100'])
    df['50'] = pd.to_numeric(df['50'])

    df['StartYear'] = df.apply(lambda row: int(row['Span'].split('-')[0]),axis=1)
    df['EndYear'] = df.apply(lambda row: int(row['Span'].split('-')[1]),axis=1)
    df['Team'] = df.apply(lambda row: row['Partners'].split('(')[-1][:-1],axis=1)
    df['Batsman1'] = df.apply(lambda row: row['Partners'].split(',')[0],axis=1)
    df['Batsman1ID'] = df.apply(lambda row: idDict[row['Batsman1']],axis=1)
    df['Batsman2'] = df.apply(lambda row: row['Partners'].split(',')[1].split('(')[0].strip(),axis=1)
    df['Batsman2ID'] = df.apply(lambda row: idDict[row['Batsman2']],axis=1)

    df.drop(columns=['Span','Partners'],inplace=True)

    df.to_csv(f'../data/top{len(df)}{format}Partnerships.csv')

if __name__ == '__main__':
    total_partnership_scrape(format = 'Test')
    total_partnership_scrape(format = 'ODI')
    total_partnership_scrape(format = 'T20I')
    total_partnership_scrape(format = 'All')
