# Recovery, Setup and Shutdown, and Maintenance Handlers
# =====================================================================================================================>

class Handler():
    def __init__(self):
        raise NotImplemented


class ExitHandler():
    def __init__(self):
        raise NotImplemented


class SetupHandler():
    def __init__(self):
        raise NotImplemented


class RecoveryHandler():
    def __init__(self):
        raise NotImplemented


class AlertHandler():
    def __init__(self):
        # todo alerts all admin with specific alerting protocols
        raise NotImplemented

    async def email(self):
        raise NotImplemented

    async def whatsapp(self):
        raise NotImplemented


class FailureHanlder():
    def __init__(self):
        raise NotImplementedError