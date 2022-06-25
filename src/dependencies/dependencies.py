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

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key