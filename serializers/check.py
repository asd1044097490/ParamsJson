from serializers.error import CheckError


class Check:

    check_name = {
        'check_required': None,
        'check_emtpy': None,
        'check_null': None,
    }

    def __init__(self):
        """
        docstring
        """
        self.error_dict = {}

    def check_required(self, field_instance):
        return CheckError('name')

    def check_null(self, field_instance):
        pass

    def check_empty(self, field_instance):
        pass

    def is_check_required(self, field_instance) -> bool:
        """
        Is True check
        Is False not check, skip

        Args:
            field_instance ([type]): [description]

        Returns:
            bool: [description]
        """

        return field_instance.required

    def is_check_null(self, field_instance) -> bool:
        """[summary]

        Args:
            field_instance ([type]): [description]

        Returns:
            bool: [description]
        """
        return not field_instance.null

    def is_check_empty(self, field_instance) -> bool:
        """[summary]

        Args:
            field_instance ([type]): [description]

        Returns:
            bool: [description]
        """
        return not field_instance.empty

    def to_check_funcs(self, field_instance):
        """
        docstring
        """
        check_func_list = []

        if self.is_check_required(field_instance=field_instance):
            check_func_list.append(self.check_required.__name__)
        if self.is_check_empty(field_instance):
            check_func_list.append(self.check_empty.__name__)
        if self.is_check_null(field_instance):
            check_func_list.append(self.check_null.__name__)

        return check_func_list

    def run_check(self, field_instance):
        check_name_list = self.to_check_funcs(field_instance)

        for check_name in check_name_list:
            check_func = getattr(self, check_name, None)
            if check_func:
                result = check_func(field_instance)
                if isinstance(result, CheckError):
                    field_instance.error_dict.update({check_name: result.detail})
            else:
                raise ValueError(
                    f'Current instance:<{self}:class:{self.__class__}> not found check function<{check_name}>')


class ObjectCheck(Check):

    # def _check_self(self, serializer_instance):
    #     check_name_list = self.to_check_funcs(serializer_instance)
        

    def run_check(self, field_instance):
        serializer_instance = field_instance

        if not serializer_instance.skip_serializer:
            # check serializer
            super().run_check(field_instance=serializer_instance)

        # check_name_list = self.to_check_funcs(
        #     field_instance=serializer_instance
        #     )

        # if not serializer_instance.skip_serializer:
        #     # check serialzier
        #     for check_name in check_name_list:
        #         check_func = getattr(self, check_name, None)
        #         if check_func:
        #             result = check_func(serializer_instance)
        #             if isinstance(result, CheckError):
        #                 errors.append(result)

        if not serializer_instance.skip_all:
            # check field
            for field_name, field in serializer_instance.fields.items():
                field.run_check(field)
