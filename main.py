import sys
import time
import os
import docker
import requests


def get_model_type():
    return input("Enter the model type\n")


def send_request(port : int, 
                 data : str):

    r = requests.post(f"http://localhost:{port}/generate",
                      json = {"data": data})

    r.raise_for_status()
    return r.json()["text"]



#--------------------GET MODEL TYPE---------------------#

model_type = get_model_type()


#--------------------DEFINITIONS------------------------#

current_directory = os.getcwd()
models_directory = os.path.join(current_directory,
                                "models")
internal_server_directory = os.path.join(current_directory,
                                         "internals")


host_port = 8000


#-------------------LAUNCH DOCKER-----------------------#

client = docker.from_env()

container = client.containers.run(
    image="test-image",

    detach=True,

    ports={f"{host_port}/tcp": None},

    environment = {
        "ADAPTER" : "hf"
    },

    mem_limit="2g",

    volumes={
        models_directory: {
            "bind": "/model",
            "mode": "ro"
        }
    }
)
container.reload()


#--------------WAIT FOR SERVER SETUP--------------------#

comm_port = int(
    container.attrs["NetworkSettings"]["Ports"][f"{host_port}/tcp"][0]["HostPort"]
)

while True:
    try:
        r = requests.get(f"http://localhost:{comm_port}/docs")
        if r.status_code == 200:
            break
    except:
        pass

    container.reload()
    if container.status != "running":
        print(container.logs().decode())
        raise Exception("Container crashed")

    time.sleep(0.5)


#-----------------SEND TEST MESSAGE---------------------#

result = send_request(comm_port, "HELLO")
print(result)

container.stop()
container.remove()
