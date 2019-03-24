import enum
import os

class Config:

    class EnvVar(enum.Enum):
        auth_type = "AZDEVMDFORGE_AUTH_TYPE"
        auth_token = "AZDEVMDFORGE_AUTH_TOKEN"
        org_url = "AZDEVMDFORGE_ORG_URL"
        query_id = "AZDEVMDFORGE_QUERY_ID"

    class AuthType(enum.Enum):
        personal_access_token = "PERSONAL_ACCESS_TOKEN"

    @classmethod
    def config_loading_from_env(cls):
        config = Config()
        config.load_from_env()
        return config

    def __init__(self):
        self._auth_type = None
        self._auth_token = None
        self._org_url = None
        self._query_id = None

    @property
    def auth_type(self):
        return self._auth_type

    @property
    def auth_token(self):
       return self._auth_token
 
    @property
    def org_url(self):
        return self._org_url

    @property
    def query_id(self):
        return self._query_id

    def load_from_env(self):
        self._auth_type = os.environ.get(Config.EnvVar.auth_type.value, None)
        self._auth_token = os.environ.get(Config.EnvVar.auth_token.value, None)
        self._org_url = os.environ.get(Config.EnvVar.org_url.value, None)
        self._query_id = os.environ.get(Config.EnvVar.query_id.value, None)

    def valid(self):
        return self.auth_type != None and self.auth_token != None and self.org_url != None and self.query_id != None
