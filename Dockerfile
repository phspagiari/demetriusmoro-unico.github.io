FROM squidfunk/mkdocs-material:7.2.2

# copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# start dev-server on the given port-env
WORKDIR /docs
ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint.sh"]
