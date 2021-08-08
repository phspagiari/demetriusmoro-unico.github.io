#/bin/sh

# run pre-build script
cp /synced/nav.yml nav.yml
./pre-build.sh

# creates symlink to synced folder
cd docs
ln -s /synced/doc doc

# run dev-server on the provided port
cd ..
mkdocs \
    serve \
    --dev-addr=0.0.0.0:$PORT
