#/bin/sh

# run build script
cd /
cp /synced/nav.yml /mkdocs/nav.yml
sh /mkdocs/scripts/build.sh

# creates symlink to synced folder
cd /mkdocs/docs
rm *.md
rm -rf doc
ln -s /synced/doc doc

# run dev-server on the provided port
cd ..
mkdocs \
    serve \
    --dev-addr=0.0.0.0:$PORT
