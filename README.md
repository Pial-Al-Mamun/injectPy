# InjectPy

A lightweight **Dependency Injection (DI) library for Python**.  
It helps you write cleaner, more testable code by automatically wiring up dependencies.

---

## ✨ Features
- Simple and Pythonic API
- Minimal boilerplate
- Explicit dependency management

### How it works

To use it you have to use the ```python @service" ``` decorator in a service class to register the dependency

```python
from injectpy import service
@service
class ServiceClass:
    ...
```

Now to use the dependency you only have to inject this to the constructor *NOTE* that you have to typehint the class for it to actually work

```python
from injectpy import inject

class Foo:
    @inject
    def __init__(self, service_class: ServiceClass)
        ...
```

You can also create a singleton

```python
from injectpy import singleton

@singleton
class SingletonClass:
    ...
```

### Example
To showcase how easy it is the library I will give a practical example that uses services and inject those services
```python
#service.py
from injectpy import service, singleton, inject

# ------------------------
# Services
# ------------------------

@singleton
class Logger:
    """A singleton logger that is shared across the app."""
    def log(self, message: str):
        print(f"[LOG] {message}")


@service
class UserService:
    """Transient service: new instance every time it is injected."""
    def __init__(self):
        self.users = []

    def add_user(self, name: str):
        self.users.append(name)
        return self.users


@service
class NotificationService:
    """
    Transient service that depends on Logger but also accepts non-service values.
    
    The 'prefix' variable is ignored by DI and must be provided manually.
    """
    @inject(prefix)
    def __init__(self, logger: Logger):
        self.logger = logger

    def notify(self, message: str):
        self.logger.log(f"{message}")
```

In our example App class we will specifically create a last class to inject all this dependency to showcase the the services going through
```python
#main.py
class App:
    @inject
    def __init__(self, user_service: UserService, notification_service: NotificationService):
        self.users = user_service
        self.notifications = notification_service

    def run(self):
        self.users.add_user("Alice")
        self.notifications.notify("Welcome Alice!")
        self.users.add_user("Bob")
        self.notifications.notify("Welcome Bob!")


if __name__ == "__main__":
    # Manually provide the ignored argument
    app1 = App()
    app1.run()

    app2 = App()
    print("User lists are separate instances (transient):", app1.users.users, app2.users.users)
    print("Logger instances are shared (singleton):", app1.notifications.logger is app2.notifications.logger)
```