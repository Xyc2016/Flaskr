class Config:
    pass


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://root:Password@localhost:3306/Flaskr'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'SECRET_KEY'
