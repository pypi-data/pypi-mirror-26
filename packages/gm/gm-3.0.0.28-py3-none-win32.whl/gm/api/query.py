# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

from gm.constant import DATA_TYPE_TICK
from gm.model.fundamental import FundamentalApi
from gm.model.history import HistoryApi
from gm.utils import load_to_datetime_str

fundamentalapi = FundamentalApi()
historyapi = HistoryApi()


def get_fundamentals(table, symbols, start_date, end_date, fields=None, filter=None, order_by=None, limit=1000):
    """
    查询基本面财务数据
    """
    return fundamentalapi.get_fundamentals(table=table, symbols=symbols,
                                           start_date=start_date,
                                           end_date=end_date, fields=fields,
                                           filter=filter, order_by=order_by,
                                           limit=limit)


def get_fundamentals_n(table, symbols, end_date, fields=None, filter=None, order_by=None, count=1):
    """
    查询基本面财务数据,每个股票在end_date的前n条
    """
    return fundamentalapi.get_fundamentals_n(table=table, symbols=symbols,
                                             end_date=end_date, fields=fields,
                                             filter=filter, order_by=order_by,
                                             count=count)


def get_instruments(symbols=None, exchanges=None, sec_types=None, names=None, skip_suspended=True, skip_st=True, fields=None):
    """
    查询最新交易标的信息,有基本数据及最新日频数据
    """
    return fundamentalapi.get_instruments(symbols, exchanges, sec_types, names, skip_suspended, skip_st, fields)


def get_history_instruments(symbols, fields=None, start_date=None, end_date=None):
    """
    返回指定的symbols的标的日指标数据
    """
    return fundamentalapi.get_history_instruments(symbols, fields, start_date, end_date)


def get_instrumentinfos(symbols=None, exchanges=None, sec_types=None, names=None, fields=None):
    """
    查询交易标的基本信息
    如果没有数据的话,返回空列表. 有的话, 返回list[dict]这样的列表. 其中 listed_date, delisted_date 为 datetime 类型
    @:param fields: 可以是 'symbol, sec_type' 这样的字符串, 也可以是 ['symbol', 'sec_type'] 这样的字符list
    """
    return fundamentalapi.get_instrumentinfos(symbols, exchanges, sec_types, names, fields)


def get_constituents(index, fields=None):
    """
    查询指数最新成分股
    返回的list每项是个字典,包含的key值有:
    symbol 股票symbol
    weight 权重
    """
    return fundamentalapi.get_constituents(index, fields)


def get_history_constituents(index, start_date=None, end_date=None):
    """
    查询指数历史成分股
    返回的list每项是个字典,包含的key值有:
    trade_date: 交易日期(datetime类型)
    constituents: 一个字典. 每个股票的sybol做为key值, weight做为value值
    """
    return fundamentalapi.get_history_constituents(index, start_date, end_date)


def get_sector(code):
    """
    查询板块股票列表
    """
    return fundamentalapi.get_sector(code)


def get_industry(code):
    """
    查询行业股票列表
    """
    return fundamentalapi.get_industry(code)


def get_concept(code):
    """
    查询概念股票列表
    """

    return fundamentalapi.get_concept(code)


def get_trading_dates(exchange, start_date, end_date):
    """
    查询交易日列表
    如果指定的市场不存在, 返回空列表. 有值的话,返回 yyyy-mm-dd 格式的列表
    """
    return fundamentalapi.get_trading_dates(exchange, start_date, end_date)


def get_previous_trading_date(exchange, date):
    """
    返回指定日期的上一个交易日
    @:param exchange: 交易市场
    @:param date: 指定日期, 可以是datetime.date 或者 datetime.datetime 类型. 或者是 yyyy-mm-dd 或 yyyymmdd 格式的字符串
    @:return 返回下一交易日, 为 yyyy-mm-dd 格式的字符串, 如果不存在则返回None
    """
    return fundamentalapi.get_previous_trading_date(exchange, date)


def get_next_trading_date(exchange, date):
    """
    返回指定日期的下一个交易日
    @:param exchange: 交易市场
    @:param date: 指定日期, 可以是datetime.date 或者 datetime.datetime 类型. 或者是 yyyy-mm-dd 或 yyyymmdd 格式的字符串
    @:return 返回下一交易日, 为 yyyy-mm-dd 格式的字符串, 如果不存在则返回None
    """
    return fundamentalapi.get_next_trading_date(exchange, date)


def get_dividend(symbol, start_date, end_date=None):
    """
    查询分红送配
    """
    return fundamentalapi.get_dividend(symbol, start_date, end_date)


def get_continuous_contracts(csymbol, start_date=None, end_date=None):
    """
    获取连续合约
    """
    return fundamentalapi.get_continuous_contracts(csymbol, start_date, end_date)


# todo 改成rest api接口提高效率
def history(symbol, frequency, start_time, end_time, fields=None, skip_suspended=True, fill_missing=None, adjust=None, df=False):
    """
    查询历史行情
    """
    start_time = load_to_datetime_str(start_time)
    end_time = load_to_datetime_str(end_time)

    if frequency == DATA_TYPE_TICK:
        return historyapi.get_history_ticks(symbols=symbol, start_time=start_time, end_time=end_time, fields=fields,
                                            skip_suspended=skip_suspended, fill_missing=fill_missing, adjust=adjust, df=df)

    else:
        return historyapi.get_history_bars(symbols=symbol, frequency=frequency, start_time=start_time, end_time=end_time, fields=fields,
                                           skip_suspended=skip_suspended, fill_missing=fill_missing, adjust=adjust, df=df)


# todo 改成rest api接口提高效率
def history_n(symbol, frequency, count, end_time=None, fields=None, skip_suspended=True, fill_missing=None, adjust=None, df=False):
    """
    查询历史行情
    """
    end_time = load_to_datetime_str(end_time)

    if frequency == DATA_TYPE_TICK:
        return historyapi.get_history_n_ticks(symbol=symbol, count=count, end_time=end_time, fields=fields,
                                              skip_suspended=skip_suspended, fill_missing=fill_missing, adjust=adjust, df=df)

    else:
        return historyapi.get_history_n_bars(symbol=symbol, frequency=frequency, count=count, end_time=end_time, fields=fields,
                                             skip_suspended=skip_suspended, fill_missing=fill_missing, adjust=adjust, df=df)

