class TaskNotFoundError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class DuplicateEmailError(Exception):
    pass

class ValidationError(Exception):
    pass