# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class MultiSeriesForecastFewshotLoss(str, enum.Enum):
    """
    The loss used to train the large time model on the data. Select from ['default', 'mae', 'mse', 'rmse', 'mape', 'smape']. It will only be used if finetune_steps larger than 0. Default is a robust loss function that is less sensitive to outliers.
    """

    DEFAULT = "default"
    MAE = "mae"
    MSE = "mse"
    RMSE = "rmse"
    MAPE = "mape"
    SMAPE = "smape"

    def visit(
        self,
        default: typing.Callable[[], T_Result],
        mae: typing.Callable[[], T_Result],
        mse: typing.Callable[[], T_Result],
        rmse: typing.Callable[[], T_Result],
        mape: typing.Callable[[], T_Result],
        smape: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is MultiSeriesForecastFewshotLoss.DEFAULT:
            return default()
        if self is MultiSeriesForecastFewshotLoss.MAE:
            return mae()
        if self is MultiSeriesForecastFewshotLoss.MSE:
            return mse()
        if self is MultiSeriesForecastFewshotLoss.RMSE:
            return rmse()
        if self is MultiSeriesForecastFewshotLoss.MAPE:
            return mape()
        if self is MultiSeriesForecastFewshotLoss.SMAPE:
            return smape()
