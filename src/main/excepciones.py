class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

class ResourceNotFoundError(Exception):
    def __init__(self, error):
        self.error = error
        self.status_code = 404

class PermissionError(Exception):
    def __init__(self, error):
        self.error = error
        self.status_code = 401
