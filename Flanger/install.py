import os
import shutil

os.system('python setup.py bdist_wheel')
shutil.rmtree('./build/', ignore_errors=True)
shutil.rmtree('./Flanger.egg-info/', ignore_errors=True)

os.system('pip install -U dist/Flanger-0.0.1-py3-none-any.whl')

