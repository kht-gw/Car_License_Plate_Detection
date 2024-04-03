# init:  sets up environment and installs requirements
# install:  Installs development requirments
# format:  Formats the code with autopep8
# lint:  Runs flake8 on src, exit if critical rules are broken
# clean:  Remove build and cache files
# env:  Source venv and environment files for testing
# leave:  Cleanup and deactivate venv
# test:  Run pytest
# run:  Executes the logic

DOCKER_NAME='car_license_app'

docker-build:
	docker build -t $(DOCKER_NAME) -f Docker/Dockerfile .

docker-run-image: 
	docker run -it --rm -v ./:/car_license_app/ --gpus all --network=host $(DOCKER_NAME)  1 "assets/images" "assets/sample_run"

docker-run-video: 
	docker run -it --rm -v ./:/car_license_app/ --gpus all --network=host $(DOCKER_NAME)  2 "assets/images" "assets/sample_run"
