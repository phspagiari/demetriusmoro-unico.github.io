FROM squidfunk/mkdocs-material:7.2.2

# mkdocs base conf
RUN mkdir -p /mkdocs
COPY mkdocs-conf /mkdocs
RUN chmod +x /mkdocs/pre-build.sh
RUN chmod +x /mkdocs/entrypoint.sh

# start dev-server on the given port-env
WORKDIR /mkdocs
ENTRYPOINT ["/bin/sh"]
CMD ["/mkdocs/entrypoint.sh"]
