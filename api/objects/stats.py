import pandas as pd

from ..db.controller import query_db, ControllerError
from ..Utils.exceptions import StatsError


class Stats(object):
    def _get_category_sums_data(self):
        sql = """
        SELECT DISTINCT(tr.t_date), ca.name, SUM(tr.amount) AS "Avg" FROM "TRANSACTIONS" tr
        JOIN "CATEGORIES" ca ON ca.id = tr.category_id
        GROUP BY tr.t_date, ca.name
        ORDER BY
            tr.t_date ASC,
            "Avg" DESC;
        """
        try:
            results = query_db(sql)
        except ControllerError as err:
            raise StatsError(
                "Something went wrong when querying the database!") from err
        return results

    def get_category_sums(self):
        data = self._get_category_sums_data()
        df = pd.DataFrame(data, columns=["Date", "Category", "Sum(NTD)"])
        return df[df["Category"] == "Food"]


if __name__ == '__main__':
    stats = Stats()
    stats.get_category_sums()
