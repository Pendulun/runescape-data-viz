import numpy as np
import pandas as pd
from sktime.split import temporal_train_test_split
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.fbprophet import Prophet
from sktime.forecasting.arima import ARIMA, AutoARIMA
from sktime.forecasting.compose import TransformedTargetForecaster, MultiplexForecaster
from sktime.transformations.series.detrend import Deseasonalizer
from sktime.performance_metrics.forecasting import mean_squared_error
from sktime.forecasting.model_selection import ForecastingGridSearchCV
from sktime.split import ExpandingWindowSplitter
import warnings


def augment_with_predictions(
        data: pd.DataFrame, models_to_use: list[str],
        forward_days: int) -> tuple[pd.DataFrame, str, dict]:
    if len(models_to_use) > 0:
        Y_train, Y_test = temporal_train_test_split(data['daily'],
                                                    test_size=forward_days)
        fh = ForecastingHorizon(Y_test.index, is_relative=False)
        forecasters = list()
        param_grid = dict()
        if 'ARIMA' in models_to_use:
            forecasters.append(
                ("ARIMA",
                 TransformedTargetForecaster([
                     ("deseasonalize", Deseasonalizer(model="additive", sp=7)),
                     ("forecast", ARIMA(seasonal_order=(0, 0, 0, 0))),
                 ])))
            param_grid["ARIMA__order"] = [(i, 0, i)
                                          for i in range(forward_days, 30)
                                          if i % 7 == 0 or i == 1]
            param_grid.setdefault('selected_forecaster',
                                  list()).append('ARIMA')

        if "AutoARIMA" in models_to_use:
            forecasters.append(
                ("AutoARIMA",
                 TransformedTargetForecaster([
                     ("deseasonalize", Deseasonalizer(model="additive", sp=7)),
                     ("forecast", AutoARIMA()),
                 ])))
            param_grid.setdefault('selected_forecaster',
                                  list()).append("AutoARIMA")

        if "Prophet" in models_to_use:
            forecasters.append(
                ("Prophet",
                 TransformedTargetForecaster([
                     ("deseasonalize", Deseasonalizer(model="additive", sp=7)),
                     ("forecast", Prophet()),
                 ])))
            param_grid.setdefault('selected_forecaster',
                                  list()).append("Prophet")

        forecaster = MultiplexForecaster(forecasters=forecasters)

        cv = ExpandingWindowSplitter(initial_window=105,
                                     fh=list(range(forward_days)),
                                     step_length=forward_days)

        gscv = ForecastingGridSearchCV(forecaster,
                                       strategy="refit",
                                       cv=cv,
                                       param_grid=param_grid)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            gscv.fit(Y_train)

        test_preds = gscv.predict(fh)
        test_error = np.sqrt(mean_squared_error(Y_test, test_preds))

        best_model = gscv.best_forecaster_
        best_model_name = gscv.best_params_['selected_forecaster']
        best_model_params = gscv.best_params_
        del best_model_params['selected_forecaster']

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            best_model.fit(data['daily'])
        fh = ForecastingHorizon(list(range(1, forward_days + 1)),
                                is_relative=True)
        future_preds = best_model.predict(fh)
        future_preds = pd.DataFrame(future_preds)
        future_preds.rename({'daily': 'future_price'},
                            inplace=True,
                            axis='columns')

        future_preds['daily'] = None
        future_preds['30 day average'] = None
        future_preds['Test Pred'] = None

        data['Test Pred'] = None
        data.loc[test_preds.index, 'Test Pred'] = test_preds
        data['future_price'] = None
        data = pd.concat([data, future_preds], axis='rows')

        data = data.astype({
            'daily': float,
            '30 day average': float,
            'Test Pred': float,
            'future_price': float
        })
    else:
        best_model_name = None
        best_model_params = {}
        test_error = None

    return data, best_model_name, best_model_params, test_error
