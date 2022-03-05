from datetime import date, timedelta
from typing import List, Tuple
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

from ..Utils.exceptions import StatsError
from ..objects.categories import Category
from ..db.controller import query_db, ControllerError


class Stats(object):
    def __init__(self, df: pd.DataFrame = None):
        self.df = None
        if df is not None:
            self.df = df

    def _get_category_sums_per_date(self) -> List[Tuple[date, str, float]]:
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

    def _get_all_categories(self) -> List[Category]:
        sql = """
            SELECT * FROM "CATEGORIES";
        """
        try:
            categories = [Category(item) for item in query_db(sql)]
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return categories

    def _get_category_sums(self):
        sql = """
            SELECT DISTINCT(cat.name), SUM(tra.amount) AS "sum" FROM "TRANSACTIONS" tra
            JOIN "CATEGORIES" cat ON cat.id = tra.category_id
            GROUP BY cat.name;
        """
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err

        return results

    def create_bytes_categories(self, plot: str):
        # Initiate plot figure
        fig, axes = plt.subplots()
        plt.style.use("dark_background")
        sns.set_style('darkgrid')

        if self.df is None:
            raise StatsError(
                "No DataFrame assigned! Run method first to generate one.")

        # Check plot type & settings
        if plot == "line":
            sns.lineplot(data=self.df, x="Date", y="Sum", hue="Category")
            axes.set_title("Daily sums per category")
            plt.setp(axes.get_xticklabels(), rotation=45,
                     ha="right", rotation_mode="anchor")
        elif plot == "pie":
            colors = plt.get_cmap('Blues')(
                np.linspace(0.25, 0.95, len(self.df["Sum"])))
            labels = list(self.df["Category"])
            axes.pie(x=self.df["Sum"], colors=colors, labels=labels, textprops={"color": "black"}, labeldistance=1.15,
                     radius=4, center=(7, 7), frame=True, wedgeprops={"linewidth": 1.5, "edgecolor": "white"})
            axes.set_title("Sums per category")
        else:
            raise StatsError(
                "No valid entry for 'plot' argument: '{}'".format(plot))

        plt.tight_layout()

        # Create and save into bytes buffer.
        buf = io.BytesIO()
        try:
            plt.savefig(buf, format="png")
        except Exception as err:
            raise StatsError(
                "Error when trying to save plot into buffer!") from err
        buf.seek(0)

        return buf

    def get_category_sums_per_date(self):
        data = self._get_category_sums_per_date()
        df = pd.DataFrame(data, columns=["Date", "Category", "Sum"])
        df = pd.pivot_table(df, index=["Date", "Category"], values="Sum")
        print(df)
        self.df = df

    def get_category_sums(self):
        data = self._get_category_sums()
        df = pd.DataFrame(data, columns=["Category", "Sum"])
        self.df = df
        self.df.sort_values("Category", inplace=True)
        print(df)


if __name__ == '__main__':
    stats = Stats()
    stats.get_category_sums()
