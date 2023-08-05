from typing import TypeVar, Type, Set, Iterable, Mapping

from datapipelines import CompositeDataSource, CompositeDataSink

from .common import SimpleKVDiskService

T = TypeVar("T")


def _default_services(path: str = None, expirations: Mapping[type, float] = None) -> Set[SimpleKVDiskService]:
    from .staticdata import StaticDataDiskService
    from .champion import ChampionDiskService
    from .summoner import SummonerDiskService
    from .championmastery import ChampionMasteryDiskService
    from .runepage import RunePagesDiskService
    from .masterypage import MasteryPagesDiskService
    from .match import MatchDiskService
    from .spectator import SpectatorDiskService
    from .status import ShardStatusDiskService
    from .leagues import LeaguesDiskService

    services = {
        StaticDataDiskService(path, expirations=expirations),
        ChampionDiskService(path, expirations=expirations),
        SummonerDiskService(path, expirations=expirations),
        ChampionMasteryDiskService(path, expirations=expirations),
        RunePagesDiskService(path, expirations=expirations),
        MasteryPagesDiskService(path, expirations=expirations),
        MatchDiskService(path, expirations=expirations),
        SpectatorDiskService(path, expirations=expirations),
        ShardStatusDiskService(path, expirations=expirations),
        LeaguesDiskService(path, expirations=expirations)
    }

    return services


class SimpleKVDiskStore(CompositeDataSource, CompositeDataSink):
    def __init__(self, path: str = None, expirations: Mapping[type, float] = None, services: Iterable[SimpleKVDiskService] = None):
        if services is None:
            services = _default_services(path, expirations)

        CompositeDataSource.__init__(self, services)
        CompositeDataSink.__init__(self, services)

    def clear(self, type: Type[T] = None):
        sinks = {sink for many_sinks in self._sinks.values() for sink in many_sinks}
        for sink in sinks:
            for key in sink._store:
                if type is None:
                    sink._store.delete(key)
                elif key.startswith("{}.".format(type.__name__)):
                        sink._store.delete(key)

    def delete(self, item: Type[T]):
        raise NotImplemented
