import unittest
import pandas as pd
import numpy  as np

class TestDebug(unittest.TestCase):
    def test_pandas_max(self):
        print(f"Pandas version: {pd.__version__}")
        print(f"Numpy version: {np.__version__}")
        df = pd.DataFrame([{
            "Longueur": 1000,
            "Images": 2
        }])
        print(df)
        print(df.dtypes)
        m = df["Longueur"].max()
        print(f"Max: {m}")
        self.assertEqual(m, 1000)
