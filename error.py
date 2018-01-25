
# todo add inheritance for email on error

class NoEntryPointError(Exception):
    """Raised when an entry point is not specified when required."""
    pass

class NoneResponseError(Exception):
    """Raised when the response returned via the invocation of the entity is None"""
    pass

class InterfaceNotFoundError(Exception):
    """Raised the interface cannot be found in the interface registry"""
    pass

class TypeNotFoundError(Exception):
    """Raised the type cannot be found in TYPE"""
    pass

class InputTypeNotFoundError(Exception):
    """Raised the type cannot be found in TYPE"""
    pass

class InterfaceDisabledError(Exception):
    """Raised when the interface has been disabled"""
    pass

class InterfaceInactiveError(Exception):
    """Raised when the interface has been made inactive"""
    pass

class InvalidServiceError(Exception):
    """Raised when the interface has been made inactive"""
    pass

# Email/ Notify errors
# --------------------------------------------------------------------------------------------------------------------->