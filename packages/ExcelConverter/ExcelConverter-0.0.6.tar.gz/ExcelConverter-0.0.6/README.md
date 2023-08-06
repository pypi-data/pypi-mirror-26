# README #

### What is this repository for? ###
Convert an excel file to python code.

### How do I get set up? ###
pip install virtualenv
cd python
virtualenv -p <path>/python3.4 env
MAC:
source NameofEnv/bin/activate
Windows:
cd env/Scripts/activate
pip install -r requirements.txt

Don't forget to update the requirements.txt file when changing/adding any dependencies.
Use: pip freeze -l > requirements.txt

## Setup in IntelliJ:
1) Install PyCharm Python plugin.
2) Add existing virtual env, see: https://www.jetbrains.com/help/idea/2017.1/adding-existing-virtual-environment.html
3) Add the python folder as "source folder" (right mouse button on folder: "Mark Directory As").


## For further info https://github.com/pypa/twine#id2
## Distribute package to pypi(pip)
1) pip install twine
2) python setup.py sdist
3) Twine upload dist # Make sure dist at the top level directory
4) Username and password can be found in the info.pypirc

### Who do I talk to? ###
Ed Bras
Dave van Rijn
Matthijs Kruger
Casper van Vliet