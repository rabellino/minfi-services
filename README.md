# minfi-services
A simple python web service that the minfi application can invoke api endpoints independently

## Running Locally
Running this project will deploy the python services webserver to support the endpoints the UI envokes.
To run locally:

1. Create a container network for the images to run in with (if necessary):
`$ docker network create test`
2. Build this image: `$ docker image build -t minfisvc:local -f ./docker/local/Dockerfile .`
3. Run the UI / gateway service with: `$ docker run --rm -it -p 8080:8080 --network test --name minfisvc minfisvc:local`
4. Verify service endpoints are reachable from UI