### Installation steps
* Check if you have python3 or else download and install from https://www.python.org/downloads/
```
]$ python3 --version
Python 3.10.7
]$ 
```

* Install pyenv -- https://ggkbase-help.berkeley.edu/how-to/install-pyenv/
```
]$ pyenv --version
pyenv 2.3.9
]$ 
```

* Install Python 3.10.9 inside pyenv
```
pyenv install 3.10.9
```

* Configure local/current shell/environment to use 3.10.9
```
pyenv shell 3.10.9
export PATH=$HOME/.pyenv/shims:$PATH
```

* Install all dependencies
```
cd configurableLedgerAsset/python3
python3 -m pip install --upgrade -r requirements.txt 
```

* Start Jupyter
```
]$ cd configurableLedgerAsset/python3/
]$ export BaseDir=`pwd`; python3 -m jupyter notebook --port=9007
```

* You will get a browser -- Enjoy

