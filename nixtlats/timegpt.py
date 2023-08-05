# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/timegpt.ipynb.

# %% auto 0
__all__ = ['TimeGPT']

# %% ../nbs/timegpt.ipynb 5
import json
import requests
from typing import Dict, List, Optional

import pandas as pd

# %% ../nbs/timegpt.ipynb 7
class TimeGPT:
    """
    A class used to interact with the TimeGPT API.
    """

    def __init__(self, token: str, api_url: str):
        """
        Constructs all the necessary attributes for the TimeGPT object.

        Parameters
        ----------
        token : str
            The authorization token to interact with the TimeGPT API.
        api_url : str
            The base URL for the TimeGPT API.
        """
        self.token = token
        self.api_url = api_url
        self.weights_x: pd.DataFrame = None

    @property
    def request_headers(self):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
        }
        return headers

    def _parse_response(self, response: str) -> Dict:
        """Parses responde."""
        try:
            resp = json.loads(response)
        except Exception as e:
            raise Exception(response)
        return resp

    def _input_size(self, freq: str):
        response_input_size = requests.post(
            f"{self.api_url}/timegpt_input_size",
            json={"freq": freq},
            headers=self.request_headers,
        )
        response_input_size = self._parse_response(response_input_size.text)
        return response_input_size["data"]

    def _preprocess_inputs(
        self,
        df: pd.DataFrame,
        h: int,
        freq: str,
        X_df: Optional[pd.DataFrame] = None,
    ):
        input_size = self._input_size(freq)
        y_cols = ["unique_id", "ds", "y"]
        y = df[y_cols].groupby("unique_id").tail(input_size + h)
        y = y.to_dict(orient="split", index=False)
        x_cols = df.drop(columns=y_cols).columns.to_list()
        if len(x_cols) == 0:
            x = None
        else:
            x = pd.concat(
                [
                    df[["unique_id", "ds"] + x_cols]
                    .groupby("unique_id")
                    .tail(input_size + h),
                    X_df,
                ]
            )
            x = x.sort_values(["unique_id", "ds"])
            x = x.to_dict(orient="split", index=False)
        return y, x, x_cols

    def _multi_series(
        self,
        df: pd.DataFrame,
        h: int,
        freq: str,
        X_df: Optional[pd.DataFrame] = None,
        level: Optional[List[int]] = None,
        finetune_steps: int = 0,
        clean_ex_first: bool = True,
    ):
        y, x, x_cols = self._preprocess_inputs(df=df, h=h, freq=freq, X_df=X_df)
        payload = dict(
            y=y,
            x=x,
            fh=h,
            freq=freq,
            level=level,
            finetune_steps=finetune_steps,
            clean_ex_first=clean_ex_first,
        )
        response_timegpt = requests.post(
            f"{self.api_url}/timegpt_multi_series",
            json=payload,
            headers=self.request_headers,
        )
        response_timegpt = self._parse_response(response_timegpt.text)
        if "weights_x" in response_timegpt["data"]:
            self.weights_x = pd.DataFrame(
                {
                    "features": x_cols,
                    "weights": response_timegpt["data"]["weights_x"],
                }
            )
        return pd.DataFrame(**response_timegpt["data"]["forecast"])

    def forecast(
        self,
        df: pd.DataFrame,
        h: int,
        freq: str,
        X_df: Optional[pd.DataFrame] = None,
        level: Optional[List[int]] = None,
        finetune_steps: int = 0,
        clean_ex_first: bool = True,
    ):
        """Forecast your time series using TimeGPT.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame with columns [`unique_id`, `ds`, `y`] and exogenous.
        h : int
            Forecast horizon.
        freq : str
            Frequency of the data.
            See [pandas' available frequencies](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).
        X_df : pandas.DataFrame, optional (default=None)
            DataFrame with [`unique_id`, `ds`] columns and `df`'s future exogenous.
        level : List[float], optional (default=None)
            Confidence levels between 0 and 100 for prediction intervals.
        finetune_steps : int (default=0)
            Number of steps used to finetune TimeGPT in the
            new data.
        clean_ex_first : bool (default=True)
            Clean exogenous signal before making forecasts
            using TimeGPT.

        Returns
        -------
        fcsts_df : pandas.DataFrame
            DataFrame with TimeGPT forecasts for point predictions and probabilistic
            predictions (if level is not None).
        """
        return self._multi_series(
            df=df,
            h=h,
            freq=freq,
            X_df=X_df,
            level=level,
            finetune_steps=finetune_steps,
            clean_ex_first=clean_ex_first,
        )
