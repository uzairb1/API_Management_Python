import asyncio
import aiohttp

API_URL = "https://fakerapi.it/api/v2/persons?_quantity=1000&_birthday_start=1900-01-01"  # Replace with actual API URL

async def fetch_records(session, page):
    params = {'page': page}  # Assuming the API supports pagination
    async with session.get(API_URL, params=params) as response:
        return await response.json()

async def gather_records(total_records=30000, records_per_call=1000):
    total_calls = total_records // records_per_call  # Calculate the number of calls needed
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_records(session, page) for page in range(1, total_calls + 1)]
        return await asyncio.gather(*tasks)

# Run the asyncio event loop
results = asyncio.run(gather_records())