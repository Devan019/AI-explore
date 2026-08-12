import os
import dotenv

dotenv.load_dotenv()

def get_env_variable(var_name):
    """Get the environment variable or raise an exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise EnvironmentError(error_msg)