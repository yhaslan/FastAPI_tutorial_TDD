import os
import time

import docker


def is_container_ready(container):
    container.reload()  # thats a method that fetches latest info about a container from docker deamon
    # so this is necessary bcz status of co,ntainer might have been changed after it had been initiated/queried
    return container.status == "running"  # will return true if running


def wait_for_stable_status(container, stable_duration=3, interval=1):
    # to check if container is sunning during three seconds, checking every second
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0  # geri 0a esitliyoruz ki interruption dumunda basa donsun ve yeniden 3 saysin

        if stable_count >= stable_duration / interval:
            return True

        time.sleep(interval)  # this controls how freq function checks the container
    return False  # this is equivalent to saying else return false mus


# usually if it runs without interruption 3 secs its ready to go dedi


def start_database_container():
    client = docker.from_env()  # this starts a client object to interact with docker
    scripts_dir = os.path.abspath(
        "./scripts"
    )  # this one will get absolute path of scripts directory idk why
    container_name = "test-db"

    # we ll first check if there is an existing container, if yes remove it, no create it

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container {container_name} exists. Stopping and removing ...")
        existing_container.stop()
        existing_container.remove()
        print(f"Container {container_name} stopped and removed.")

    except docker.errors.NotFound:
        print(f"Container {container_name} does not exist.")

    # Define container configuration
    container_config = {
        "name": container_name,
        "image": "postgres:16.1-alpine3.19",
        "detach": True,
        "ports": {
            "5432": "5434"
        },  ### port'larda once image inkini mi yaziyoduk ki ya??
        # normalde oyle yazmiyoduk, isin garibi docker desktopta yerleri degisiyo otomatik
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },  # we didnt use the env variables here as this container is gonna temporarily and destryed after test
        "volumes": [
            f"{scripts_dir}:/docker-entrypoint-initdb.d"
        ],  # docker-compsedan farkli olarak burda abs path
        "network_mode": "fastapi-development_dev-network",
    }

    # Start Container
    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(
            1
        )  # if container is not ready oit will wait a second and recheck if its ready
        # sometimes it takes time to initaite thats why

    if not wait_for_stable_status(container):
        raise RuntimeError("Container did not stabilize within the specified time")

    return container
