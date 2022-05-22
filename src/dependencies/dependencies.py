from fastapi import Depends
from ..models.common_query_params import CommonQueryParams

async def common_parameters(commons: CommonQueryParams = Depends(CommonQueryParams), include_all: bool = False):
    return {**commons.__dict__, "include_all": include_all}