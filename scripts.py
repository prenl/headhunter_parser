import pandas as pd


def sort(dataframe, column: str, ascending: bool) -> pd.DataFrame:
    if column == "experience_years" or column == "experience_months":
        new_dataframe = pd.DataFrame(dataframe)
        new_dataframe['experience_months'] += new_dataframe['experience_years'] * 12
        new_dataframe['experience_years'] = 0
        return new_dataframe.sort_values(by='experience_months', ascending=ascending).reset_index(drop=True)
    else:
        return dataframe.sort_values(by=column, ascending=ascending).reset_index(drop=True)


def get_min(dataframe, column: str) -> pd.DataFrame:
    return pd.DataFrame(sort(dataframe, column, ascending=True).reset_index(drop=True).iloc[0])


def get_max(dataframe, column: str):
    sorted_dataframe = pd.DataFrame(
        sort(dataframe, column, ascending=True).reset_index(drop=True))
    for i in range(1, len(sorted_dataframe[column])):
        try:
            int(sorted_dataframe[column][i])
        except Exception:
            try:
                return pd.DataFrame(sorted_dataframe.iloc[i - 1])
            except Exception:
                return None
    return pd.DataFrame(sort(dataframe, column, ascending=False).reset_index(drop=True).iloc[0])


def get_average(dataframe, column: str):
    salary_list = []
    for i in dataframe[column]:
        try:
            salary_list.append(int(i))
        except Exception:
            continue
    try:
        return str(int(sum(salary_list) / len(salary_list))) + " KZT"
    except ZeroDivisionError:
        return "None"


def leave_only_row(dataframe: pd.DataFrame, column, value):
    delete_list = list(i for i in range(
        len(dataframe[column])) if dataframe[column][i] != value)
    return dataframe.drop(delete_list).reset_index(drop=True)


def get_salary_stats(group):
    group = group['salary']
    min_salary = group.min()
    max_salary = group.max()
    mean_salary = group.mean()

    stats = pd.concat([min_salary, max_salary, mean_salary], axis=1)
    stats.columns = ['min', 'max', 'average']

    return stats


def get_age_stats(group):
    group = group['age']
    min_age = group.min()
    max_age = group.max()
    mean_age = group.mean()

    stats = pd.concat([min_age, max_age, mean_age], axis=1)
    stats.columns = ['min', 'max', 'average']

    return stats
