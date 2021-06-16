test:
	#!/usr/bin/env bash
	set -e
	DOCKER_BUILDKIT=1 docker build . --target test --progress plain
	
run:
	pip3.6 install -r requirements.txt
	python3 photo_details.py

