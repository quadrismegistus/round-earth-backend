# round-earth-backend


## Install

### Mac

```
# install system reqs
brew install sqlite
brew install libspatialite

# configure paths
export LDFLAGS="-L$(brew --prefix sqlite)/lib"
export CPPFLAGS="-I$(brew --prefix sqlite)/include" 
export PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions"

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