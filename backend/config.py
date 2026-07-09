class Config():
    DEBUG= False
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LocalDevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///trekking.sqlite3"
    JWT_SECRET_KEY="NIHARIKA-JINNI-KEY"
    CACHE_TYPE="RedisCache"
    CACHE_REDIS_TYPE="localhost"
    CACHE_REDIS_PORT="6379"
    CACHE_DEFAULT_TIMEOUT="300"