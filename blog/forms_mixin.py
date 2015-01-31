

class AddCustomErrorMixin(object):
    def add_custom_error(self, error_code, **kwargs):
        if self.error_messages is None:
            raise ValueError('`error_messages` is required form attribute.')
        self._errors[error_code] = self.error_messages[error_code] % kwargs
