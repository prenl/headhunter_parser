import pandas as pd


def sort(dataframe, column: str, ascending: bool) -> pd.DataFrame:
    return dataframe.sort_values(by=column, ascending=ascending).reset_index(drop=True)


def get_min(dataframe, column: str) -> pd.DataFrame:
    return pd.DataFrame(sort(dataframe, column, ascending=True).reset_index(drop=True).iloc[0])


def get_max(dataframe, column: str) -> pd.DataFrame:
    i = 0
    l = list(sort(dataframe, column, ascending=False)[column])
    while l[i] == None:
        i += 1
    return pd.DataFrame(sort(dataframe, column, ascending=False).iloc[i]).reset_index(drop=True)


def get_average(dataframe, column: str):
    salary_list = []
    for i in dataframe[column]:
        try:
            salary_list.append(int(i))
        except Exception:
            continue
    return sum(salary_list) / len(salary_list)


def leave_only_row(dataframe: pd.DataFrame, column, value):
    delete_list = list(i for i in range(len(dataframe[column])) if dataframe[column][i] != value)
    return dataframe.drop(delete_list).reset_index(drop=True)
