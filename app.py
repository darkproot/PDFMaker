import tornado.web
import tornado.httpserver
import asyncio

from config import DevelopmentConfig, ProductionConfig
from handlers.main import MainHandler
from handlers.generator import GeneratorHandler


class Application(tornado.web.Application):
    def __init__(self, config):
        handlers = [
            (r'/', MainHandler),
            (r'/generator', GeneratorHandler),
            (
                r'/static/(.*)', 
                tornado.web.StaticFileHandler, {
                "path": config.STATIC_PATH
            }),
            (
                r'/fonts/(.*)', 
                tornado.web.StaticFileHandler, {
                "path": config.FONT_PATH
            }),
            (
                r'/pdf/(.*)', 
                tornado.web.StaticFileHandler, {
                "path": config.PDF_PATH
            }),
            (
                r'/image/(.*)', 
                tornado.web.StaticFileHandler, {
                "path": config.IMAGE_PATH
            })
        ]

        settings = {
            "template_path": config.TEMPLATE_PATH,
            "static_path": config.STATIC_PATH,
            "debug": config.DEBUG,
            "reload": True
        }

        super().__init__(handlers, **settings)



async def main():
    config = DevelopmentConfig()
    app = Application(config)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(config.PORT)
    print(f"Server: http://localhost:{config.PORT}")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())