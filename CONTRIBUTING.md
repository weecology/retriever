# Contributing to the Data Retriever

We welcome contributions of all kinds including improvements to the core code,
addition of new dataset scripts to add new datasets to the Retriever,
improvements to the documentation, bug reports, or anything else you can think
of. We strive to be supportive of anyone who wants to contribute, so don't be
shy, give it a go, and we'll do our best to help.  One way to ease into
contributing is to
[add datasets](https://retriever.readthedocs.io/en/latest/scripts.html) to the
Retriever.

## Process for contributing changes

We use a standard
[GitHub flow](https://guides.github.com/introduction/flow/index.html) for
development and reviewing contributions. Fork the repository. Make changes to a
branch of your fork and then submit a pull request.


## Running the tests

We use [nose](https://nose.readthedocs.org/en/latest/) for testing. To run the
tests first install nose using pip:

`pip install nose`

Then from the root of the repository install the Retriever:

`python setup.py install`

and run the tests:

`nosetests`

You should see a bunch of output from the Retriever followed by something like:

```
.....................
----------------------------------------------------------------------
Ran 32 tests in 143.621s

OK
```

Tests for MySQL and PostgreSQL require properly configured database management
systems for testing.

### Postgres setup

Requires that the `postgres` user has permissions on a database named `testdb`
from `localhost`. This login information should be stored in the [postgreSQL
password file](http://www.postgresql.org/docs/9.1/static/libpq-pgpass.html).


### MySQL setup

Requires that the `travis` user has permissions on a database named `testdb`
from `localhost`.


## Continuous integration

We use [Travis CI](https://travis-ci.org/) for continuous integration
testing. All pull requests will automatically report whether the tests are
passing.

Our postgreSQL tests fail idiosyncratically on Travis, so if only the postgres
tests are failing it on Travis, and they are passing locally, it is likely not a
problem.
