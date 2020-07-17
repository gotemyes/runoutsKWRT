import pandas as pd
import matplotlib.pyplot as plt

test = pd.read_csv('../data/top50TestPartnerships.csv')
odi = pd.read_csv('../data/top50ODIPartnerships.csv')
t20i = pd.read_csv('../data/top50T20IPartnerships.csv')
all = pd.read_csv('../data/top50AllPartnerships.csv')

runouts = pd.read_csv('../data/playerRunouts.csv')


## ALL
pair_all_runouts_list = []
for ind, row in all.iterrows():
    this_pair_runouts = runouts[
        (((runouts['Partner']==row['Batsman1'])&(runouts['Batsman']==row['Batsman2']))|
            ((runouts['Partner']==row['Batsman2'])&(runouts['Batsman']==row['Batsman1'])))].copy()

    pair_all_runouts_list.append([row['Batsman1']+ ', '+row['Batsman2'],len(this_pair_runouts),row['Inns']])

all_runout_df = pd.DataFrame(pair_all_runouts_list,columns = [
    'Pair',
    'Runouts',
    'Inns'
])
all_runout_df['Inns_per_runout'] = all_runout_df['Inns']/all_runout_df['Runouts']
all_runout_df['Runout_pct'] = 100*all_runout_df['Runouts']/all_runout_df['Inns']
## order by higehst runout percentage
ordered_all = all_runout_df.sort_values('Runout_pct',ascending=False).reset_index()
kwrt_all = ordered_all[ordered_all['Pair']=='LRPL Taylor, KS Williamson'].index.values[0]

## Test
pair_test_runouts_list = []
for ind, row in test.iterrows():
    this_pair_runouts = runouts[
        (runouts['Format']=='Test')&
        (((runouts['Partner']==row['Batsman1'])&(runouts['Batsman']==row['Batsman2']))|
            ((runouts['Partner']==row['Batsman2'])&(runouts['Batsman']==row['Batsman1'])))].copy()

    pair_test_runouts_list.append([row['Batsman1']+ ', '+row['Batsman2'],len(this_pair_runouts),row['Inns']])

test_runout_df = pd.DataFrame(pair_test_runouts_list,columns = [
    'Pair',
    'Runouts',
    'Inns'
])
test_runout_df['Inns_per_runout'] = test_runout_df['Inns']/test_runout_df['Runouts']
test_runout_df['Runout_pct'] = 100*test_runout_df['Runouts']/test_runout_df['Inns']
## order by higehst runout percentage
ordered_test = test_runout_df.sort_values('Runout_pct',ascending=False).reset_index()
kwrt_test = ordered_test[ordered_test['Pair']=='LRPL Taylor, KS Williamson'].index.values[0]

## odi
pair_odi_runouts_list = []
for ind, row in odi.iterrows():
    this_pair_runouts = runouts[
        (runouts['Format']=='ODI')&
        (((runouts['Partner']==row['Batsman1'])&(runouts['Batsman']==row['Batsman2']))|
            ((runouts['Partner']==row['Batsman2'])&(runouts['Batsman']==row['Batsman1'])))].copy()

    pair_odi_runouts_list.append([row['Batsman1']+ ', '+row['Batsman2'],len(this_pair_runouts),row['Inns']])

odi_runout_df = pd.DataFrame(pair_odi_runouts_list,columns = [
    'Pair',
    'Runouts',
    'Inns'
])
odi_runout_df['Inns_per_runout'] = odi_runout_df['Inns']/odi_runout_df['Runouts']
odi_runout_df['Runout_pct'] = 100*odi_runout_df['Runouts']/odi_runout_df['Inns']
## order by higehst runout percentage
ordered_odi = odi_runout_df.sort_values('Runout_pct',ascending=False).reset_index()
kwrt_odi = ordered_odi[ordered_odi['Pair']=='LRPL Taylor, KS Williamson'].index.values[0]

## T20i
pair_t20i_runouts_list = []
for ind, row in t20i.iterrows():
    this_pair_runouts = runouts[
        (runouts['Format']=='T20I')&
        (((runouts['Partner']==row['Batsman1'])&(runouts['Batsman']==row['Batsman2']))|
            ((runouts['Partner']==row['Batsman2'])&(runouts['Batsman']==row['Batsman1'])))].copy()

    pair_t20i_runouts_list.append([row['Batsman1']+ ', '+row['Batsman2'],len(this_pair_runouts),row['Inns']])

t20i_runout_df = pd.DataFrame(pair_t20i_runouts_list,columns = [
    'Pair',
    'Runouts',
    'Inns'
])
t20i_runout_df['Inns_per_runout'] = t20i_runout_df['Inns']/t20i_runout_df['Runouts']
t20i_runout_df['Runout_pct'] = 100*t20i_runout_df['Runouts']/t20i_runout_df['Inns']
## order by higehst runout percentage
ordered_t20i = t20i_runout_df.sort_values('Runout_pct',ascending=False).reset_index()
kwrt_t20i = ordered_t20i[ordered_t20i['Pair']=='LRPL Taylor, KS Williamson'].index.values[0]

## plots
entries = 50
fig, ax  = plt.subplots(figsize=(12,7))
plt.barh(
    y = [el for el in range(entries)][::-1],
    width = ordered_all['Runout_pct'].iloc[:entries],
)
plt.barh(
    y = [el for el in range(entries)][::-1][kwrt_all],
    width = [ordered_all['Runout_pct'].iloc[kwrt_all]],
    color='red'
)
ax.set_yticks([el for el in range(entries)][::-1])
ax.set_yticklabels(ordered_all['Pair'].iloc[:entries])
plt.xlabel('Runout Dismissal Percentage')
plt.title('Runout Dismissal Percentage For Top 50 All Format Partnerships')
plt.margins(y=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()

## plots
fig, ax  = plt.subplots(figsize=(12,7))
plt.barh(
    y = [el for el in range(entries)][::-1],
    width = ordered_test['Runout_pct'].iloc[:entries],
)
plt.barh(
    y = [el for el in range(entries)][::-1][kwrt_test],
    width = [ordered_test['Runout_pct'].iloc[kwrt_test]],
    color='red'
)
ax.set_yticks([el for el in range(entries)][::-1])
ax.set_yticklabels(ordered_test['Pair'].iloc[:entries])
plt.xlabel('Runout Dismissal Percentage')
plt.title('Runout Dismissal Percentage For Top 50 Test Partnerships')
plt.margins(y=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()

## plots
fig, ax  = plt.subplots(figsize=(12,7))
plt.barh(
    y = [el for el in range(entries)][::-1],
    width = ordered_odi['Runout_pct'].iloc[:entries],
)
plt.barh(
    y = [el for el in range(entries)][::-1][kwrt_odi],
    width = [ordered_odi['Runout_pct'].iloc[kwrt_odi]],
    color='red'
)
ax.set_yticks([el for el in range(entries)][::-1])
ax.set_yticklabels(ordered_odi['Pair'].iloc[:entries])
plt.xlabel('Runout Dismissal Percentage')
plt.title('Runout Dismissal Percentage For Top 50 ODI Partnerships')
plt.margins(y=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()

## plots
fig, ax  = plt.subplots(figsize=(12,7))
plt.barh(
    y = [el for el in range(entries)][::-1],
    width = ordered_t20i['Runout_pct'].iloc[:entries],
)
plt.barh(
    y = [el for el in range(entries)][::-1][kwrt_t20i],
    width = [ordered_t20i['Runout_pct'].iloc[kwrt_t20i]],
    color='red'
)
ax.set_yticks([el for el in range(entries)][::-1])
ax.set_yticklabels(ordered_t20i['Pair'].iloc[:entries])
plt.xlabel('Runout Dismissal Percentage')
plt.title('Runout Dismissal Percentage For Top 50 T20I Partnerships + KWRT')
plt.margins(y=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()

plt.savefig('../images/t20i.png')
plt.close()
plt.savefig('../images/odi.png')
plt.close()
plt.savefig('../images/test.png')
plt.close()
plt.savefig('../images/all.png')
plt.close()
#plt.show()
