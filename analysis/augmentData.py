import pandas as pd
from bs4 import BeautifulSoup
import requests


def find_partnership(bat1,bat2,format):
    ## called to find partnership if it isn't in the top 50
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

    presentKWRT = False
    page = 2
    while not presentKWRT:
        ## scrape data from sequential pages on cricinfo
        url = f'https://stats.espncricinfo.com/ci/engine/stats/index.html?class={formatID};page={page};template=results;type=fow'
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

        df.columns.name=''

        onlyKWRT = df[
            ((df['Batsman1']=='KS Williamson')|(df['Batsman2']=='KS Williamson'))&
            ((df['Batsman1']=='LRPL Taylor')|(df['Batsman2']=='LRPL Taylor'))]

        if len(onlyKWRT)==1:
            presentKWRT = True
        page+=1

    onlyKWRT.index = (page-2)*50+onlyKWRT.index.values
    return onlyKWRT

def augmentation():

    ## load partnership data
    tests = pd.read_csv('../data/top50TestPartnerships.csv',index_col=0)
    odis = pd.read_csv('../data/top50ODIPartnerships.csv',index_col=0)
    t20is = pd.read_csv('../data/top50T20IPartnerships.csv',index_col=0)
    all = pd.read_csv('../data/top50AllPartnerships.csv',index_col=0)

    ## isolate KW & RT
    testKWRT = tests[
        ((tests['Batsman1']=='KS Williamson')|(tests['Batsman2']=='KS Williamson'))&
        ((tests['Batsman1']=='LRPL Taylor')|(tests['Batsman2']=='LRPL Taylor'))]
    odiKWRT = odis[
        ((odis['Batsman1']=='KS Williamson')|(odis['Batsman2']=='KS Williamson'))&
        ((odis['Batsman1']=='LRPL Taylor')|(odis['Batsman2']=='LRPL Taylor'))]
    t20iKWRT = t20is[
        ((t20is['Batsman1']=='KS Williamson')|(t20is['Batsman2']=='KS Williamson'))&
        ((t20is['Batsman1']=='LRPL Taylor')|(t20is['Batsman2']=='LRPL Taylor'))]
    allKWRT = all[
        ((all['Batsman1']=='KS Williamson')|(all['Batsman2']=='KS Williamson'))&
        ((all['Batsman1']=='LRPL Taylor')|(all['Batsman2']=='LRPL Taylor'))]

    ## check that KW & RT are found. If not, find them and append
    if len(testKWRT)==0:
        print('KWRT not in top 50 tests: scraping and appending')
        testKWRT = find_partnership('KS Williamson','LRPL Taylor','Test')
        tests.append(testKWRT)
    if len(odiKWRT)==0:
        print('KWRT not in top 50 odi: scraping and appending')
        odiKWRT = find_partnership('KS Williamson','LRPL Taylor','ODI')
        odis.append(odiKWRT)
    if len(t20iKWRT)==0:
        print('KWRT not in top 50 t20is: scraping and appending')
        t20iKWRT = find_partnership('KS Williamson','LRPL Taylor','T20I')
        t20is.append(t20iKWRT)
    if len(allKWRT)==0:
        print('KWRT not in top 50 all: scraping and appending')
        allKWRT = find_partnership('KS Williamson','LRPL Taylor','All')
        all.append(allKWRT)

    print(testKWRT)
    print(odiKWRT)
    print(t20iKWRT)
    print(allKWRT)

if __name__ == '__main__':
    augmentation()
