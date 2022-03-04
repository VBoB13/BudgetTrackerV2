from pprint import pprint
import pandas as pd

from typing import List, Tuple
from datetime import date, timedelta

from ..db.controller import query_db, ControllerError
from ..objects.categories import Category
from ..Utils.exceptions import StatsError


class Stats(object):
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
        return df


if __name__ == '__main__':
    stats = Stats()
    stats.get_category_sums()
