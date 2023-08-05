======
 Lore
======

Lore is a python data science framework to design, fit, and exploit data science models from development to production. It codifies best practices to simplify collaborating and deploying models developed on a laptop with Jupyter notebook, into high availability distributed production data centers.


Why?
----
Writing code with a fast feedback loop is fulfilling. With complex data, you can spend hours, days, then weeks iterating through more complex edge cases on larger samples until the last bits are smoothed over. Instead of spending time partially reimplementing common patterns, frequent challenges should be solved once, and thoroughly.




A model in 5 minutes
--------------------

::

$ pip install lore

$ lore init my_project  #  create file structure
$ cd my_project

$ lore install  #  setup dependencies in virtualenv
$ lore test  # make sure the project is in working order

$ lore generate my_model  #  create a model
$ lore fit my_model  #  train the model

$ lore api &  # start a default api process
$ curl -X POST -d '{"feature_1": "true"}' http://0.0.0.0:3000/my_model
  {class: "positive"}


Python Modules
==============
Lore provides python modules to simplify and standardize Machine Learning techniques across multiple libraries.

Core Functionality
------------------
* **Models** are compatibility wrappers for your favorite library (keras, xgboost, scikit). They come with reasonable defaults for rough draft training out of the box.
* **Pipelines** fetch, encode, and split data into training/test sets for models. A single pipeline will have one Encoder per feature in the model.
* **Encoders** operate within Pipelines to transform a single feature into an optimal representation for learning.
* **Transformers** provide common operations, like extracting the area code from a free text phone number. They can be chained together inside encoders. They efficiently

Supporting functionality
------------------------
* **io.Connection** allows querying data from postgresql/redshift.
* **Serializers** persist models with their pipelines and encoders to disk, or s3.
* **Caches** save intermediate data, sometimes for reproducibility, sometimes for performance.

Utilities
---------
* **Logger** writes per environment (development/test/production) to ./logs/ + console if present + syslog in production
* **Timer** writes to the log in development or librato in production*


On the shoulders giants
===================================

Lore is designed to be as fast and powerful as the underlying libraries.
It seamlessly supports workflows that utilize:

* Keras/Tensorflow + Tensorboard
* XGBoost
* Scikit-Learn
* Jupyter Notebook
* Pandas
* Numpy
* Matplotlib
* SQLAlchemy, psychopg
* virtualenv, pyenv, python (2.7, 3.3+)


Commands
========

$ lore init
$ lore install [--upgade]
$ lore generate [**all**, api, model, notebook, task] NAME
$ lore test
$ lore console
$ lore api


Project Structure
=================

::

├── .env.template            <- Template for environment variables for developers (mirrors production)
├── runtime.txt              <- keeps dev and production in sync (pyenv or buildpack)
├── README.rst               <- The top-level README for developers using this project.
├── requirements.txt         <- keeps dev and production in sync via pip, managed w/ lore install
│
├── data/                    <- caches and intermediate data from pipelines
│
├── docs/                    <- generated from src
│
├── notebooks/               <- explorations of data and models
│       └── my_exploration/
│            └── exploration_1.ipynb
│
├── logs/
│   ├── development.log
│   └── test.log
│
├── models/                  <- persisted trained models
│
├── my_project/
│   ├── __init__.py          <- environment, logging, exceptions, metrics initializers
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── my_model.py      <- external entry points to my_model
│   │
│   ├── extracts/
│   │   └── my_model.sql     <- a query to fetch features for my_model's pipeline
│   │
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── my_model.py      <- define the pipeline for my_model
│   │
│   └── models/
│       ├── __init__.py
│       └── my_model.py      <- inherits and customized multiple lore base models
│
└── tests/
    ├── data/                <- test caches and intermediate data from pipelines
    ├── models/              <- persisted models for tests
    ├── mocks/               <- mock code to stub out models/pipelines etc
    └── unit/                <- unit tests for my_model



Design Philosophies & Inspiration
=================================

* Personal Pain
* Minimal Abstraction
* No code is better than no code (https://blog.codinghorror.com/the-best-code-is-no-code-at-all/)
* Convention over configuration (https://xkcd.com/927/)
* Sharp Tools (https://www.schneems.com/2016/08/16/sharp-tools.html)
* Rails (https://en.wikipedia.org/wiki/Ruby_on_Rails)
* Cookie Cutter Data Science (https://drivendata.github.io/cookiecutter-data-science/)
* Gene Roddenberry (https://www.youtube.com/watch?v=0JLgywxeaLM)
