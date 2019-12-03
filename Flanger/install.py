import os

os.system('python setup.py bdist_wheel')
os.system('pip install -U dist/Flanger-0.0.1-py3-none-any.whl')
