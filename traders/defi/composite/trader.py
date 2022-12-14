from typing import List

from head.interfaces.trader.interface import ITraderComponent
from head.decorators.singleton import singleton
from head.decorators.yieldmethod import yieldmethod

from traders.defi.components.curve.trader import CurveTrader
from traders.defi.components.ellipsis.trader import EllipsisTrader
from traders.defi.components.convex.trader import ConvexTrader
from traders.defi.components.sturdy.trader import SturdyTrader


@singleton
class DeFiTrader(ITraderComponent):

    _traders: List[ITraderComponent] = list()

    def addTrader(self, trader) -> None:
        self._traders.append(trader)
        trader.setParent(self, parent=self)

    @yieldmethod
    def getPrice(self, major: str, vs: str = 'USD') -> float:
        for trader in self._traders:
            yield trader.getPrice(major=major, vs=vs)


defiTrader = DeFiTrader()

defiTrader.addTrader(trader=CurveTrader)
defiTrader.addTrader(trader=EllipsisTrader)
defiTrader.addTrader(trader=ConvexTrader)
defiTrader.addTrader(trader=SturdyTrader)
