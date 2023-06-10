import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

from eResponse.event.models import ThreadEvent


def prepare_data() -> pd.DataFrame:
    queryset = ThreadEvent.objects.prefetch_related('roles')

    data = [
        {'threadId': thread.id,
         'responses': [
             (thread.timestamp.timestamp(),
              response.timestamp.timestamp())
             for response in thread.roles.all()
         ]} for thread in queryset
    ]

    df = pd.DataFrame(data)

    def clean_responses(lst: list[tuple]) -> list:
        return [(round(sent, 3), round(response, 3))
                for sent, response in lst]

    def get_time_lapse(lst: list[tuple]) -> list:
        return [response-sent for sent, response in lst]

    def clean_time_lapse(lst: list) -> list:
        return [round(v, 3) for v in lst]

    df['responses'] = df['responses'].apply(clean_responses)
    df['time-lapse'] = df['responses'].apply(get_time_lapse)
    df['time-lapse'] = df['time-lapse'].apply(clean_time_lapse)
    df['mean-time'] = df['time-lapse'].apply(
        lambda lst: sum(lst)/len(lst)  # mean-time per row
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


prep = prepare_data()
print(prep)
# describe_
# data(prep)
# print(prep.describe())
# print(prep['mean-time'].corr())
# print(prep['mean-time'].boxplot(by='mean-time', ))
# print(describe_data(prep))
