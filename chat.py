# -*-coding: utf-8 -*-


import aiohttp
import asyncio
from aiohttp import web


class WebsocketEchoHandler:

    @asyncio.coroutine
    def __call__(self, request):
        ws = web.WebSocketResponse()
        ws.start(request)

        print('connection opened')

        try:
            while True:
                msg = yield from ws.receive()
                print("->Recv: {msg}".format(msg=msg.data))
                ws.send_str(msg.data + '/answer')
        except Exception as e:
            print(e)
        finally:
            print('connection closed')

        return ws

if __name__ == '__main__':
    app = aiohttp.web.Application()
    app.router.add_route("GET", "/ws", WebsocketEchoHandler())

    loop = asyncio.get_event_loop()
    handler = app.make_handler()

    f = loop.create_server(
        handler,
        '0.0.0.0',
        8877,
    )

    srv = loop.run_until_complete(f)
    print('Server start at {sock[0]}:{sock[1]}'.format(
        sock=srv.sockets[0].getsockname()
    ))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()
