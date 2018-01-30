# Transit Tracker #
## Testing ##
### Fast coverage/tests ###
Within `pipenv shell` run:
```
watchmedo shell-command --patterns='*.py' --recursive --command='coverage run --source=tracker -m pytest; coverage html;'
```
In another tab run:
```
livereload htmlcov
```

## Deploying to a Raspberry Pi ##
First we need to get and build the C libraries needed to communicate with the LED strip.
```
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x.git
apt-get install scons
scons
```
Next we need to build the Python wrapper.
```
apt-get install python3-dev swig
python3 ./setup.py build
python3 ./setup.py install
```

### Run on startup ###
To get the script to start on startup add the command to run it to /etc/rc.local
