class Config():
    DEBUG= False
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LocalDevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///trekking.sqlite3"
    JWT_SECRET_KEY="NIHARIKA-JINNI-KEY"
    