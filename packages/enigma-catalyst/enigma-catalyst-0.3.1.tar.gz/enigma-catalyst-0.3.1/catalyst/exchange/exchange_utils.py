import json
import os
import pickle
import urllib
from datetime import date, datetime

import pandas as pd

from catalyst.exchange.exchange_errors import ExchangeAuthNotFound, \
    ExchangeSymbolsNotFound
from catalyst.utils.paths import data_root, ensure_directory, \
    last_modified_time

SYMBOLS_URL = 'https://s3.amazonaws.com/enigmaco/catalyst-exchanges/' \
              '{exchange}/symbols.json'


def get_exchange_folder(exchange_name, environ=None):
    if not environ:
        environ = os.environ

    root = data_root(environ)
    exchange_folder = os.path.join(root, 'exchanges', exchange_name)
    ensure_directory(exchange_folder)

    return exchange_folder


def get_exchange_symbols_filename(exchange_name, environ=None):
    exchange_folder = get_exchange_folder(exchange_name, environ)
    return os.path.join(exchange_folder, 'symbols.json')


def download_exchange_symbols(exchange_name, environ=None):
    filename = get_exchange_symbols_filename(exchange_name)
    url = SYMBOLS_URL.format(exchange=exchange_name)
    response = urllib.urlretrieve(url=url, filename=filename)
    return response


def get_exchange_symbols(exchange_name, environ=None):
    filename = get_exchange_symbols_filename(exchange_name)

    if not os.path.isfile(filename) or \
            pd.Timedelta(pd.Timestamp('now', tz='UTC') - last_modified_time(filename)).days > 1:
        download_exchange_symbols(exchange_name, environ)

    if os.path.isfile(filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            return data
    else:
        raise ExchangeSymbolsNotFound(
            exchange=exchange_name,
            filename=filename
        )


def get_exchange_auth(exchange_name, environ=None):
    exchange_folder = get_exchange_folder(exchange_name, environ)
    filename = os.path.join(exchange_folder, 'auth.json')

    if os.path.isfile(filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            return data
    else:
        data = dict(name=exchange_name, key='', secret='')
        with open(filename, 'w') as f:
            json.dump(data, f, sort_keys=False, indent=2, separators=(',', ':'))
            return data

def get_algo_folder(algo_name, environ=None):
    if not environ:
        environ = os.environ

    root = data_root(environ)
    algo_folder = os.path.join(root, 'live_algos', algo_name)
    ensure_directory(algo_folder)

    return algo_folder


def get_algo_object(algo_name, key, environ=None, rel_path=None):
    if algo_name is None:
        return None

    folder = get_algo_folder(algo_name, environ)

    if rel_path is not None:
        folder = os.path.join(folder, rel_path)

    filename = os.path.join(folder, key + '.p')

    if os.path.isfile(filename):
        try:
            with open(filename, 'rb') as handle:
                return pickle.load(handle)
        except Exception as e:
            return None
    else:
        return None


def save_algo_object(algo_name, key, obj, environ=None, rel_path=None):
    folder = get_algo_folder(algo_name, environ)

    if rel_path is not None:
        folder = os.path.join(folder, rel_path)
        ensure_directory(folder)

    filename = os.path.join(folder, key + '.p')

    with open(filename, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def append_algo_object(algo_name, key, obj, environ=None):
    algo_folder = get_algo_folder(algo_name, environ)
    filename = os.path.join(algo_folder, key + '.p')

    mode = 'a+b' if os.path.isfile(filename) else 'wb'
    with open(filename, mode) as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_algo_df(algo_name, key, environ=None, rel_path=None):
    folder = get_algo_folder(algo_name, environ)

    if rel_path is not None:
        folder = os.path.join(folder, rel_path)

    filename = os.path.join(folder, key + '.csv')

    if os.path.isfile(filename):
        try:
            with open(filename, 'rb') as handle:
                return pd.read_csv(handle, index_col=0, parse_dates=True)
        except IOError:
            return pd.DataFrame()
    else:
        return pd.DataFrame()


def save_algo_df(algo_name, key, df, environ=None, rel_path=None):
    folder = get_algo_folder(algo_name, environ)

    if rel_path is not None:
        folder = os.path.join(folder, rel_path)
        ensure_directory(folder)

    filename = os.path.join(folder, key + '.csv')

    with open(filename, 'wb') as handle:
        df.to_csv(handle)


def get_exchange_minute_writer_root(exchange_name, environ=None):
    exchange_folder = get_exchange_folder(exchange_name, environ)

    minute_data_folder = os.path.join(exchange_folder, 'minute_data')
    ensure_directory(minute_data_folder)

    return minute_data_folder

def get_exchange_bundles_folder(exchange_name, environ=None):
    exchange_folder = get_exchange_folder(exchange_name, environ)

    temp_bundles = os.path.join(exchange_folder, 'temp_bundles')
    ensure_directory(temp_bundles)

    return temp_bundles


def perf_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
