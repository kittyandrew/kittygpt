from typing import Callable
import inspect


class Command:
    def __init__(self, func: Callable, terminating: bool = False):
        # @TODO: This will break for lambdas, so we need to generate (randomized) name in that case.
        self.name = func.__name__

        if not func.__doc__: raise ValueError(f"Func '{self.name}': missing docstring!")
        self.doc = func.__doc__.strip(",. \n\r\t")

        spec = inspect.getfullargspec(func)
        for arg in spec.args:
            # @NOTE: If user annotates 'return' this will show up here!
            if arg not in spec.annotations:
                raise ValueError(f"Func '{self.name}': argument '{arg}' is not annotated!")

        # @TODO: This errors out if complex type (union etc)!
        self.annotations = {name: value.__name__ for name, value in spec.annotations.items()}
        self.func = func
        self.terminating = terminating

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
