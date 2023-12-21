
from multiapi_routes.Routes.Configs     import Configs
from multiapi_routes.Routes.Forward     import forward_
from multiapi_routes.Routes.Wallet      import Wallets
from multiapi_routes.Routes.Skeleton    import Skeleton
from multiapi_routes.Routes.VirtualBond import Virtual_Bond

class MultiAPIRouter:
    def __init__(self) -> None:
        self.__dict__.update({"wallet"      : Wallets()})
        self.__dict__.update({"virtual_bond": Virtual_Bond()})
        self.__dict__.update({"skeleton"    : Skeleton()})
        self.__dict__.update({"config"      : Configs()})
        self.__dict__.update({"forward"     : forward_})