

class ValidationException(Exception):
    def __init__(self, message, field, value, hint=None, code=None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.value = value
        self.hint = hint
        self.code = code

    def __str__(self):
        base = f"Validation error on '{self.field}': некорректный формат значения '{self.value}'. {self.message}"
        return f"{base}. Hint: {self.hint}" if self.hint else base


