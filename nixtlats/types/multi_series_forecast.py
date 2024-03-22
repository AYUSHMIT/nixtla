# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .multi_series_forecast_fewshot_loss import MultiSeriesForecastFewshotLoss
from .multi_series_forecast_finetune_loss import MultiSeriesForecastFinetuneLoss
from .multi_series_forecast_model import MultiSeriesForecastModel
from .multi_series_input import MultiSeriesInput


class MultiSeriesForecast(pydantic.BaseModel):
    model: typing.Optional[MultiSeriesForecastModel] = pydantic.Field(
        description="Model to use as a string. Options are: `short-horizon`, and `long-horizon.` We recommend using `long-horizon` for forecasting if you want to predict more than one seasonal period given the frequency of your data."
    )
    freq: typing.Optional[str] = pydantic.Field(
        description="The frequency of the data represented as a string. 'D' for daily, 'M' for monthly, 'H' for hourly, and 'W' for weekly frequencies are available."
    )
    level: typing.Optional[typing.List[typing.Any]] = pydantic.Field(
        description="A list of values representing the prediction intervals. Each value is a percentage that indicates the level of certainty for the corresponding prediction interval. For example, [80, 90] defines 80% and 90% prediction intervals."
    )
    fh: typing.Optional[int] = pydantic.Field(
        description="The forecasting horizon. This represents the number of time steps into the future that the forecast should predict."
    )
    y: typing.Optional[typing.Any]
    x: typing.Optional[MultiSeriesInput] = pydantic.Field(
        description='The exogenous  variables provided as a dictionary of two colums: columns and data. The columns contains the columns of the dataframe and data contains eaach data point. For example: {"columns": ["unique_id", "ds", "ex_1", "ex_2"], "data": [["ts_0", "2021-01-01", 0.2, 0.67], ["ts_0", "2021-01-02", 0.4, 0.7]}. This should also include forecasting horizon (fh) additional timestamps for each unique_id to calculate the future values.'
    )
    clean_ex_first: typing.Optional[bool] = pydantic.Field(
        description="A boolean flag that indicates whether the API should preprocess (clean) the exogenous signal before applying the large time model. If True, the exogenous signal is cleaned; if False, the exogenous variables are applied after the large time model."
    )
    fewshot_steps: typing.Optional[int] = pydantic.Field(
        description="The number of tuning steps used to train the large time model on the data. Set this value to 0 for zero-shot inference, i.e., to make predictions without any further model tuning."
    )
    fewshot_loss: typing.Optional[MultiSeriesForecastFewshotLoss] = pydantic.Field(
        description="The loss used to train the large time model on the data. Select from ['default', 'mae', 'mse', 'rmse', 'mape', 'smape']. It will only be used if finetune_steps larger than 0. Default is a robust loss function that is less sensitive to outliers."
    )
    finetune_steps: typing.Optional[int] = pydantic.Field(description="Deprecated. Please use fewshot_steps instead.")
    finetune_loss: typing.Optional[MultiSeriesForecastFinetuneLoss] = pydantic.Field(
        description="Deprecated. Please use fewshot_loss instead."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
