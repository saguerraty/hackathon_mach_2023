import pandas as pd
from datetime import date, timedelta


def classify(value, amount_quantiles_dict):
    i = 1
    for quantile, amount in amount_quantiles_dict.items():
        if value <= amount:
            return f"c{i}"
        i += 1
    return f"c{i}"


def get_stats_in_time_window(df, start_date, end_date):
    df_agg = pd.pivot_table(
        df[(df["fecha"] >= str(start_date)) & (df["fecha"] <= str(end_date))],
        index="user_id",
        values="amount",
        columns="tipo",
        aggfunc="sum",
    ).reset_index()
    df_agg["CARGO/ABONO"] = round(100*abs(df_agg["CARGO"] / df_agg["ABONO"]), 2)
    return df_agg


def get_user_cluster_stats(df_train, df_test, user_id, delta_time=30, end_date=date(2022, 12, 31)):
    start_date = end_date - timedelta(days=delta_time)

    df_train_agg = get_stats_in_time_window(df_train, start_date, end_date)
    df_user_agg = get_stats_in_time_window(
        df_test[df_test["user_id"] == user_id], start_date, end_date
    )

    quantiles = [0.25, 0.5, 0.75, 0.9]
    amount_quantiles_dict = df_train_agg["ABONO"].quantile(quantiles).to_dict()

    df_train_agg["cluster"] = df_train_agg["ABONO"].apply(
        lambda x: classify(x, amount_quantiles_dict)
    )
    df_user_agg["cluster"] = df_user_agg["ABONO"].apply(
        lambda x: classify(x, amount_quantiles_dict)
    )

    user_dict = df_user_agg.to_dict(orient="records")[0]
    cluster_median = df_train_agg[df_train_agg["cluster"] == user_dict["cluster"]]["CARGO/ABONO"].median()
    user_dict["cluster_CARGO/ABONO"] = cluster_median
    gap_median = 100*(cluster_median - user_dict["CARGO/ABONO"])/cluster_median
    user_dict["gap_CARGO/ABONO"] = round(gap_median, 2)
    return user_dict


if __name__ == "__main__":
    df_train = pd.read_csv("data_files/ingresos_egresos_train.csv") 
    df_test = pd.read_csv("data_files/ingresos_egresos_test.csv")
    user_id = 202
    end_date = date.today()
    user_dict = get_user_cluster_stats(df_train, df_test, user_id, 30, end_date)
