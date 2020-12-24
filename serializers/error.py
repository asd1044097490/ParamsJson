class SerializerError(Exception):
    
    def __init__(self, *args: object, detail=None) -> None:
        super().__init__(*args)
        self.detail = detail


class CheckError(SerializerError):
    pass
