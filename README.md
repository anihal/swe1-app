# swe1-app

main: [![Build Status](https://app.travis-ci.com/anihal/swe1-app.svg?branch=main)](https://app.travis-ci.com/github/anihal/swe1-app) [![Coverage Status](https://coveralls.io/repos/github/anihal/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/anihal/swe1-app?branch=main)

Django polls app ([tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/) parts 1-4) deployed to AWS Elastic Beanstalk.

Live app: http://swe1-app-env.us-east-1.elasticbeanstalk.com/polls/

## Local development

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python manage.py migrate && python manage.py loaddata sample_polls
python manage.py runserver
```

## Checks (run by Travis CI on every push and pull request)

```
black --check .
flake8 .
coverage run manage.py test && coverage report
```
