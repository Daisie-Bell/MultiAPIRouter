from multiapi_routes.Routes.Configs     import Configs
from multiapi_routes.Routes.Forward     import forward_
from multiapi_routes.Routes.Wallet      import Wallets
from multiapi_routes.Routes.Skeleton    import Skeleton
from multiapi_routes.Routes.VirtualBond import Virtual_Bond

from fastapi import APIRouter

class MultiAPIRouter(APIRouter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update({"wallet": Wallets()})
        self.__dict__.update({"virtual_bond": Virtual_Bond()})
        self.__dict__.update({"skeleton": Skeleton()})
        self.__dict__.update({"config": Configs()})
        self.__dict__.update({"forward": forward_})

        self.include_router(self.wallet)
        self.include_router(self.virtual_bond)
        self.include_router(self.skeleton)
        self.include_router(self.config)
        self.include_router(self.forward)
