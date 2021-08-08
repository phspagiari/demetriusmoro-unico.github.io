#/bin/sh

# run pre-build script
cp /synced/nav.yml nav.yml
./pre-build.sh

# creates symlink to synced folder
ln -s /synced/docs docs

# run dev-server on the provided port
mkdocs \
    serve \
    --dev-addr=0.0.0.0:$PORT
