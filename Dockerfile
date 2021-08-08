FROM squidfunk/mkdocs-material:7.2.2

# set workdir 
WORKDIR /mkdocs

# mkdocs base file
COPY mkdocs/conf.yml .
COPY mkdocs/pre-build.sh .
RUN chmod +x pre-build.sh

# entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# start dev-server on the given port-env
ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint.sh"]
