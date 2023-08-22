import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    OTP_TIMEOUT_IN_MINUTES = 60
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    COOKIE_EXPIRY = 60000
    PORT = 9900
    FLASKS3_BUCKET_NAME = os.getenv('static_bucket_name')
    FLASKS3_FILEPATH_HEADERS = {r'.css$': {'Content-Type': 'text/css; charset=utf-8'},
                                r'.js$': {'Content-Type': 'text/javascript'}}
    FLASKS3_ACTIVE = os.getenv("flask_s3_active", "True") == "True"
    FLASKS3_GZIP = True
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    JWT_TOKEN_LOCATION = ['headers']
    S3_PRIVATE_BUCKET = os.getenv("PRIVATE_BUCKET")
    # below is valid for tokens coming in as part of query_params
    JWT_QUERY_STRING_NAME = "token"
    # Set the secret key to sign the JWTs with
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 1


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    ENV = True
    # SQLALCHEMY_DATABASE_URI = "postgresql://flask:flask@localhost:5433/flask"
    SQLALCHEMY_DATABASE_URI = "postgresql://dataorc:xoo8Wum2udae7uoy@localhost:5432/fm_dashboard"
    DOMAIN = "http://localhost:9900"



class TestingConfig(Config):
    DEBUG = True
    PORT = 9901
    SQLALCHEMY_DATABASE_URI = "postgresql://flask:flask@localhost:5433/flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOMAIN = "http://localhost:9900"
    PROPOGATE_EXCEPTIONS = True
    REDSHIFT_ANALYTICS_SCHEMA = "analytics"


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    JWT_COOKIE_CSRF_PROTECT = False
    MMI_CLIENT_ID = os.getenv("MMI_CLIENT_ID")
    MMI_CLIENT_SECRET = os.getenv("MMI_CLIENT_SECRET")
    MMI_ADVANCE_API_KEY = os.getenv("MMI_ADVANCE_API_KEY")
    knowlarity_number = os.getenv("KNOWLARITY_NUMBER")
    knowlarity_agent_number = os.getenv("KNOWLARITY_AGENT_NUMBER")
    knowlarity_api_key = os.getenv("KNOWLARITY_API_KEY")
    knowlarity_authorization_header_key = os.getenv("KNOWLARITY_AUTHORIZATION_HEADER_KEY")


class LightConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    JWT_COOKIE_CSRF_PROTECT = False
    ZENDRIVE_API_KEY = os.getenv("ZENDRIVE_API_KEY")
    sign_up_approvers = ["navdeep@dataorc.in", "mayur@dataorc.in", "shrey@dataorc.in"]
    SES = {
        "from_email": "no-reply@whatsapp.dataorc.in",
        "region": "ap-south-1",
    }


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    light=LightConfig,
)

key = Config.SECRET_KEY


def get_config_by_name(config_name, default=None, env_param_name=None):
    config_env = os.getenv(env_param_name or "ENV")
    config_value = default
    if config_env:
        config_value = getattr(config_by_name[config_env](), config_name, default)
    return config_value


def get_email_config_value_for_name(config_name):
    email_config_value = get_config_by_name("SES") or {}
    config = email_config_value.get(config_name)
    return config


if __name__ == '__main__':
    os.environ["ENV"] = "light"
    print(get_config_by_name("DOMAIN"))

    os.environ["ENV"] = "prod"
    print(get_email_config_value_for_name("from_email"))
