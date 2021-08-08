.PHONY: $(MAKECMDGOALS)
.SILENT: ${MAKECMDGOALS}

image_name=mkdocs-dev
image_tag=devbuild
image_url=${image_name}:${image_tag}
container_name=mkdocs-dev-app

container_port=80
localhost_port=8000


run:
	make clean
	make build
	
	echo "*** Run"
	echo "Starting dev-server on http://localhost:${localhost_port}/"
	docker run \
		-it \
		--rm \
		--name ${container_name} \
		--env PORT=${container_port} \
		-p ${localhost_port}:${container_port} \
		-v ${PWD}/mkdocs:/synced \
		${image_url} \
		|| true
	
	make clean

clean:
	echo "*** Clean"
	docker rmi ${image_url} || true

build:
	echo "*** Build"
	docker build -t ${image_url} .
