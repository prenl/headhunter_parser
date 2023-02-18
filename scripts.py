import pandas as pd

def sort(dataframe, column: str) -> pd.DataFrame:
    return dataframe.sort_values(by=column, ascending=True)

def get_min(dataframe, column: str) -> pd.DataFrame:
    return pd.DataFrame(sort(dataframe, column).iloc[0])

def get_max(dataframe, column: str) -> pd.DataFrame:
    i = -1
    l = list(sort(dataframe, column)[column])
    while l[i] == "Unspecified":
        i -= 1
    return pd.DataFrame(sort(dataframe, column).iloc[i])

def get_average(dataframe, column: str) -> float:
    salary_list = list(int(i) for i in dataframe[column] if i!="Unspecified")
    return sum(salary_list) / len(salary_list)

