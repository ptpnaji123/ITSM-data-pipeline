from _typeshed import Incomplete

class DeviceAuthorizationEndpoint:
    ENDPOINT_NAME: str
    CLIENT_AUTH_METHODS: Incomplete
    USER_CODE_TYPE: str
    EXPIRES_IN: int
    INTERVAL: int
    server: Incomplete
    def __init__(self, server) -> None: ...
    def __call__(self, request): ...
    def create_endpoint_request(self, request): ...
    def authenticate_client(self, request): ...
    def create_endpoint_response(self, request): ...
    def generate_user_code(self): ...
    def generate_device_code(self): ...
    def get_verification_uri(self) -> None: ...
    def save_device_credential(self, client_id, scope, data) -> None: ...

def create_string_user_code(): ...
def create_digital_user_code(): ...
