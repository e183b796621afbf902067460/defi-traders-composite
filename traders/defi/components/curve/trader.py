from typing import Optional

from head.interfaces.trader.interface import ITraderComponent
from defi.protocols.curve.contracts.Pool import CurvePoolContract
from providers.fabrics.http.fabric import httpProviderFabric


class CurveTrader(ITraderComponent):

    _markets: dict = {
        '3Crv': {
            'address': '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7',
            'provider': httpProviderFabric.getProduct(chain='eth'),
            'scale': 18
        },
        'am3CRV': {
            'address': '0x445FE580eF8d70FF569aB36e80c647af338db351',
            'provider': httpProviderFabric.getProduct(chain='matic'),
            'scale': 18
        },
        'FRAX3CRV-f': {
            'address': '0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B',
            'provider': httpProviderFabric.getProduct(chain='eth'),
            'scale': 18
        }
    }

    @classmethod
    def getPrice(self, major: str, vs: str, *args, **kwargs) -> Optional[float]:
        try:
            market = self._markets[major]
        except KeyError:
            return None

        pool: CurvePoolContract = CurvePoolContract()\
            .setAddress(address=market['address'])\
            .setProvider(provider=market['provider'])\
            .create()
        return pool.get_virtual_price() / 10 ** market['scale']
