class Field:
    
    def __init__(
        self, name=None,
        required=True, null=False, empty=False,
        to_value_instance=None, error_msg_instance=None) -> None:

        self.name = name
        self.required, self.null, self.empty = required, null, empty
        self.to_value_instance, self.error_msg_instance = to_value_instance, error_msg_instance


if __name__ == "__main__":
    Field()