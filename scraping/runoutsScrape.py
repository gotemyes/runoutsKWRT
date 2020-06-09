from bs4 import BeautifulSoup
import requests
import pandas as pd

def runouts_scrape():

    top50Test = pd.read_csv('../data/top50TestPartnerships.csv')
    top50ODI = pd.read_csv('../data/top50ODIPartnerships.csv')
    top50T20I = pd.read_csv('../data/top50T20IPartnerships.csv')
    top50All = pd.read_csv('../data/top50AllPartnerships.csv')

    idDict = {}
    for ind,row in top50Test.iterrows():
        idDict[row['Batsman1']] = row['Batsman1ID']
        idDict[row['Batsman2']] = row['Batsman2ID']
    for ind,row in top50ODI.iterrows():
        idDict[row['Batsman1']] = row['Batsman1ID']
        idDict[row['Batsman2']] = row['Batsman2ID']
    for ind,row in top50T20I.iterrows():
        idDict[row['Batsman1']] = row['Batsman1ID']
        idDict[row['Batsman2']] = row['Batsman2ID']
    for ind,row in top50All.iterrows():
        idDict[row['Batsman1']] = row['Batsman1ID']
        idDict[row['Batsman2']] = row['Batsman2ID']

    playerID = idDict[row['Batsman1']]
    player = row['Batsman1']

    print(f'Finding runouts for {len(idDict)} unique players')


    allDFlist = []
    ## iterate through players and create a df for each containing the runouts
    for player in idDict:
        playerID = idDict[player]

        url = f'https://stats.espncricinfo.com/ci/engine/player/{playerID}.html?class=11;dismissal=4;filter=advanced;orderby=start;outs=1;template=results;type=batting;view=fow_list'

        website = requests.get(url)
        soup = BeautifulSoup(website.content,'html.parser')
        data=[]
        for tag in soup.find_all('tr'):
            data.append(tag.get_text().split('\n'))
        df = pd.DataFrame(data=data)

        '''for tag in soup.find_all('div',{'class':'icc-home'}):
            if not player in tag.get_text():
                raise KeyError(f'This link does not seem to refer to the correct player: {player}')'''

        ## cleaning
        df.columns = df.iloc[9]
        df.drop(df.index[:10],inplace=True)
        df.reset_index(inplace=True,drop=True)

        if 'Partner' not in df.columns:
            continue
        finalInd = df[df['Partner']==''].index[0]
        df.drop(df.index[finalInd:],inplace=True)

        df = df[df.columns[1:11]].copy()
        df['Match'] = df.iloc[:,8].values


        df = df[['Partner','Wkt','Runs','In','Out','Inns','Opposition','Ground','Start Date','Match']].copy()
        df['Batsman'] = player



        dropInds = []
        for ind, row in df.iterrows():
            if ind == len(df)-1:
                continue

            if (row['Match'] == df.loc[ind+1]['Match'])&(row['Inns'] == df.loc[ind+1]['Inns']):
                dropInds.append(ind)


        df.drop(index = dropInds,inplace=True)
        df.reset_index(inplace=True,drop=True)

        allDFlist.append(df)

    allDF = pd.concat(allDFlist)

    allDF['Wkt'] = pd.to_numeric(allDF['Wkt'])
    allDF['NO'] = allDF.apply(lambda row: True if row['Runs'][-1]=='*' else False, axis = 1)
    allDF['Runs'] = allDF.apply(lambda row: int(row['Runs'][:-1]) if row['NO'] else int(row['Runs']), axis=1)
    allDF['Inns'] = pd.to_numeric(allDF['Inns'])
    allDF['Format'] = allDF.apply(lambda row: row['Match'].split(' # ')[0], axis=1)
    allDF['Match'] = allDF.apply(lambda row: row['Match'].split(' # ')[1], axis=1)
    allDF['Opposition'] = allDF.apply(lambda row: row['Opposition'].split(' v ')[-1],axis = 1)

    allDF.reset_index(inplace=True,drop=True)

    allDF.to_csv(f'../data/playerRunouts.csv')

if __name__ == '__main__':
    runouts_scrape()
