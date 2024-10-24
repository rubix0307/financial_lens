import openai


def handle_openai_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except openai.AuthenticationError as e:
            return None
        except openai.NotFoundError as e:
            return None
    return wrapper