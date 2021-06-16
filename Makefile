test:
	#!/usr/bin/env bash
	set -e
	DOCKER_BUILDKIT=1 docker build . --target test --progress plain
	
run:
	python3 photo_details.py

