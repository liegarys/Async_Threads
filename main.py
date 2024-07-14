import  threading
import requests
import  time

import  asyncio
import aiohttp

class ThreadingDownloader(threading.Thread):

    json_array = []

    def __init__(self, url):
        super().__init__()
        self.url = url


    def run(self):
        response = requests.get(self.url)
        self.json_array.append(response.json())
        return self.json_array


def get_data_threading(urls) :
    st = time.time()

    threads = []
    for url in urls:
        t = ThreadingDownloader(url)
        t.start()
        threads.append(t)

    for t in threads :
        t.join()
        print(t)


    et = time.time()
    elapsed_time = et - st
    print(f"Start time : {st}, End time: {et}, Elapsed time: {elapsed_time}")

def get_data_sync(urls):

    st = time.time()

    json_array = []

    for url in urls:
        json_array.append(requests.get(url).json())

    et = time.time()
    elapsed_time = et - st
    print(f"Start time : {st}, End time: {et}, Elapsed time: {elapsed_time}")

    return json_array


async  def get_data_but_as_wrapper(urls):
    json_array = []
    st = time.time()

    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                json_array.append(await response.json())


    et = time.time()
    elapsed_time = et - st
    print(f"Start time : {st}, End time: {et}, Elapsed time: {elapsed_time}")

    return  json_array

async  def get_data(session, url, json_array):

    async with session.get(url) as response:
        json_array.append(await response.json())

async  def get_data_async_concurrently(url):
    json_array = []
    st = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_data(session,url,json_array)))

        await asyncio.gather(*tasks)

    et = time.time()
    elapsed_time = et - st
    print(f"Start time : {st}, End time: {et}, Elapsed time: {elapsed_time}")

    return json_array

urls = ['https://postman-echo.com/delay/3'] * 10

print(urls)

#get_data_sync(urls) #36 seconds
#get_data_threading(urls)#3.7
#asyncio.run(get_data_but_as_wrapper(urls)) #32
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_data_async_concurrently(url=urls)) #4