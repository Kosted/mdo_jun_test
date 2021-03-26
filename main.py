import os
from http.server import HTTPServer

from dotenv import load_dotenv

from server import HttpServer

load_dotenv()


def get_env(variable_name, default=None):
    value = os.getenv(variable_name, default)
    if value is None:
        raise ValueError(f"{variable_name} is not not presented in environment variables. Check your .env file")
    if str(value).lower() in ("true", "false"):
        return str(value).lower() == "true"
    return value


if __name__ == "__main__":

    delta = float(get_env("DELTA", 1.0))
    hostName = get_env("HOSTNAME", 'localhost')
    serverPort = int(get_env("SERVERPORT", 8000))
    force_reread_flag = bool(get_env("FORSE_REREAD_FLAG", False))

    server = HttpServer(hostName, serverPort, delta, force_reread_flag)

    server.run()








