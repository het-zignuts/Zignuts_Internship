import asyncio
import httpx
import requests
import time

def sync_fetch():
    response=requests.get("https://bored-api.appbrewery.com/random")
    print("Status:", response.status_code)
    print("Raw text:", response.text[:100])
    reseponse_json=response.json()
    return reseponse_json

async def async_fetch():
    async with httpx.AsyncClient() as client:
        response=await client.get("https://bored-api.appbrewery.com/random")
        print("Status:", response.status_code)
        print("Raw text:", response.text[:100])
        return response.json()

async def async_call():
    start_time=time.time()
    call1, call2 = await asyncio.gather(async_fetch(), async_fetch())
    end_time=time.time()
    print(call1)
    print(call2)
    return end_time-start_time

def sync_call():
    start_time=time.time()
    call1=sync_fetch()
    call2=sync_fetch()
    end_time=time.time()
    print(call1)
    print(call2)
    return end_time-start_time

print("Time taken by sync calls: ", sync_call())
print("Time taken by async calls: ", asyncio.run(async_call()))
    