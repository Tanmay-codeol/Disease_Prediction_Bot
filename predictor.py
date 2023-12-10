import pandas as pd
import numpy as np
import pickle

with open("./classifire.pkl", "rb") as file:
    classifire = pickle.load(file, errors="ignore")

with open("./regressor.pkl", "rb") as file:
    regressor = pickle.load(file, errors="ignore")

df = pd.read_csv('./disease_symptoms_weight.csv').iloc[:, 1:]
df.set_index('Disease', inplace=True)

dis_df = pd.read_csv('./data.csv', index_col='disease')


def predict(data: list):

    lst = pd.DataFrame(data).transpose()
    col = df.iloc[:, :-1].columns.tolist()
    lst.columns = col

    clf_proba = classifire.predict_proba(lst)
    top_n_category_predictions = np.argsort(clf_proba)[:, :-41:-1]
    order = list(top_n_category_predictions[0])[:5]

    dis_series = pd.Series(dis_df.index)
    order = dis_series.loc[order].values.tolist()

    pred_nor_mean = regressor.predict(lst)[0]

    ll = pred_nor_mean-0.1
    ul = pred_nor_mean+0.1

    filt2 = ((df['normalised_mean'] > ll) & (df['normalised_mean'] < ul))
    reg_proba = df.loc[filt2, ["normalised_mean"]].groupby(
        "Disease").agg("mean").sort_values("normalised_mean")

    reg_proba = reg_proba.columns.tolist()

    for i in order:
        if i in reg_proba:
            return i

    return order[0]


if __name__ == "__main__":

    n = 450

    t1 = df.iloc[n, :-1]

    print(dis_df.loc[t1.name].name)

    t1 = pd.DataFrame(t1)
    t1 = t1.transpose()

    lst = t1.iloc[0].to_list()

    s = predict(lst)
    print(s)
