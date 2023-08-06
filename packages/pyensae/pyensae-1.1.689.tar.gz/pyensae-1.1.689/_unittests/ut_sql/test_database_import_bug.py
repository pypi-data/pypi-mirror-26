"""
@brief      test log(time=1s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""


import sys
import os
import unittest


try:
    import src
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import src
    import pyquickhelper as skip_

from pyquickhelper.loghelper import fLOG
from src.pyensae.sql.database_helper import import_flatfile_into_database
from src.pyensae.sql.database_main import Database
from src.pyensae.sql.database_core2 import NoHeaderException


class TestDatabaseImportSql(unittest.TestCase):

    def test_sqllite_sql(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        file = os.path.join(
            os.path.abspath(
                os.path.split(__file__)[0]),
            "data",
            "taxi_trip.csv")
        dbf = os.path.join(
            os.path.abspath(
                os.path.split(__file__)[0]),
            "temp_taxi.db3")
        if os.path.exists(dbf):
            os.remove(dbf)
        try:
            import_flatfile_into_database(
                dbf,
                file,
                fLOG=fLOG,
                header=True)
        except NoHeaderException:
            return

        assert os.path.exists(dbf)
        db = Database(dbf, LOG=fLOG)
        db.connect()
        view = db.execute_view("SELECT * FROM taxi_trip")
        fLOG(len(view))
        fLOG(view)
        exp = ('1B5C0970F2AE8CFFBA8AE4584BEAED29', 'D961332334524990D1BBD462E2EFB8A4',
               'CMT', '2013-02-08 23:35:14', 'CRD', 6.0, 0.5, 0.5, 0.0, 0, 7.0)
        assert len(view) > 0
        assert len(view[0]) == len(exp)


if __name__ == "__main__":
    unittest.main()
