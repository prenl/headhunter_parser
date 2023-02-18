import pandas as pd


def sort(dataframe, column: str) -> pd.DataFrame:
    return dataframe.sort_values(by=column, ascending=True).reset_index(drop=True)


def get_min(dataframe, column: str) -> pd.DataFrame:
    return pd.DataFrame(sort(dataframe, column).iloc[0]).reset_index(drop=True)


def get_max(dataframe, column: str) -> pd.DataFrame:
    i = -1
    l = list(sort(dataframe, column)[column])
    while l[i] == "Unspecified":
        i -= 1
    return pd.DataFrame(sort(dataframe, column).iloc[i]).reset_index(drop=True)


def get_average(dataframe, column: str) -> float:
    salary_list = list(int(i) for i in dataframe[column] if i!="Unspecified")
    return sum(salary_list) / len(salary_list)


def leave_only_row(dataframe: pd.DataFrame, column, value):
    delete_list = list(i for i in range(len(dataframe[column])) if dataframe[column][i] != value)
    return dataframe.drop(delete_list).reset_index(drop=True)
