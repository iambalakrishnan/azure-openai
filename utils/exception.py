class OpenAIAPIError(Exception):
    """Exception raised for errors in the OpenAI API."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code
