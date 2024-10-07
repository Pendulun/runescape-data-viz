import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA

import streamlit as st
import warnings


def arima_model_decorator(order: tuple):

    def fit_and_predict(data, start: int, end: int):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ARIMA(data, order=order, trend='ct')
            model_fit = model.fit()
            yhat = model_fit.predict(start, end)
            return yhat

    return fit_and_predict


def auto_reg_decorator(lags: int = 1):

    def fit_and_predict(data, start: int, end: int):
        model = AutoReg(data, lags=lags)
        model_fit = model.fit()
        yhat = model_fit.predict(start, end)
        return yhat

    return fit_and_predict


def get_test_preds_and_error(X_train: pd.DataFrame, Y_test: pd.DataFrame,
                             n: int, model_func):
    """
    Train the model on the X_train and return the error on Y_test
    """
    test_pred_start = len(X_train)
    test_pred_end = test_pred_start + n - 1
    test_preds = model_func(X_train, test_pred_start, test_pred_end)
    test_error = root_mean_squared_error(Y_test, test_preds)
    return test_preds, test_error


def get_future_preds(data: pd.DataFrame, forward_days: int, model_func):
    """
    Train the model and return the future predictions
    data: The train data
    forward_days: Num of days to pred
    model_func: The model func
    """
    future_pred_start = len(data)
    future_pred_end = future_pred_start + forward_days
    future_preds = model_func(data, future_pred_start, future_pred_end)
    return future_preds


def cross_validate(models: dict[str, dict], X: pd.DataFrame, val_size: int):
    """
    Return the cross validation scores for all models
    models: dict of models info
    X: training data
    val_size: Validation set size 
    """
    n_splits = 5
    cross_val_scores = dict()
    for model_name, model_info in models.items():
        # Cross Validation
        model_best_config_rmse = None
        for param in model_info['params']:
            model_func = model_info['decorator'](**param)

            tscv = TimeSeriesSplit(n_splits=n_splits, test_size=val_size)
            folds_errors = np.array(range(n_splits))
            for fold_idx, (train_index,
                           test_index) in enumerate(tscv.split(X)):
                pred_start = len(train_index)
                pred_end = pred_start + val_size - 1
                yhat = model_func(X.iloc[train_index], pred_start, pred_end)
                fold_preds = np.array(yhat)
                fold_val = np.array(X.iloc[test_index])
                rmse_error = root_mean_squared_error(fold_val, fold_preds)
                folds_errors[fold_idx] = rmse_error

            mean_rmse = np.mean(folds_errors)
            if model_best_config_rmse is None or mean_rmse < model_best_config_rmse:
                model_best_config_rmse = mean_rmse
                model_results = {'rmse': mean_rmse, 'param': param}
                cross_val_scores[model_name] = model_results
    return cross_val_scores


def get_best_model_and_params(models: dict[str, dict], ts_data: pd.DataFrame,
                              n: int, forward_days: int):
    cross_val_scores = cross_validate(models, ts_data[:-n], forward_days)

    best_model_dict = dict()
    best_model_name = None
    min_rmse = None
    for model_name, model_results in cross_val_scores.items():
        if min_rmse is None or model_results['rmse'] < min_rmse:
            min_rmse = model_results['rmse']
            best_model_dict = model_results
            best_model_name = model_name

    #Search best model
    best_model_func = None
    for model_name, model_info in models.items():
        if model_name == best_model_name:
            best_model_func = model_info['decorator'](
                **best_model_dict['param'])

    return best_model_func, best_model_name, best_model_dict['param']


def augment_with_predictions(
        data: pd.DataFrame, models_to_use: list[str],
        forward_days: int) -> tuple[pd.DataFrame, str, dict]:
    data.set_index("date", drop=True, inplace=True)
    data.index = pd.DatetimeIndex(pd.to_datetime(data.index,
                                                 format="%Y-%m-%d"),
                                  freq='infer')
    models = dict()
    for model in models_to_use:
        if model == "ARIMA":
            params = list()
            ps = [28, 21, 14, 7]
            params = [{'order': (p, 0, 7) for p in ps if p >= forward_days}]
            arima_dict = {'decorator': arima_model_decorator, 'params': params}
            models['ARIMA'] = arima_dict
        elif model == 'AutoRegression':
            params = list()
            ps = [28, 21, 14, 7]
            params = [{'lags': p for p in ps if p >= forward_days}]
            auto_reg_dict = {'decorator': auto_reg_decorator, 'params': params}
            models['AutoRegression'] = auto_reg_dict

    if len(models) > 0:
        n = forward_days
        best_model_func, best_model_name, best_model_params = get_best_model_and_params(
            models, data['daily'], n, forward_days)

        test_preds, test_error = get_test_preds_and_error(
            data[:-n]['daily'], data[-n:]['daily'], n, best_model_func)

        future_preds = get_future_preds(data['daily'], forward_days,
                                        best_model_func)
        # st.write("FUTURE")
        # st.write(future_preds)
        future_data_range = pd.date_range(
            start=data.index[-1] + datetime.timedelta(days=1),
            end=data.index[-1] + datetime.timedelta(days=forward_days + 1),
            freq='1D').to_list()

        future_df = pd.DataFrame(future_preds.to_list(),
                                 columns=['future_price'],
                                 index=future_data_range)
        future_df['daily'] = None
        future_df['30 day average'] = None
        future_df['Test Pred'] = None
        # st.write("FUTURE PREDS:")
        # st.write(future_df)
        data['Test Pred'] = None
        data['Test Pred'][-n:] = test_preds
        data['future_price'] = None
        data = pd.concat([data, future_df], axis='rows')

        data = data.astype({
            'daily': float,
            '30 day average': float,
            'Test Pred': float,
            'future_price': float
        })
        # st.write(data.tail(10))
    else:
        best_model_name = None
        best_model_params = {}
        test_error = None

    return data, best_model_name, best_model_params, test_error
