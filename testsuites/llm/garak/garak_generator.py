from garak.generators.base import Generator
from garak.attempt import Message


class CustomGenerator(Generator):
    """ Custom Generator Wrapper for Garak """

    def __init__(self, generate_fn, config_root=None):
        super().__init__(
            name="garak-tests",
            config_root=config_root
        )

        self.generate_fn = generate_fn


    def _call_model(self,
                    prompt,
                    generations_this_call=1):
        
        # gotta convert Conversation to list[dict]
        to_pass = [{"content" : prompt.turns[-1].content.text}]

        response = self.generate_fn(to_pass)

        return [Message(text=response)]


CustomGenerator.__module__ = "generators.custom"
