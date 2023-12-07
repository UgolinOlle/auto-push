import functools
from rich import print
from typing import Callable, Any

from auto_push.src.classes.github import Github


def error_issue(github: Github) -> Callable:
    """
    A decorator factory that creates a decorator for automatically creating a GitHub issue when an exception is raised in the decorated function.

    This function returns a decorator that wraps around any given function. If an exception occurs during the execution of the decorated function, the decorator catches it and creates an issue in a GitHub repository, detailing the exception and the function where it occurred.

    Parameters:
    ----------
    github : Github
        An instance of the Github class, preconfigured with necessary credentials and settings.

    Returns:
    -------
    Callable
        A decorator that can be applied to any function. The decorator will monitor the function for exceptions and create GitHub issues accordingly.

    Notes:
    ------
    - The GitHub instance (`github`) should be initialized with appropriate permissions to create issues in the repository.
    - The raised exception is re-thrown after the issue is created, ensuring that exception handling in the decorated function (or higher in the call stack) is not bypassed.

    Raises:
    -------
    Exception
        Propagates any exception caught in the decorated function after logging it to GitHub.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                try:
                    github.create_issue(title=f"Exception in {func.__name__}",
                                        body=f"{e}",
                                        labels=["bug"])
                except Exception as issue_creation_error:
                    print(f"\n[red][ERROR] - Failed to create GitHub issue: \n{
                        issue_creation_error} [/red]")
                print(f"\n[red][ERROR] - An error occured in {
                      func.__name__}: \n{e}[/red]")
        return wrapper
    return decorator
