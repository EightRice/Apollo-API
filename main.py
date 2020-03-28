from uvicorn import run
from dynaconf import settings
from api.v1 import create_api

server = create_api()

"""
1. Setup logger
2. Setup workers
3. Instantiate DB
4. Instantiate service (glue between worker API and DB)
5. Create server with reference to the service
6. Run server
"""

if __name__ == "__main__":
    host = settings.get("server_host")
    port = settings.get("server_port")
    run("main:server", host=host, port=port, log_level="info")
