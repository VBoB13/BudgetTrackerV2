from datetime import date, timedelta
from calendar import monthrange
from traceback import print_tb
from typing import List, Tuple
from decimal import Decimal
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

from ..Utils.exceptions import StatsError
from ..objects.categories import Category
from ..db.controller import query_db, ControllerError

from ..Utils import START_DAY, TODAY, ONE_MONTH_AGO, ONE_MONTH_AHEAD, ONE_DAY


class Stats(object):
    def __init__(self, df: pd.DataFrame = None):
        self.df = None
        if df is not None:
            self.df = df

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
            SELECT DISTINCT(cat.name), SUM(case when tra.currency='USD' then
                tra.amount*(
                    SELECT rate FROM "EXCHANGE_RATES"
                    WHERE r_date <= tra.t_date
                    ORDER BY r_date DESC
                    LIMIT 1) else
                tra.amount END)::numeric(8,2) AS "sum"
            FROM "TRANSACTIONS" tra
            JOIN "CATEGORIES" cat ON cat.id = tra.category_id
            WHERE t_date < '{}' AND t_date > '{}'
            GROUP BY cat.name
            UNION ALL
                SELECT 'Remaining', SUM(amount)-(SELECT SUM(amount) FROM "TRANSACTIONS" WHERE t_date < '{}' AND t_date > '{}') FROM "INCOMES"
                WHERE i_date < '{}' AND i_date > '{}'
            ;
        """.format(
            TODAY.strftime("%Y-%m-%d"), START_DAY.strftime("%Y-%m-%d"),
            TODAY.strftime("%Y-%m-%d"), START_DAY.strftime("%Y-%m-%d"),
            TODAY.strftime("%Y-%m-%d"), START_DAY.strftime("%Y-%m-%d"))
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err

        return results

    def _get_category_sums_per_date(self) -> List[Tuple[date, str, float]]:
        sql = """
        SELECT DISTINCT(tr.t_date), ca.name, SUM(tr.amount) AS "Sum" FROM "TRANSACTIONS" tr
        JOIN "CATEGORIES" ca ON ca.id = tr.category_id
        WHERE t_date > '{}' AND t_date < '{}' AND ca.id != 2
        GROUP BY tr.t_date, ca.name
        ORDER BY
            tr.t_date ASC,
            "Sum" DESC;
        """.format(ONE_MONTH_AGO.strftime("%Y-%m-%d"), TODAY.strftime("%Y-%m-%d"))
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return results

    def _get_income(self, daily_avg=False) -> int:
        if daily_avg:
            sql = """
                SELECT ROUND(SUM(amount)/{}, 2) FROM "INCOMES" TOP2;
            """.format(monthrange(TODAY.year, TODAY.month)[1])
        else:
            sql = """
                SELECT SUM(amount) FROM "INCOMES";
            """
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return results[0][0]

    def _get_rent_util_avg(self) -> int:
        sql = """
            SELECT ROUND(SUM(amount)/30, 2) FROM "TRANSACTIONS"
            WHERE category_id=2 AND t_date > '{}';
        """.format(ONE_MONTH_AGO.strftime("%Y-%m-%d"))

        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return results[0][0]

    def _get_meal_avgs(self) -> List[Tuple[str, float]]:
        sql = """
        SELECT tra.comment AS "Meal", CAST(tra.amount AS real) AS "Amount" FROM "TRANSACTIONS" tra
        WHERE tra.category_id=1 AND tra.comment in ('Breakfast', 'Lunch', 'Dinner')
        ORDER BY "Amount";
        """
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return results

    def create_bytes_categories(self, plot: str) -> io.BytesIO:
        # Initiate plot figure
        fig, axes = plt.subplots()
        plt.style.use("seaborn-dark-palette")
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
                np.linspace(0.15, 1, len(self.df["Sum"])))
            labels = list(self.df["Category"])
            axes.pie(x=self.df["Sum"], colors=colors, labels=labels, textprops={"color": "black"}, labeldistance=1.0,
                     radius=4, center=(7, 7), frame=True, wedgeprops={"linewidth": 1, "edgecolor": "white"})
            axes.set_title("Sums per category")
        elif plot == "bar":
            axes = sns.barplot(x="Meal", y="Amount",
                               data=self.df)
            axes.set_title("Sums per category")
            axes.bar_label(
                axes.containers[0], labels=self.df["Meal"].unique(), label_type='center', )
            self.show_values_on_bars(axes)
        else:
            raise StatsError(
                "Not valid entry for 'plot' argument: '{}'".format(plot))

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
        income_daily_avg = self._get_income(daily_avg=True)
        rent_util_avg = self._get_rent_util_avg()
        first_date = data[0][0]
        current_date = first_date
        date_list = []
        while current_date <= TODAY:
            date_list.append(current_date + ONE_DAY)
            current_date += ONE_DAY
        try:
            for date_obj in date_list:
                data.append((date_obj, "Income", income_daily_avg))
                data.append((date_obj, "Rent & Utilities", rent_util_avg))
        except Exception as err:
            print(err)
            print_tb(err.__traceback__)

        df = pd.DataFrame(
            data, columns=["Date", "Category", "Sum"])
        df = pd.pivot_table(
            df, index=["Date", "Category"], values="Sum", fill_value=0)
        print(df)
        self.df = df

    def get_category_sums(self):
        data = self._get_category_sums()
        df = pd.DataFrame(data, columns=["Category", "Sum"])
        self.df = df
        self.df.sort_values("Category", inplace=True)
        print(df)

    def get_meal_avgs(self):
        data = self._get_meal_avgs()
        self.df = pd.DataFrame(data, columns=["Meal", "Amount"])
        self.df.info(verbose=True)
        print(self.df)

    def show_values_on_bars(self, axs):
        def _show_on_single_plot(ax):
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = '{:.2f}'.format(p.get_height())
                ax.text(_x, _y, value, ha="center")

        if isinstance(axs, np.ndarray):
            for idx, ax in np.ndenumerate(axs):
                _show_on_single_plot(ax)
        else:
            _show_on_single_plot(axs)


if __name__ == '__main__':
    stats = Stats()
    stats.get_category_sums_per_date()
