"""
@brief      test log(time=28s)
"""


import sys
import os
import unittest
import datetime


try:
    import src
    import pyquickhelper as skip_
    import pymyinstall as skip__
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
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pymyinstall",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import src
    import pyquickhelper as skip_
    import pymyinstall as skip__

from pyquickhelper.loghelper import fLOG
from src.pyensae.datasource.data_velib import DataVelibCollect


class TestDataVelibOffline (unittest.TestCase):

    def test_data_velib_contract(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        fold = os.path.abspath(os.path.split(__file__)[0])
        data = os.path.join(fold, "data")

        df = DataVelibCollect.to_df(data)
        # fLOG(df.head())
        assert len(df) > 0

        stations = df[["name", "lat", "lng"]]
        gr = stations.groupby(["name", "lat", "lng"], as_index=False).sum()
        # fLOG(gr.head())
        assert len(gr) >= 30

        df.to_csv(os.path.join(fold, "out_data.txt"), sep="\t", index=False)
        dt = datetime.datetime(2014, 5, 22, 11, 49, 27, 523164)
        sub = df[df["collect_date"] == dt]
        fig, ax, plt = DataVelibCollect.draw(sub)

    def test_data_velib_animation(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        fold = os.path.abspath(os.path.split(__file__)[0])
        data = os.path.join(fold, "data")

        if "travis" in sys.executable:
            return

        from pymyinstall.installhelper.install_cmd_helper import is_conda_distribution
        if is_conda_distribution():
            # not tested on anaconda
            return

        df = DataVelibCollect.to_df(data)
        DataVelibCollect.js_animation(df)


if __name__ == "__main__":
    unittest.main()
