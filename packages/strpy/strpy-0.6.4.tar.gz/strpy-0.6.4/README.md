Project
-------------------
strpy: The STR Python Tools for Computer Vision and Machine Learning  
Author: Jeffrey Byrne <jeffrey.byrne@stresearch.com>  
URL: https://github.com/stresearch/strpy/  


Overview
-------------------
Systems and Technology Research Python package for computer vision and machine learning.

Creating a pypi package
-------------------
```bash
 git commit -am "message"
 git push
 git tag X.Y.Z -m "strpy-X.Y.Z"
 git push --tags origin master
```
edit setup.py to create new version

The git sequence to delete a tag
```bash
   git tag -d x.y
   git push origin :refs/tags/x.y
```

 create ~/.pypirc following https://packaging.python.org/guides/migrating-to-pypi-org/#uploading
 python setup.py register -r pypi
 python setup.py sdist upload -r pypi


MacOSX Installation Notes
-------------------
When installing strpy on MacOSX, you must use a framework build of python in order to use matplotlib, as described in:

https://matplotlib.org/faq/osx_framework.html

Install anaconda python (https://anaconda.org/anaconda/python), then:

```bash
conda install python=2.7.9 ipython
virtualenv $STRPY
source $STRPY/bin/activate
pip install matplotlib==2.0.2 opencv-python numpy scipy scikit-learn dill h5py
pythonw -m IPython  
```

replacing $STRPY with your virtual environment name.  This last step will create an ipython shell using the framework build of python (pythonw).




