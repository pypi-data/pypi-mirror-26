from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, DataSink, PipelineContext, Query, validate_query

from cassiopeia.data import Platform, Region
from cassiopeia.dto.masterypage import MasteryPagesDto
from cassiopeia.datastores.uniquekeys import convert_region_to_platform
from .common import SimpleKVDiskService

T = TypeVar("T")


class MasteryPagesDiskService(SimpleKVDiskService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    #################
    # Mastery Pages #
    #################

    _validate_get_mastery_pages_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    @get.register(MasteryPagesDto)
    @validate_query(_validate_get_mastery_pages_query, convert_region_to_platform)
    def get_mastery_pages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasteryPagesDto:
        key = "{clsname}.{platform}.{id}".format(clsname=MasteryPagesDto.__name__,
                                                 platform=query["platform"].value,
                                                 id=query["summoner.id"])
        return MasteryPagesDto(self._get(key))

    @put.register(MasteryPagesDto)
    def put_mastery_pages(self, item: MasteryPagesDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}".format(clsname=MasteryPagesDto.__name__,
                                                 platform=platform,
                                                 id=item["summonerId"])
        self._put(key, item)
