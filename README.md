# Activity Book Generator Back-end

## Quickstart

```shell
# Clone
git clone git@gitlab.doc.ic.ac.uk:g216002122/activity-book-generator-back-end.git
cd activity-book-generator-back-end

# Set up python virtual environment
python3 -m venv venv
. venv/bin/activate
pip3 install --upgrade pip && pip3 install -r requirements.txt

# Tell Flask where to find the app
export FLASK_APP=activitygen

# Use development environment
export FLASK_ENV=development

# Run app
flask run
```

## Testing

Run tests using `pytest`. Add `-v` for more details.

Measure code coverage using `coverage run -m pytest`.
Or for a coverage report, run `coverage report`.
