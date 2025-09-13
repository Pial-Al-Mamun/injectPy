from ._errors import NoServiceFound
from typing import Literal, Type

LIFETIME_DEPENDENCY = Literal["transient", "singleton"]


class Container:
    """
    A simple Dependency Injection (DI) container.

    Responsibilities:
    - Register service classes and their lifetimes (singleton or transient).
    - Resolve dependencies automatically.

    Attributes:
    - _registrations: Dict mapping service classes to their lifetime type.
    - _singletons: Dict storing already-created singleton instances.
    """

    _singletons = {}
    _registrations = {}

    @classmethod
    def register(cls, service_cls: Type, lifetime: LIFETIME_DEPENDENCY = "transient"):
        """
        Register a service class with the container.

        Parameters:
        - service_cls: The class to register (not an instance).
        - lifetime: Either "transient" (new instance every time)
                    or "singleton" (same instance every time).
                    Default is "transient".

        Returns:
        - Returns the class itself so that it can be resolved later from the container.
        """
        cls._registrations[service_cls] = lifetime
        return service_cls

    @classmethod
    def resolve(cls, service_cls: Type):
        """Retrieve an instance of a registered service.

        Parameters:
        - service_cls: The class of the service to resolve.

        Returns:
        - A singleton instance (if registered as singleton),
          or a new instance (if transient).

        Raises:
        - NoServiceFound: If the class is not registered in the container.
        """
        lifetime = cls._registrations.get(service_cls)

        if lifetime is None:
            raise NoServiceFound(
                f"Class '{service_cls.__name__}' is not registered. "
                "Did you forget to annotate it with @service or @singleton?"
            )

        if lifetime == "singleton":
            if service_cls not in cls._singletons:
                cls._singletons[service_cls] = service_cls()
            return cls._singletons[service_cls]

        elif lifetime == "transient":
            return service_cls()
