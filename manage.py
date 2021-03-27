#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def load_from_env_file():
    """
    Load environment variables from the file, if option --load-env specified.
    Good for injecting environment into PyCharm run configurations for example and no need to
    manually load the env values for manage.py commands

    You can easily change the loaded env file path with overriding
    the environment variable called 'DJANGO_LOAD_ENV_FILE_PATH'.

    Call this function anywhere before the execution command line (execute_from_command_line) in the main function.
    """
    from pathlib import Path

    if "--load-env" in sys.argv:
        os.environ.setdefault('DJANGO_LOAD_ENV_FILE_PATH', '.env')
        environment_file = Path(os.environ.get('DJANGO_LOAD_ENV_FILE_PATH'))
        if environment_file.exists():
            with environment_file.open() as env_file:
                for line in env_file:
                    if line.strip():
                        key, value = line.strip().split("=", maxsplit=1)
                        os.environ.setdefault(key, value)
        else:
            print(f"You provided --load-env flag but the targeted file ({environment_file}) is not found!")
        sys.argv.remove("--load-env")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    load_from_env_file()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
