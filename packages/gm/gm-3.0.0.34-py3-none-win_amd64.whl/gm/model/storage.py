# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import datetime

from gm.constant import SUB_TAG, CSDK_OPERATE_SUCCESS
from gm.csdk.c_sdk import gmi_now, py_gmi_get_cash, py_gmi_get_positions, \
    py_gmi_get_accounts, py_gmi_get_account_connections
from gm.model.account import Account
from gm.pb.account_pb2 import Positions, Cashes, AccountConnections
from gm.pb.strategy_service_pb2 import GetAccountsRsp
from gm.pb.trade_pb2 import GetCashReq, GetPositionsReq
from gm.pb.tradegw_service_pb2 import GetAccountConnectionsReq
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import load_to_list, ObjectLikeDict


class DefaultFileModule(object):
    def on_tick(self, context, tick):
        print('请初始化on_tick方法')

    def on_bar(self, context, bar):
        print('请初始化on_bar方法')

    def on_bod(self, context, bod):
        print('请初始化on_bod方法')

    def on_eod(self, context, eod):
        print('请初始化on_eod方法')


class Context(object):
    __instance = None

    def __new__(cls, *args, **kwd):
        if Context.__instance is None:
            Context.__instance = object.__new__(cls, *args, **kwd)
            cls.strategy_id = ''
            cls.inside_file_module = DefaultFileModule()
            cls.token = None

        return Context.__instance

    def inside_init(self):
        self._bar_subs = []
        self._bar_tasks = []
        self.inside_tick_subs = set()
        self.inside_schedules = {}
        self.inside_accounts = {}
        self.inside_parameters = {}

    def inside_unsubscribe_all(self):
        self.inside_init()
        from gm.model.storage_data import SubBarData
        SubBarData().inside_init()

    def __init__(self):
        self._bar_subs = []
        self._bar_tasks = []
        self.inside_tick_subs = set()
        self.inside_schedules = {}
        self.inside_accounts = {}
        self.inside_parameters = {}

    @property
    def now(self):
        '''
        返回一个时间字符串
        '''
        now = gmi_now()
        return datetime.datetime.fromtimestamp(now)

    def inside_append_bar_sub(self, sub):
        if not sub.unique:
            return
        # 添加sub
        self._bar_subs.append(sub)
        # 添加任务
        self._append_bar_task(sub)
        # contextdata 添加相关类实例
        from gm.model.storage_data import SubBarData
        SubBarData().sub_data(sub.sub_tag, sub.count)

    def inside_remove_bar_sub(self, sub):
        # 移除sub
        self._bar_subs.remove(sub)
        # 取消任务
        self._remove_bar_task(sub)
        # contextdata 去掉相关类实例
        from gm.model.storage_data import SubBarData
        SubBarData().unsub_data(sub.sub_tag)

    @property
    def symbols(self):
        """
        bar 的symbols + tick 的symbols
        """
        return set([sub.symbol for sub in self.inside_bar_subs]).union(self.inside_tick_subs)

    @property
    def accounts(self):
        """
        用户资金 & 持仓情况
        """
        if not self.inside_accounts:
            self._set_accounts()

        return self.inside_accounts

    def account(self, account_id=''):
        accounts = self.accounts
        # 只有一个账户 且未有account_id 的情况下返回唯一用户
        if not account_id and len(accounts) == 1:
            default_id = sorted(accounts.keys())[0]
            return accounts.get(default_id)

        return accounts.get(account_id)

    @property
    def parameters(self):
        """
        动态参数
        """
        if not self.inside_parameters:
            self._set_parameters()

        return self.inside_parameters

    @property
    def inside_bar_subs(self):
        return self._bar_subs

    @property
    def inside_bar_tasks(self):
        return self._bar_tasks

    def _set_accounts(self):
        status, data = py_gmi_get_accounts()
        if not status == CSDK_OPERATE_SUCCESS:
            return

        accounts_info = GetAccountsRsp()
        accounts_info.ParseFromString(data)
        account_infos = protobuf_to_dict(accounts_info)
        account_ids = account_infos['account_ids']

        for account_id in account_ids:
            self._get_account_info(account_id)

    @staticmethod
    def data(symbol, frequency, count=1, fields='close'):
        fields = load_to_list(fields)
        from gm.model.storage_data import SubBarData
        return SubBarData().get_data(symbol, frequency, count, fields)

    def _append_bar_task(self, sub):
        # 如果不是wait_group的直接当成一个单独的任务就行
        if not sub.wait_group:
            self._bar_tasks.append(BarTask(symbols=[sub.symbol], frequency=sub.frequency, wait_group=False, wait_group_timeout=sub.wait_group_timeout))
            return

        # 如果没有该频率的task，构建一个， 有的话， 对这个task成员进行添加
        if sub.frequency not in [task.frequency for task in self.inside_bar_tasks if task.wait_group == True]:
            self._bar_tasks.append(BarTask(symbols=[sub.symbol], frequency=sub.frequency, wait_group=True, wait_group_timeout=sub.wait_group_timeout))

        else:
            [task.symbols.add(sub.symbol) for task in self.inside_bar_tasks if sub.frequency == task.frequency and task.wait_group == True]

    def _remove_bar_task(self, sub):
        # 如果不是wait_group的， 说明都是单独订阅的
        if not sub.wait_group:
            [self._bar_tasks.remove(task) for task in self._bar_tasks if task.symbols == [sub.symbol] and not task.wait_group]
            return

        # 如果是wait_group的， 要判断是否是单独的
        [self._bar_tasks.remove(task) for task in self._bar_tasks if task.symbols == [sub.symbol] and task.wait_group]
        # task.symbols != [sub.symbol] 说明还有一起存的
        [task.symbols.remove(sub.symbol) for task in self._bar_tasks if sub.symbol in task.symbols and task.wait_group]

    def _set_parameters(self):
        from gm.api.basic import get_parameters
        parameters = get_parameters()
        for p in parameters:
            key = p['key']
            self.inside_parameters[key] = p

    def _get_account_info(self, account_id):
        # 资金信息
        req = GetCashReq()
        req.account_id = account_id
        req = req.SerializeToString()
        status, result = py_gmi_get_cash(req)
        if not status == CSDK_OPERATE_SUCCESS:
            return

        cashes = Cashes()
        cashes.ParseFromString(result)
        cashes = [protobuf_to_dict(cash) for cash in cashes.data]
        cash = cashes[0]

        # 持仓信息
        req = GetPositionsReq()
        req.account_id = account_id
        req = req.SerializeToString()
        status, result = py_gmi_get_positions(req)
        if not status == CSDK_OPERATE_SUCCESS:
            return

        positions = Positions()
        positions.ParseFromString(result)

        positions = [protobuf_to_dict(position) for position in positions.data]
        positions_infos = {'{}.{}'.format(position['symbol'], position['side']): position for position in positions}

        # 获取account 的title
        req = GetAccountConnectionsReq()
        req.account_ids.extend([account_id])
        req = req.SerializeToString()
        status, result = py_gmi_get_account_connections(req)
        if not status == CSDK_OPERATE_SUCCESS:
            return

        res = AccountConnections()
        res.ParseFromString(result)
        account_info = [protobuf_to_dict(one) for one in res.data]
        # 回测的话收不到account_info  默认 title = account_id
        if not account_info:
            title = account_id
        else:
            account_info = account_info[0]
            title = account_info['account']['title']

        # 初始化信息
        account = Account(account_id, title, cash, positions_infos)
        self.inside_accounts[account_id] = account


# 提供给API的唯一上下文实例
context = Context()
context.inside_init()


# 任务中心 按 symbols， frequency 来分组
class BarTask(object):
    def __init__(self, symbols, frequency, wait_group, wait_group_timeout):
        self.waiting = False
        self.symbols = set(symbols)
        self.frequency = frequency
        self.wait_group = wait_group
        self.overtime = wait_group_timeout

        self.performed_eobs = set()
        self.wait_perform_eob = None

    def set_wait_perform_eob(self, bar):
        symbol = bar['symbol']
        eob = bar['eob']
        frequency = bar['frequency']
        if symbol not in self.symbols or not frequency == self.frequency:
            return

        if not self.wait_perform_eob:
            self.wait_perform_eob = eob

    # 每接受一个数据， 都会判断下是否满足条件， 如果满足条件， 将is_ready 改成true
    def state_analysis(self):
        # 执行过的任务不在执行
        if context.now in self.performed_eobs:
            return

        if not self.wait_perform_eob:
            return

        # 要判断一下是不是订阅的代码都到了啊。
        all_present = True
        for symbol in self.symbols:
            sub_tag = SUB_TAG.format(symbol, self.frequency)
            from gm.model.storage_data import SubBarData
            if not SubBarData().data_is_ready(sub_tag, context.now):
                all_present = False

        if all_present:
            return self.sign_waiting(context.now)

        # 如果超时时间到了， 任务就必须执行， 直接设is_ready = True
        if (context.now - self.wait_perform_eob).total_seconds() >= self.overtime:
            self.sign_waiting(self.wait_perform_eob)
            return

    # 任务执行以后要重置一下
    def reset(self):
        self.waiting = False
        self.performed_eobs.add(self.wait_perform_eob)
        self.wait_perform_eob = None

    # 标记待执行任务和状态
    def sign_waiting(self, eob):
        self.waiting = True
        self.wait_perform_eob = eob

    # 获取等待返回的bar
    def get_perform_bars(self):
        from gm.model.storage_data import SubBarData
        bars = SubBarData().inside_get_data(self.symbols, self.frequency, self.wait_perform_eob)
        bars = [ObjectLikeDict(bar) for bar in bars]
        return bars
