.PHONY: $(MAKECMDGOALS)
.SILENT: ${MAKECMDGOALS}


build:
	chmod +x mkdocs/scripts/build.sh
	FETCH_DEPENDENCIES=1 mkdocs/scripts/build.sh

run:
	echo "Starting dev-server on http://localhost:8000/"
	make build
	docker run \
		-it \
		--rm \
		-p 8000:8000 \
		-v ${PWD}/mkdocs:/docs \
		squidfunk/mkdocs-material:7.2.4
