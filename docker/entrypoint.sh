#/bin/sh

# run dev-server on the provided port
mkdocs \
    serve \
    --dev-addr=0.0.0.0:$PORT
