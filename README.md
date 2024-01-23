# Python Thingspeak Demo
The purpose of this repository is to demonstrate how a Python script can be run as K8s Job.
The Python script is run inside a docker image that is stored in the repository [petrjamf/thingspeak-demo](https://hub.docker.com/r/petrjamf/thingspeak-demo) and it periodically updates the value of the `field1`` of one of my thinspeak.com private channels (called On Air Light) with the current timestamp.

The channel is protected from unauthorized access by API key. The key and channel ID is provided in a form of environmental variables.

## Python

### venv

Create the virtual environment "thingspeak" and install the required modules.
```
python -m venv thingspeak
pip install -r requirements.txt
```

### Thingspeak module documentation

https://thingspeak.readthedocs.io/en/latest/_modules/thingspeak.html#Channel.get


## Docker

Follow the instructions on https://docs.docker.com/language/python/containerize/

```
cd Docker
docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.7.4
? What port do you want your app to listen on? 8000
? What is the command to run your app? python3 thingspeak-demo.py -k ${API_KEY} -ch ${CHANNEL_ID}
```
As the port to listen on is unused it might be removed from the Dockerfile
All other propertis might be checked out or customized in the Docker file as well.


### Build the image

Build the image and run the docker with compose. The env variables are defined in `compose.yaml`.
Update the line 15 and 16 with the respective values:

```
services:
  thingspeak:
    build:
      context: .
    environment:
      - API_KEY=<paste your api write-key here>
      - CHANNEL_ID=<paste your channel-id here>
```

Build the image with docker compose.
```
docker compose up --build
```

Or run the container manually if the image has already been built and only the containre need to be instantiated.
```
docker run -d -t -i \
-e API_KEY='<write-api-key>' \
-e CHANNEL_ID='<channel-id>' \
--name thingspeak docker-thingspeak
```

### Push the image to the registry

```
# Rename the image to the format <registry-name>/<repository-name>
docker tag docker-thingspeak:latest petrjamf/thingspeak-demo

# Upload the image
docker image push petrjamf/thingspeak-demo
```

## K8s

### Secrets

Create the secrets
```
kubectl create secret generic thingspeak-api-key --from-literal=api_key=<API write-key>
kubectl create secret generic thingspeak-channel-id --from-literal=channel_id=<channel-id>
```

### CronJob

Create the CronJob
```
kubectl apply -f cronjob.yaml
```

## Tests

Run the Python script.
```
python3 thingspeak-demo.py -k '<write-key>' -ch '<channel-id>'
```

Check the staus of the field from the terminal on your Mac to see if the values are being incremented proving the CronJob is active.
```
curl "https://api.thingspeak.com/channels/2203959/fields/1/last.json?api_key=<read key>"
```
