FROM squidfunk/mkdocs-material:7.2.4

# update pip
RUN python3 -m pip install --upgrade pip

# mkdocs base conf
RUN mkdir -p /mkdocs
COPY mkdocs /mkdocs
RUN chmod +x /mkdocs/scripts/build.sh
RUN chmod +x /mkdocs/scripts/docker.sh

# start dev-server on the given port-env
WORKDIR /mkdocs
ENTRYPOINT ["/bin/sh"]
CMD ["/mkdocs/scripts/docker.sh"]
