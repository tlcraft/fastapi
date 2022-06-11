import time
from fastapi import BackgroundTasks, Depends, Header, HTTPException
from ..models.common_query_params import CommonQueryParams
from typing import Union

async def common_parameters(commons: CommonQueryParams = Depends(CommonQueryParams), include_all: bool = False):
    return {**commons.__dict__, "include_all": include_all}

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: Union[str, None] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

async def verify_test_header(x_test_header: str = Header(...)):
    if x_test_header != "X-Test-Header":
        raise HTTPException(status_code=400, detail="X-Test-Header value invalid")

async def yield_dependency_example():
    try:
        start = time.perf_counter()
        print("Start: ", start)
        yield start
    finally:
        end = time.perf_counter()
        print("End: ", end)
        print(f"Completed the yield in {end - start:0.4f} seconds")