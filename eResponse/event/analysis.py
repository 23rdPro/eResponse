import time
import uuid
import random

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

from django.db.models import Count

from eResponse.event.models import *


def prepare_data() -> pd.DataFrame:
    queryset = ThreadEvent.objects.prefetch_related('roles')

    data = [
        {'root': thread.timestamp.timestamp(),
         'responses': [
             response.timestamp.timestamp()
             for response in thread.roles.all()
         ]} for thread in queryset
    ]

    df = pd.DataFrame(data)

    df['mean-response'] = df['responses'].apply(
        lambda lst: sum(lst)/len(lst)
    )

    return df


def describe_data(data: pd.DataFrame):
    """
    central tendency, deviation
    locate central data with mean, median, mode
    :return:
    """
    data.describe()
    overall_mean = data['mean-time'].mean()
    median = data['mean-time'].median()
    mode = data['mean-time'].mode()
    std = data['mean-time'].std()
    # print('mode: ', mode)
    print(std)
    return


# prep = prepare_data()
# print(prep)
# describe_
# data(prep)
# print(prep.describe())
# print(prep['mean-time'].corr())
# print(prep['mean-time'].boxplot(by='mean-time', ))
# print(describe_data(prep))


"""
import eResponse
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = [{'root':thread.timestamp.timestamp(),}]
data = [{'root':thread.timestamp.timestamp(), 'responses':[response.timestamp.timestamp() for response in thread.roles.all()]} for thread in queryset]
data
import pandas as pd
df = pd.DataFrame(data)
df
1.681739**9
float('1.681739e+09')
float(1681738898.966287)
float( 1.681739e+09)
df.describe()
df['mean-response'] = df['responses'].apply(lambda lst: sum(lst)/len(lst))
df
df.describe()
float(1.681739e+09)
df['responses']
df[['responses']]
df[['mean-response', 'root']].groupby('mean-response').describe()
df[['mean-response', 'root']].groupby('mean-response').head()
df['root'].dtype
df['root].astype('float64').mean()
df['root'].astype('float64').mean()
1.681739e+09.astype('float64')
df
float(1.681739e+09)
df.info()
df.shape
tmp = df.append(df)
tmp = df.concat
tmp = df.concat([df, df], ignore_index=True, axis=1)
tmp = pd.concat([df, df], ignore_index=True, axis=1)
tmp
tmp.shape
tmp = tmp.drop_duplicates()
df.loc[df.astype(str).drop_duplicates().index]
tmp.loc[tmp.astype(str).drop_duplicates().index]
tmp = tmp.loc[tmp.astype(str).drop_duplicates().index]
tmp
df.columns
df.isnull()
df.isnull().sum()
thread = df['root']
thread
thread.head()
thread.describe()
thread.info()
thread.mean()
thread.std()
thread.value_counts()
df.corr()
%history
df.loc[df.astype(str).corr().index]
df[['root', 'mean-response']].corr()

How many complete information cycle was observed? -> compare with not completed, mean, median, mode

What is the minimum time to complete an eInfo cycle?
ratio lowest time: largest time
25% responses in under 2 seconds
tot num of threads/eInfo 

What is the minimum number of experts needed to resolve incident?
relative risk-> min_messages_per_thread = 20
if current thread has 25 what is the relative risk that thread is completed successfully?
Are there threads without responses? then do statistics.describe 
tot number of participating experts

Relationship between each thread/eInfo

d1 = [{f'rp{i}':r.timestamp.timestamp() for i, r in enumerate(thread.roles.all())} for thread in queryset]

df['mean-response'] = df.apply(lambda lst: sum(r-lst[0] for r in lst[1:])/(len(lst)-1), axis=1)

df[df.select_dtypes(np.float64).columns] = df.select_dtypes(np.float64).astype('float32')


def do_d2():
    ...:     lst = []
    ...:     for i, thread in enumerate(queryset):
    ...:         d = {}
    ...:         for j, role in enumerate(thread.roles.all()):
    ...:             if j == 0:
    ...:                 root = role.timestamp
    ...:                 continue
    ...:             else:
    ...:                 d[f'thread{j}'] = (role.timestamp-root).total_seconds()
    ...:         lst.append(d)
    ...:     return lst
    
    
    def do_table(dfg: pd.DataFrame):
     ...:     for i in range(dfg.shape[0]):
     ...:         for j in range(dfg.shape[1]):
     ...:             cell = dfg.iat[i, j]
     ...:             tle.cell(i, j).text = str(round(cell, 3))
     
     
     def do_data():
    ...:     lst = []
    ...:     for i, thd in enumerate(queryset):
    ...:         data = None
    ...:         for j, role in enumerate(thd.roles.all()):
    ...:             if j == 0:
    ...:                 root = role.timestamp
    ...:                 continue
    ...:             else:
    ...:                 data = {f'thread{k}': round((role.timestamp-root).total_seconds(), 3) for k, role in enumerate(queryset[1:], 1)}
    ...:                 break
    ...:         lst.append(data) if data is not None else {}
    ...:     return lst
    
    
    def do_data():
    ...:     lst = []
    ...:     for i, thd in enumerate(queryset):
    ...:         data = None
    ...:         if len(thd.roles.all()) > 1 and thd.id == thd.roles.first().id:
    ...:             for j, role in enumerate(thd.roles.all()):
    ...:                 if j == 0:
    ...:                     root = role.timestamp
    ...:                 else:
    ...:                     data = {f'thread{k}': round((rle.timestamp-root).total_seconds(), 3) for k,rle in enumerate(queryset[1:], start=1)}
    ...:                     break
    ...:         lst.append(data) if data is not None else {}
    ...:     return lst
    
    
 thread = ThreadEvent.objects.create(id=uuid.uuid4())
   ...:     time.sleep(60)
   ...:     thread.roles.add(Role.objects.create(id=uuid.uuid4())
   ...:     time.sleep(29)
   ...:     thread.roles.add(Role.objects.create(id=uuid.uuid4())
   ...:     time.sleep(13.9474723)
   ...:     thread.roles.add(Role.objects.create(id=uuid.uuid4())
   ...:     time.sleep(49.353621367)
   ...:     for k in range(7):
   ...:         thread.roles.add(Role.objects.create(id=uuid.uuid(4))
   ...:         time.sleep(3.464746353)


12 - 3

60s = 1m
603065.734s = x

10051.096min

60min = 1hr

167.518hr

24hr = 1


%matplotlib
import eResponse
import pandas as pd
import numpy as np
import docx
import matplotlib.pyplot as plt
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = {f'thread{i}':pd.Series([round((role.timestamp-thd.timestamp).total_seconds(), 3) for role in thd.roles.all()]) for i, thd in enumerate(queryset, start=1)}
trend = pd.DataFrame(data)
trend
trend = trend.dropna()
trend
'plot trend'
''' 
plot trend
>>> trend.plot(kind='hist', edgecolor='blue', bins=how to bin dataframe? by axis?)
From our trend histogram above, we can easily observe an ascent of trend line- signifying a longer thread event. 
This ascent gets steeper toward the right, which tells us that most events from mid february to march took at least 
274026.907 seconds (approximately 4 days) to complete events

display legend out of plot- legend obstructing plot
my matplotlib histogram taking too long Stall detected message, reduce number of variables? or reduce datapoints
'''



meeeeeeeeeee

%matplotlib
import eResponse
import pandas as pd
import numpy as np
import docx
import matplotlib.pyplot as plt
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = {f'thread{i}':pd.Series([round((role.timestamp-thd.timestamp).total_seconds(), 3) for role in thd.roles.all()]) for i, thd in enumerate(queryset, start=1)}
trend = pd.DataFrame(data)
trend
trend = trend.dropna()
trend
trend.range
trend.min()
trend.min(axis=1)
bins = []
trend.max()
trend.max(axis=1)
280775.543/80
280775.543//80
[v for v in range(3509, 280776, 3509)]
x = [v for v in range(3509, 280776, 3509)]
len(x)
trend.plot(kind='hist', bins=bins)
trend
bins
x
trend.plot(kind='hist', bins=x)
plt.close('all')
trend.plot(kind='hist', bins=x)
trend
trend.thread1
trend
trend.astype(int)
trend
trend.astype(int).plot(kind='hist')
trend.astype(int).plot(kind='hist', bins=x)
import seaborn
import seaborn as sns
trend.max(axis=1)
maxi = int(280775.543)
maxi
maxi+=1
maxi
trend['time_pot'] = pd.cut(trend, bins=list(range(0, maxi, 120)), right=False)
trend['time_pot'] = pd.cut(trend, bins=list(range(0, maxi, 120)), right=False)
trend.columns
trend['time_pot'] = pd.cut(trend, bins=x, right=False)
trend.columns
trend['time_pot'] = pd.cut(np.array(trend), bins=x, right=False)
trend
a = [1, 2, 9, 1, 5, 3]
b = [9, 8, 7, 8, 9, 1]

c = [a, b]

print(pd.cut(c, 3, labels=False))
r = pd.cut(c, 3, labels=False)
r
r = pd.cut(c, 3, labels=False)
df_list = [pd.DataFrame({'Values' : v, 'Labels' : l}) for v, l in zip(c, r)]
trend['time_pot'] = pd.apply(pd.cut(trend, bins=list(range(0, maxi, 120)), right=False))
trend['time_pot'] = trend.apply(pd.cut(trend, bins=list(range(0, maxi, 120)), right=False))
trend['time_pot'] = trend.apply(pd.cut, bins=list(range(0, maxi, 120)))
trend['time_pot'] = trend.apply(pd.cut, bins=list(range(0, maxi, 120)), axis=1)
trend['time_pot'] = trend.apply(pd.cut, bins=x)
x
len(x)
trend['time_pot'] = trend.apply(pd.cut, bins=list(range(0, maxi, 120)))
trend['time_pot'] = trend.apply(pd.cut, bins=list(range(0, maxi, 120)))
"""


def create_thread():
    thread = ThreadEvent.objects.create(id=uuid.uuid4())
    time.sleep(17.889878)
    thread.roles.add(Role.objects.create(id=uuid.uuid4()))
    time.sleep(13.98663376)
    thread.roles.add(Role.objects.create(id=uuid.uuid4()))
    time.sleep(7.9474723)
    thread.roles.add(Role.objects.create(id=uuid.uuid4()))
    time.sleep(9.353621367)
    for k in range(7):
        thread.roles.add(Role.objects.create(id=uuid.uuid4()))
        time.sleep(4.464746353)

    return


def create_role():
    # threads = ThreadEvent.objects.prefetch_related('roles').order_by('-timestamp')[10:]
    # threads = ThreadEvent.objects.prefetch_related('roles')
    threads = ThreadEvent.objects.annotate(
        count_roles=Count('roles')
    ).filter(count_roles__lt=80).prefetch_related('roles')

    for thread in threads:
        for _ in range(10):
            t = random.randrange(1, 13)
            thread.roles.add(Role.objects.create(id=uuid.uuid4()))
            time.sleep(t)

    return


"""
%matplotlib
import eResponse
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
import numpy as np
import docx
import matplotlib.pyplot as plt
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = {f'thread{i}':pd.Series([round((role.timestamp-thd.timestamp).total_seconds(), 3) for role in thd.roles.all()]) for i, thd in enumerate(queryset, start=1)}
trend = pd.DataFrame(data)
trend = trend.dropna()
groupdf = pd.DataFrame()
groupdf['Group Min.'] = trend.min(axis=1)
groupdf['Group Avg.'] = trend.apply(lambda row: round(np.mean(row), 3), axis=1)
def percentile(row):
    global ple
    rank_index = int(ple*len(sorted(row)))+1
    return row[rank_index]
ple = .25
groupdf['Group Q1'] = trend.apply(percentile, axis=1)
ple = .5
groupdf['Group Q2'] = trend.apply(percentile, axis=1)
ple = .75
groupdf['Group Q3'] = trend.apply(percentile, axis=1)
groupdf
groupdf['Group Max.'] = trend.max(axis=1)
groupdf['Group Tot.'] = trend.apply(np.sum, axis=1)
xz = pd.cut(trend.to_numpy().flatten(), np.percentile(trend, [v for v in range(0, 105, 5)]))
xz
trend.groupby(pd.cut(trend.to_numpy().flatten(), np.percentile(trend, [v for v in range(0, 105, 5)])))
new = pd.DataFrame({'responses': trend.to_numpy().flatten()})
new
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)])))
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)]))).val
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)]))).count()
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)]))).count().plot(kind='hist')
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)]))).count().plot(kind='bar')
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)]))).count().plot(kind='area')
plt.close('all')
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 125, 25)]))).count().plot(kind='area')
new.groupby(pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 125, 25)]))).count().plot(kind='hist')
new
bz = pd.cut(new['responses'], np.percentile(new['responses'], [v for v in range(0, 105, 5)]))
plt.hist(new, bins=bz)
new.plot(kind='hist', color='blue', edgecolor='black', bins=33)
plt.close('all')
new.plot(kind='hist', color='blue', edgecolor='black', bins=33)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
from matplotlib.ticker import PercentFormatter
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel('seconds')
plt.xlabel('Time of Arrival (s)')
plt.title('Historical trend of Responses')
new.plot(kind='line', color='blue', edgecolor='black', bins=33)
new.plot(kind='line', color='blue', bins=33)
new.plot(kind='line', color='blue')
xz
pd.DataFrame(np.array([[1,2], [3,4]]))
pd.DataFrame(np.array([[1,2], [3,4]])).to_numpy().flatten()
new
new = pd.DataFrame({'responses': trend.to_numpy().flatten('F')})
new
new.plot(kind='line', color='blue')
plt.close('all')
new.plot(kind='line', color='blue')
new.plot(kind='hist', color='blue')
new = pd.DataFrame({'responses': trend.to_numpy().flatten()})
new.plot(kind='hist', color='blue')
plt.close('all')
new.plot(kind='hist', color='blue')
plt.close('all')
new.plot(kind='bar', color='blue')
new = pd.DataFrame({'responses': trend.to_numpy().flatten()})
new
new.min()
np.percentile(range(new.min(), new.max()), [5, 10, 15, 20, 25, ])
min(new)
min(new['responses'])
np.percentile(range(min(new['responses']), max(new['responses'])), [5, 10, 15, 20, 25, ])
np.percentile(range(min(new['responses'].astype(int)), max(new['responses'].astype(int))), [5, 10, 15, 20, 25, ])
new
np.percentile(range(min(new['responses'].astype(int)), max(new['responses'].astype(int))), [v for v in range(0, 105, 5)])
cv = np.percentile(range(min(new['responses'].astype(int)), max(new['responses'].astype(int))), [v for v in range(0, 105, 5)])
len(cv)
len(cv) == len(set(cv))
from scipy import stats
cv
new
stats(new, 60)
stats.percentileofscore(new, 60)
stats.percentileofscore(new, 272730.309)
stats.percentileofscore(new.to_numpy().flatten(), 60)
stats.percentileofscore(new.to_numpy().flatten(), 272730.309)
stats.percentileofscore(new.to_numpy().flatten(), 272730.309, nan_policy='raise')
def get_percentile():
    d = {k:0 for k in range(0, 105, 5)}
    new = new.astype(int).to_numpy().flatten()
    for v in new:
        p = stats.percentileofscore(new, v, nan_policy='raise', kind='rank')
        for k in d:
            if p > k:
                continue
            else:
                d[k] += 1
                break
    return d
get_percentile()
def get_percentile(df):
    d = {k:0 for k in range(0, 105, 5)}
    new = df.astype(int).to_numpy().flatten()
    for v in new:
        p = stats.percentileofscore(new, v, nan_policy='raise', kind='rank')
        for k in d:
            if p > k:
                continue
            else:
                d[k] += 1
                break
    return d
get_percentile(new)
sum(get_percentile(new).values())
percentiles = [v for v in range(0, 105, 5)]
count = get_percentile(new).values()
count
plt.bar(percentiles, count)
plt.close('all')
plt.bar(percentiles, count)
help(plt.hist)
plt.hist(percentiles, count)
plt.bar(percentiles, count, align='center')
plt.xlabel('Time pot rates (%)')
plt.ylabel('Count')
plt.barh(percentile, count, align='center')
plt.barh(percentile, count)
plt.barh(count, percentile)
plt.bar(percentiles, count, align='center', width='0.1')
plt.bar(percentiles, count, align='center', width='0.9')
plt.bar(percentiles, count, align='center', width=0.9)
plt.bar(percentiles, count, align='center', width=2.9)
plt.bar(percentiles, count, align='center', width=2.7)
plt.title('Response-percentile count')
plt.close('all')

"""


"""
%matplotlib
import eResponse
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
import numpy as np
import docx
import matplotlib.pyplot as plt
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = {f'thread{i}':pd.Series([round((role.timestamp-thd.timestamp).total_seconds(), 3) for role in thd.roles.all()]) for i, thd in enumerate(queryset, start=1)}
trend = pd.DataFrame(data)
time_count = pd.DataFrame()
time_count['Time Aggregate'] = trend.apply(np.sum)
time_count
time_count['Time Aggregate'] = time_count['Time Aggregate'].astype(int)
time_count
time_count['Count'] = trend.apply(lambda col: np.count_nonzero(~np.isnan(col)))
fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()
time_count['Time Aggregate'].plot(kind='bar', ax=ax, color='blue', width=0.4, position=1)
time_count['Count'].plot(kind='bar', ax=ax2, color='red', width=0.4, position=0)
ax.legend()
ax2.legend()
ax.legend(loc='upper center')
ax2.legend(loc='upper center')
ax2.legend(loc='lower center')
ax2.legend(loc='center')
ax2.legend(loc=0)
plt.close('all')
time_count['Count'].plot(kind='bar', ax=ax2, color='green', width=0.4, position=0)
plt.show()

"""



"""
%matplotlib
import eResponse
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
import numpy as np
import docx
import matplotlib.pyplot as plt
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = {f'thread{i}':pd.Series([round((role.timestamp-thd.timestamp).total_seconds(), 3) for role in thd.roles.all()]) for i, thd in enumerate(queryset, start=1)}
trend = pd.DataFrame(data)
trend
df = pd.DataFrame([a,b,c,d], columns=["A", "B", "C", "D", "E"])
a = [3,4, 15, 10, 12]
b =
b = [2,13,4,19,1]
c = [12,3,7,8,4]
d = [12, 13,4,7,14]
df = pd.DataFrame([a,b,c,d], columns=["A", "B", "C", "D", "E"])
df
df.to_numpy().flatten()
df.to_numpy().flatten('f')
np.percentile(cut['responses'], [v for v in range(0, 105, 5)])
df
np.percentile(cut['responses']]]
groupdf = pd.DataFrame()
groupdf['Group Avg.'] = trend.apply(lambda row: round(np.mean(row), 3), axis=1)
def percentile(row):
    global ple
    rank_index = int(ple*len(sorted(row)))+1
    return row[rank_index]
groupdf['Group Avg.'] = trend.apply(lambda row: round(np.mean(row), 3), axis=1)
groupdf
groupdf['Group Min.'] = trend.min(axis=1)
groupdf
len(trend)
np.percentile(trend)
np.percentile(trend, 50)
np.percentile(trend, 50, axis=1)
np.nanpercentile(trend, 50)
np.nanpercentile(trend, 50, axis=1)
len(np.nanpercentile(trend, 50, axis=1))
groupdf
round(np.nanpercentile(trend, 25, axis=1), 3)
b = np.nanpercentile(trend, 25, axis=1)
b
pd.DataFrame(b)
groupdf['Group Q1'] = pd.DataFrame(np.nanpercentile(trend, 25, axis=1)).apply(lambda row: round(row, 3))
groupdf



.
|-- LICENSE
|-- README.md
|-- eResponse
|   |-- __init__.py
|   |-- asgi.py
|   |-- celery.py
|   |-- event
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- models.py
|   |   |-- pubsub.py
|   |   |-- tasks.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- manage.py
|-- requirements.txt
|-- scripts
|   |-- __init__.py
|   `-- script.py
|-- setup.py
|-- static
"""

"""
import pandas as pd
from eResponse.event.models import *
queryset = ThreadEvent.objects.prefetch_related('roles')
data = {
    f'thread{i}':pd.Series([round((role.timestamp-thd.timestamp).total_seconds(), 3)
                            for role in thd.roles.all()]) 
    for i, thd in enumerate(queryset, start=1)
}
df = pd.DataFrame(data)
cleaned_df = df.dropna()
cleaned_df.describe().T
cleaned_df.describe()
pd.set_option('display.float_format', lambda x: '%.5f' % x)
cleaned_df.describe()
pd.set_option('display.float_format', lambda x: '%.3f' % x)
cleaned_df.describe()
cleaned_df.thread1.head(80)
cleaned_df
cleaned_df.transpose()
cleaned_df.apply(pd.DataFrame.describe, axis=1)
cleaned_df
trend = cleaned_df.apply(pd.DataFrame.describe, axis=1)
trend.count
trend.count()
trend['count']
trend[['min', 'mean']].plott(kind='area')
trend[['min', 'mean']].plot(kind='area')
%matplotlib
import eResponse
import numpy as np
import docx
import matplotlib.pyplot as plt
trend[['min', 'mean']].plot(kind='area')
trend[['std', 'mean']].plot(kind='area')
trend[['25%', 'mean']].plot(kind='area')
trend[['50%', 'mean']].plot(kind='area')
trend[['75%', 'mean']].plot(kind='area')
trend = cleaned_df.apply(pd.DataFrame.describe, percentiles=[], axis=1)
trend
trend = cleaned_df.apply(pd.DataFrame.describe, percentiles=[.25,], axis=1)
trend
trend = cleaned_df.apply(pd.DataFrame.describe, percentiles=[.25, .5,], axis=1)
trend
trend = cleaned_df.apply(pd.DataFrame.describe, percentiles=[.05, .25, .5,], axis=1)
trend
trend = cleaned_df.apply(pd.DataFrame.describe, percentiles=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], axis=1)
trend
trend = cleaned_df.apply(pd.DataFrame.describe, percentiles=[0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], axis=1)
trend
trend[['5%', 'mean']].plot(kind='area')
trend.plot(kind='area', subplots=[('min', 'mean'),('5%', 'mean'),('15%', 'mean'),('25%', 'mean'),('35%', 'mean')])
plt.close('all')
trend.plot(kind='area', subplots=[('min', 'mean'),('5%', '10%')])
trend.plot(kind='area', subplots=[('min', 'mean'),('5%', '10%')])
cleaned_df
desc_df = cleaned_df.apply(pd.DataFrame.describe, percentiles=[0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], axis=1)
desc_df
desc.plot(kind='area', subplots=[('min', 'mean'),('5%', '10%')])
desc_df.plot(kind='area', subplots=[('min', 'mean'),('5%', '10%')])
desc_df
desc_df.plot(kind='area', subplots=[('min', 'mean'),('5%', '15%')])
plt.close('all')
desc_df.plot(kind='area', subplots=[('min', 'mean'),('5%', '15%')])
desc_df.plot(kind='line', subplots=[('min', 'mean'),('5%', '15%')])
desc_df.plot(kind='line', subplots=[])
desc_df.plot(kind='line', subplots=[('min', 'mean')])
plt.close('all')
desc_df.plot(kind='line', subplots=[('min', 'mean')])
desc_df.columns
desc_df[['5%', '15%', '25%', '35%']].plot(kind='line', subplots=True)
plt.close('all')
"""






