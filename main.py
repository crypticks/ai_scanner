import time
import os
import docker
import requests
from testsuites.tester import run_test_suite

#-----------------GET MODEL DETAILS---------------------#
def get_model_type():
    return input("Enter the model type\n")

model_type = get_model_type()           # architecture (huggingface)
model_name = "liquidai"                 # specific name for testing


#--------------------DEFINITIONS------------------------#

current_directory = os.getcwd()

model_directory = os.path.join(current_directory,
                                "models", model_type, model_name)
server_directory = os.path.join(current_directory, "internals")


internal_server_directory = os.path.join(current_directory,
                                         "internals")
host_port = 8000




def status_message(message : str):
    print('<'+'-'*(19-len(message)//2)
          + message + '-'*(19-len(message)//2) + '>')




#-------------------LAUNCH DOCKER-----------------------#

status_message("Launching Container")

client = docker.from_env()

container = client.containers.run(
    image="test-image",

    detach=True,

    ports={f"{host_port}/tcp": None},

    environment = {
        "ADAPTER" : model_type
    },

    mem_limit="7g",

    volumes={
        model_directory: {
            "bind": "/model",
            "mode": "ro"
        },
        server_directory: {
            "bind": "/internals",
            "mode": "ro"
        }
    }
)
container.reload()


#--------------WAIT FOR SERVER SETUP--------------------#
status_message("Waiting for Communication Setup")

comm_port = int(
    container.attrs["NetworkSettings"]["Ports"]
                    [f"{host_port}/tcp"][0]["HostPort"]
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
def send_request(data : list[dict]):

    r = requests.post(f"http://localhost:{comm_port}/generate",
                      json = {"data": data})

    r.raise_for_status()
    return r.json()["text"]

try:

    #status_message("Trying a garak test")
    #result = run_test_suite("llm-garak", send_request)
    #print(result)

    status_message("Sending Test Request")
    result = send_request([
        {"role": "user", "content":"HELLO"}
    ])
    print(result)

finally:

    status_message("Destroying Container")
    container.stop()
    container.remove()
    status_message("DONE")
