import asyncio

import aiohttp

from roi_web import loadEvents, Processer


async def main():
	async with aiohttp.ClientSession( connector = aiohttp.TCPConnector( verify_ssl = False, limit_per_host = 5, limit = 15 ) ) as session:
		processer = Processer( session )
		results = [ processer.process( url ) for url in loadEvents() ]
		await asyncio.gather( *results )


if __name__ == "__main__":
	import logging

	handler = logging.StreamHandler()
	handler.setLevel( logging.INFO)
	formatter = logging.Formatter("%(digest)s\t%(kind)s\t\t%(message)s")
	handler.setFormatter( formatter)
	myLogger = logging.getLogger("Roi")
	myLogger.addHandler( handler)
	myLogger.setLevel( logging.INFO)



	asyncio.set_event_loop_policy( asyncio.WindowsSelectorEventLoopPolicy() )
	asyncio.run( main() )