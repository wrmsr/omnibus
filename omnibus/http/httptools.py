"""
FIXME: jettison wsgiref?
"""
import asyncio

import httptools


class HttpToolsRequestParserListener:

    def on_message_begin(self):
        pass

    def on_url(self, url: bytes):
        pass

    def on_header(self, name: bytes, value: bytes):
        pass

    def on_headers_complete(self):
        pass

    def on_body(self, body: bytes):
        pass

    def on_message_complete(self):
        pass

    def on_chunk_header(self):
        pass

    def on_chunk_complete(self):
        pass

    def on_status(self, status: bytes):
        pass


"""
# self.headers = http.client.parse_headers(self.rfile, _class=self.MessageClass)

def httptools_parse_headers(fp, _class=http.client.HTTPMessage):
    l = HttpToolsRequestParserListener()
    p = httptools.HttpResponseParser(l)
    # p.feed_data(b'POST /test HTTP/1.1\r\n')
    while True:
        line = fp.readline()
        if not line:
            break
        p.feed_data(line)
    raise NotImplementedError

http.client.parse_headers = httptools_parse_headers
"""


# https://github.com/MagicStack/httptools/issues/20


class Request:

    def __init__(self):
        self.EOF = False

    def on_url(self, url: bytes):
        self.on_url_called = True

    def on_message_complete(self):
        self.EOF = True


async def serve(reader, writer):
    chunks = 2 ** 16
    req = Request()
    parser = httptools.HttpRequestParser(req)
    while True:
        data = await reader.read(chunks)
        parser.feed_data(data)
        if not data or req.EOF:
            break
    assert req.on_url_called
    writer.write(b'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK')
    writer.write_eof()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_task(asyncio.start_server(serve, '127.0.0.1', 8080))
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Bye.')
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
