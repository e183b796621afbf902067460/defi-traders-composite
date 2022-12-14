from typing import Optional

from head.interfaces.trader.interface import ITraderComponent
from defi.protocols.ellipsis.contracts.Pool import EllipsisPoolContract
from providers.fabrics.http.fabric import httpProviderFabric


class EllipsisTrader(ITraderComponent):

    _markets: dict = {
        '3EPS': {
            'address': '0x160CAed03795365F3A589f10C379FfA7d75d4E76',
            'provider': httpProviderFabric.getProduct(chain='bsc'),
            'scale': 18
        },
        '2epx': {
            'address': '0x408A61e158D7BC0CD339BC76917b8Ea04739d473',
            'provider': httpProviderFabric.getProduct(chain='bsc'),
            'scale': 18
        }
    }

    @classmethod
    def getPrice(self, major: str, vs: str, *args, **kwargs) -> Optional[float]:
        try:
            market = self._markets[major]
        except KeyError:
            return None

        pool: EllipsisPoolContract = EllipsisPoolContract()\
            .setAddress(address=market['address'])\
            .setProvider(provider=market['provider'])\
            .create()
        return pool.get_virtual_price() / 10 ** market['scale']
