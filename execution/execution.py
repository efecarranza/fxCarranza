from __future__ import print_function

from abc import ABCMeta, abstractmethod
import logging
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import urllib3
urllib3.disable_warnings()

from qsforex.client.base_client import BaseClient

class ExecutionHandler(object):
    """
    Provides an abstract base class to handle all execution in the
    backtesting and live trading system.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self):
        """
        Send the order to the brokerage.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecution(ExecutionHandler):
    """
    Provides a simulated execution handling environment. This class
    actually does nothing - it simply receives an order to execute.

    Instead, the Portfolio object actually provides fill handling.
    This will be modified in later versions.
    """
    def execute_order(self, event):
        pass


class OANDAExecutionHandler(ExecutionHandler):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute_order(self, event):
        print('Executing Order')
        return
        instrument = "%s_%s" % (event.instrument[:3], event.instrument[3:])
        params = urlencode({
            "instrument" : instrument,
            "units" : event.units,
            "type" : event.order_type,
            "side" : event.side
        })

        response = BaseClient().send_request('POST', params)
        response = self.conn.getresponse().read().decode("utf-8").replace("\n","").replace("\t","")
        self.logger.debug(response)

        self.conn.close()

        