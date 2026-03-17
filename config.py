import os

class Config:
    DEBUG = True
    PORT = int(os.environ.get("PORT", 8888))
    STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
    FONT_PATH = os.path.join(os.path.dirname(__file__), "database/fonts")
    PDF_PATH = os.path.join(os.path.dirname(__file__), 'database/pdf')
    IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'database/image')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True