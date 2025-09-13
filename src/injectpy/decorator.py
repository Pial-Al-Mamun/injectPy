import inspect
from functools import wraps
from ._container import Container


def service(cls):
    return Container.register(cls)


def inject(init_func):
    """
    Decorator to automatically inject dependencies into a class constructor.

    It inspects the constructor's parameters and looks for type annotations
    that match registered services. For each parameter:
        - If it has a type annotation that is registered in the container,
          the corresponding instance is resolved and passed automatically.
        - Existing values in kwargs are preserved.
        - 'self' is always ignored.
        - Any parameter in `ignore` will be skipped.

    Parameters:
    - init_func: The __init__ method of a class to decorate.

    Returns:
    - A wrapped __init__ method that automatically injects dependencies.
    """
    sig = inspect.signature(init_func)

    @wraps(init_func)
    def wrapper(self, *args, **kwargs):
        for name, param in sig.parameters.items():
            # Skip self, already-provided kwargs
            if name == "self" or name in kwargs :
                continue

            ann = param.annotation
            # Only try to resolve if the annotation is registered in the container
            if ann in Container._registrations:
                kwargs[name] = Container.resolve(ann)
            # Otherwise leave it as-is; user must provide a value manually

        return init_func(self, *args, **kwargs)

    return wrapper


def singleton(cls):
    return Container.register(cls, lifetime="singleton")