# round-earth-backend


## Install

### Docker setup

```
docker run -it \
  -e PBF_URL=https://download.geofabrik.de/europe/monaco-latest.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/europe/monaco-updates/ \
  -p 8080:8080 \
  --name nominatim \
  mediagis/nominatim:4.3

```

### Mac

```
# install system reqs
brew install postgres postgis

# install python
pyenv install 3.12.1

# install repo
python -m venv venv
. venv/bin/activate
pip install -e .

```

### Linux

```
# install system reqs
sudo apt install sqlite3 libsqlite3-mod-spatialite

# configure paths
export LDFLAGS="-L/usr/local/opt/sqlite/lib -L/usr/local/opt/zlib/lib"
export CPPFLAGS="-I/usr/local/opt/sqlite/include -I/usr/local/opt/zlib/include"
export PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions" 

# install python
pyenv install 3.12.1

# install repo
python -m venv venv
. venv/bin/activate
pip install -e .
```