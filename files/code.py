
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Fixing random state for reproducibility
np.random.seed(19680801)

#Set seaborn color scheme
sns.set(style='dark')

#-------------------------------------------------------------------------------------------------#
#Data wrangling
#-------------------------------------------------------------------------------------------------#

## POPULATION DATASET##
#get column names
column_names = pd.read_csv('ACSDP1Y2010.csv',skiprows=1, skipfooter=2)

#load files and filter the relevant data (until column 64)
df_2010 = pd.read_csv('ACSDP1Y2010.csv',header=None)
df_2010 = df_2010.iloc[2].values[0:65].reshape(1,65)
df_2011 = pd.read_csv('ACSDP1Y2011.csv',header=None)
df_2011 = df_2011.iloc[2].values[0:65].reshape(1,65)
df_2012 = pd.read_csv('ACSDP1Y2012.csv',header=None)
df_2012 = df_2012.iloc[2].values[0:65].reshape(1,65)
df_2013 = pd.read_csv('ACSDP1Y2013.csv',header=None)
df_2013 = df_2013.iloc[2].values[0:65].reshape(1,65)
df_2014 = pd.read_csv('ACSDP1Y2014.csv',header=None)
df_2014 = df_2014.iloc[2].values[0:65].reshape(1,65)
df_2015 = pd.read_csv('ACSDP1Y2015.csv',header=None)
df_2015 = df_2015.iloc[2].values[0:65].reshape(1,65)
df_2016 = pd.read_csv('ACSDP1Y2016.csv',header=None)
df_2016 = df_2016.iloc[2].values[0:65].reshape(1,65)
df_2017 = pd.read_csv('ACSDP1Y2017.csv',header=None)
df_2017 = df_2017.iloc[2].values[0:65].reshape(1,65)
df_2018 = pd.read_csv('ACSDP1Y2018.csv',header=None)
df_2018 = df_2018.iloc[2].values[0:65].reshape(1,65)

## POPULATION DATASET##

## CRIME DATASET##
crime_df = pd.read_csv('AnnArbor_crimes_2005_2018.csv',skiprows=1, skipfooter=2)
crime_df=crime_df.set_index('Type').T
crime_df=crime_df[5:]
#crime_df.rename(columns={'Type':'Year'})

#name cleaning
new_list_names = []

for name in column_names:
    splitting = name.split('!')
    new_name = ''
    for item in splitting:
        if not(item.isupper() or item==''):
            new_name=new_name + " " + item
    
    if new_name[0]==' ':
        new_name=new_name[1:]
    
    new_list_names.append(new_name)
#name cleaning

#create an array containing relevant values, merging the datasets
data = np.concatenate((df_2010,df_2011,df_2012,df_2013,df_2014,df_2015,df_2016, df_2017,df_2018), axis=0)

#convert the resulting list into a dataframe with new, clean names
df = pd.DataFrame(data,columns=new_list_names[0:65])

df.set_index(crime_df.index)

#drop irrelevant columns
df = df.drop(columns=['id','Geographic Area Name','Percent Total population','Percent Margin of Error Total population'])

#set both DFs to the same index and replace non numbers with NaN
df.index=crime_df.index
df = df.apply(pd.to_numeric, errors='coerce')

crime_df['Thefts'] = crime_df['Thefts'].str.replace(',', '').astype(int)
crime_df=crime_df.astype(str).astype(int)

#-------------------------------------------------------------------------------------------------#
#Data wrangling
#-------------------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------------------#
#Line plot recording the total population evolution in Ann Arbor
#-------------------------------------------------------------------------------------------------#

ax_total_pop=df['Estimate Total population'].plot(style='o-',c='orange',title='Ann Arbor\'s Population 2010-2018',grid=True,legend=True)
ax_total_pop.set_xlabel("Year")
ax_total_pop.set_ylabel("# People")
ax_total_pop.get_figure().savefig('EstPopulation.png')

#-------------------------------------------------------------------------------------------------#
#Line plot recording the total population evolution in Ann Arbor
#-------------------------------------------------------------------------------------------------#

                        
#-------------------------------------------------------------------------------------------------#
#Line subplots showing the evolution of different offenses over the years
#-------------------------------------------------------------------------------------------------#

x=crime_df.index.values

crime_breakdown_fig, axs = plt.subplots(len(crime_df)-1,figsize=(8, 29),sharex=False)

for i in range(len(crime_df.columns)):
    y=crime_df.iloc[:,i].values
    axs[i].plot(x,y,c='orange',linestyle='-',marker='o')
    axs[i].grid(linestyle='-', color='white')
    axs[i].set_ylabel("# " + crime_df.columns[i])
    #axs[i].set_yticks(crime_df.iloc[:,i].values.tolist(), minor=False)

crime_breakdown_fig.suptitle('Ann Arbor\'s Recorded crimes 2010-2018', fontsize=16)
#fig.tight_layout()
crime_breakdown_fig.subplots_adjust(top=0.97)
crime_breakdown_fig.savefig('CrimeTime.png')

#-------------------------------------------------------------------------------------------------#
#Line subplots showing the evolution of different offenses over the years
#-------------------------------------------------------------------------------------------------#



#-------------------------------------------------------------------------------------------------#
#Donut chart illustrating the crimes committed in the periods between 2010-2014 and 2014-2018
#-------------------------------------------------------------------------------------------------#

figpie, axpie = plt.subplots(figsize=(20,20))
size = 0.4

totalvalues = np.empty(0)
broken_values = np.empty(0)

crime_df_aux=crime_df.drop(['Murders','Thefts'],axis=1)
crime_type = []
broken_labels = []

for i in range(len(crime_df_aux.columns)):
    totalvalues=np.append(totalvalues,crime_df_aux.iloc[:,i].values.sum())
    crime_type.append(crime_df_aux.columns[i] + " Total: " + str(crime_df_aux.iloc[:,i].values.sum()))
    broken_values=np.append(broken_values,crime_df_aux.iloc[0:4,i].values.sum())
    broken_values=np.append(broken_values,crime_df_aux.iloc[4:,i].values.sum())
    broken_labels.append("2010-2014" + " Total: " + str(crime_df_aux.iloc[0:4,i].values.sum()))
    broken_labels.append("2015-2018" + " Total: " + str(crime_df_aux.iloc[4:,i].values.sum()))


outter_cmap = plt.get_cmap("RdYlGn")
inner_cmap = plt.get_cmap("pink")
outter_colors = outter_cmap(np.arange(0, 1, 1/7))
inner_colors = inner_cmap(np.arange(0.1, 0.7, 1/2))

axpie.pie(totalvalues,labels=crime_type,labeldistance=0.8,radius=1.2,colors=outter_colors,wedgeprops=dict(width=size, edgecolor='white'))

#Following line should center labels on wedge radial axis but it causes an unkown bug
#axpie.pie(broken_values.flatten(),labels=broken_labels,textprops = dict(rotation_mode = 'anchor', va='center', ha='left'),rotatelabels = 270,textprops={'color':"w"},labeldistance=0.6,radius=1.2-size,colors=inner_colors, wedgeprops=dict(width=size, edgecolor='black'))
#This is the same code line as the previous one but without the dictionary: "textprops = dict(rotation_mode = 'anchor', va='center',"

axpie.pie(broken_values.flatten(),labels=broken_labels,rotatelabels = 270,textprops={'color':"w"},labeldistance=0.6,radius=1.2-size,colors=inner_colors, wedgeprops=dict(width=size, edgecolor='black'))

axpie.set_title("Crime breakdown in 2010-2014 and 2015-2020 periods",{'fontsize': 16})

figpie.savefig('Pie.png')
#-------------------------------------------------------------------------------------------------#
#Donut chart illustrating the crimes committed in the periods between 2010-2014 and 2014-2018
#-------------------------------------------------------------------------------------------------#




#-------------------------------------------------------------------------------------------------#
#Average # Population Estimate for the period 2010-2018
#-------------------------------------------------------------------------------------------------#

#Fill NaN with mean value
df=df.fillna(df.mean())

age_breakdown_raw=["Estimate Under 5 years",'Estimate 5 to 9 years','Estimate 10 to 14 years','Estimate 15 to 19 years','Estimate 20 to 24 years','Estimate 25 to 34 years','Estimate 35 to 44 years','Estimate 45 to 54 years','Estimate 55 to 59 years','Estimate 60 to 64 years','Estimate 65 to 74 years','Estimate 75 to 84 years','Estimate 85 years and over']
age_breakdown_errors=['Percent Margin of Error Under 5 years','Percent Margin of Error 5 to 9 years','Percent Margin of Error 10 to 14 years','Percent Margin of Error 15 to 19 years','Percent Margin of Error 20 to 24 years','Percent Margin of Error 25 to 34 years','Percent Margin of Error 35 to 44 years','Percent Margin of Error 45 to 54 years','Percent Margin of Error 55 to 59 years','Percent Margin of Error 60 to 64 years','Percent Margin of Error 65 to 74 years','Percent Margin of Error 75 to 84 years','Percent Margin of Error 85 years and over']

age_breakdown_labels = []
for item in age_breakdown_raw:
    age_breakdown_labels.append(item[9:])

df[age_breakdown_raw]=df[age_breakdown_raw].astype(int)

age_interval_mean = np.mean(df[age_breakdown_raw])
age_interval_std = np.std(df[age_breakdown_raw])

mean_fig, mean_ax = plt.subplots(figsize=(10,10))
mean_ax.bar(age_breakdown_labels, age_interval_mean, yerr=age_interval_std, align='center', alpha=0.5, ecolor='black', capsize=10, color='orange')
mean_ax.set_ylabel('Average # Population Estimate')
mean_ax.set_title('Age Distribution of the Population for the period 2010-2018', fontsize=16)
mean_ax.yaxis.grid(True)

plt.xticks(age_breakdown_labels, rotation='vertical')

mean_fig.savefig('AgeDistribution.png')

#-------------------------------------------------------------------------------------------------#
#Average # Population Estimate for the period 2010-2018
#-------------------------------------------------------------------------------------------------#




#-------------------------------------------------------------------------------------------------#
#Correlations between types of crime and Population Evolution
#-------------------------------------------------------------------------------------------------#

crime_df['Total crimes']=crime_df.values.sum(axis=1)

data1 = crime_df
data1['Estimate Total population']=df['Estimate Total population']

corr_fig1,corr_fig_ax = plt.subplots(3,3,figsize=(16,16),sharex=False)

outter_cmap = plt.get_cmap("RdYlGn")
outter_colors = outter_cmap(np.arange(0, 1, 1/9))

idx=data1['Estimate Total population'].values

for i in range(len(data1.columns[:-1])):
    if i<3:
        line=0
        column=i
    if i>=3 and i<6:
        line=1
        column=i-3
    if i>=6:
        line=2
        column=i-6
    sns.regplot(x=idx,y=data1.iloc[:,i],ax=corr_fig_ax[line,column],color=outter_colors[i])


corr_fig1.suptitle('Correlations between Crime and Temporal Population Evolution', fontsize=16)
corr_fig1.subplots_adjust(top=0.96)
corr_fig1.savefig('Correlations.png')

#-------------------------------------------------------------------------------------------------#
#Correlations between types of crime and Population Evolution
#-------------------------------------------------------------------------------------------------#


