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
