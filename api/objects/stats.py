from ..Utils.exceptions import StatsError
from ..objects.categories import Category
from ..db.controller import query_db, ControllerError
from datetime import date, timedelta
from typing import List, Tuple
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import io
from base64 import b64encode
import urllib


class Stats(object):
    def __init__(self, df: pd.DataFrame = None):
        self.df = None
        if df is not None:
            self.df = df

    def _get_category_sums_data(self) -> List[Tuple[date, str, float]]:
        sql = """
        SELECT DISTINCT(tr.t_date), ca.name, SUM(tr.amount) AS "Sum" FROM "TRANSACTIONS" tr
        JOIN "CATEGORIES" ca ON ca.id = tr.category_id
        GROUP BY tr.t_date, ca.name
        ORDER BY
            tr.t_date ASC,
            "Sum" DESC;
        """
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return results

    def create_bytes(self):
        fig = plt.figure()
        sns.set_style(style='darkgrid')
        plt.style.use("dark_background")
        axes = fig.gca()

        if self.df is None:
            raise StatsError(
                "No DataFrame assigned! Run method first to generate one.")
        sns.lineplot(data=self.df, x="Date", y="Sum", hue="Category")
        plt.setp(axes.get_xticklabels(), rotation=45,
                 ha="right", rotation_mode="anchor")
        axes.set_title("Daily sums per categoriy")
        plt.tight_layout()

        buf = io.BytesIO()
        try:
            plt.savefig(buf, format="png")
        except Exception as err:
            raise StatsError(
                "Error when trying to save plot into buffer!") from err
        buf.seek(0)
        return buf

    def _get_all_categories(self) -> List[Category]:
        sql = """
            SELECT * FROM "CATEGORIES";
        """
        try:
            categories = [Category(item) for item in query_db(sql)]
        except ControllerError as err:
            raise StatsError(
                "Something went wring when querying the database!") from err
        return categories

    def get_category_sums(self):
        data = self._get_category_sums_data()
        cols = [category.name for category in self._get_all_categories()]
        df = pd.DataFrame(data, columns=["Date", "Category", "Sum"])
        df = pd.pivot_table(df, index=["Date", "Category"], values="Sum")
        # df.pivot_table(index=dates, columns=cols, values=values, fill_value=0)
        # df.pivot_table(index=df["Date"].unique(), columns=cols, values=values, fill_value=0)
        print(df)
        self.df = df


if __name__ == '__main__':
    stats = Stats()
    stats.get_category_sums()
