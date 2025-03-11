# speer-notes

![Speer Technologies](./img/speer-banner.svg)

This is my submission to Speer Technologies Test Center.

This `README.md` file covers the details asked for in the assignment ("a README file with...").  For more technical details, please see the [service README.md file](./src/speer-notes/README.md)

## Frameworks

### hypermea
I have chosen to use a tool I created called [hypermea](https://pointw-dev.github.io/hypermea).  It is a code generation suite, and a core library, which makes creating hypermedia APIs really easy.

Given this challenge was not to create a hypermedia API, I removed that functionality - leaving a robust, feature-rich API.  I hope to show you more in the future.  But for our current purposes, to really understand this choice you have to know that **hypermea** leverages the [Python Eve](https://docs.python-eve.org/en/stable/) library, which is a subclass of [Flask](https://flask.palletsprojects.com/en/stable/).  What Eve does is focuses Flask on API creating.  It uses a pre-JSON-schema validation tool: [Cerberus](https://docs.python-cerberus.org/) to define the "domain" of an API, that is the resources it serves and their schema.  It uses this domain specification to generate Flask routes, and provides a host of features I will not enumerate here.

In short: using **hypermea** (and the supporting libraries it inherits from), a large part of the problem is solved my merely defining what a note is and what a user is (see `src/speer-notes/domain`).

This includes, but is not limited to:
* a simple to use authorization framework
* rate limiting
* creating arbitrary routes (affordances in hypermedia-world, but worked well for the requirements spelled out in this assignment)
* validation
* using MongoDB for persistence (can be configured for other DBMS's, but MongoDB is the default) - all basic CRUD operations require no specific code to implement.


### nginx
For the request throttling requirement, I leveraged the ability of nginx to do this.  It is configured in the `docker-compose.yml` set of services as a reverse proxy. with the `speer-notes` service as a `proxy_pass`.  You can configure request throttling by changing the limit rate and burst in `src/nginx/default.conf`

## Launch the service

### tl;dr

* create a virtual environment in the root of the [cloned repo](https://github.com/biscuit314/speer-notes)
* change to `src/speer-notes`
* install dependencies/tools with `pip install -r requirements`
* build the docker image with `hy docker build`
* launch the service with `hy docker up`
* change to `/src/scripts`
* run `./prepare_database`
  * If running Windows, run each of these python scripts:
  * `create_sysop.py`, `create_full_text_search_index.py`

### Prerequisites
* docker (not strictly necessary if you have an instance of MongoDB, Redis, and nginx you can configure `speer-notes` to use them, but docker makes it so much easier)
* python
* recommended: a python virtual environment manager ([virtualenv](https://virtualenv.pypa.io/en/latest/), [pyenv](https://github.com/pyenv/pyenv), or any of your choosing)

### Prepare your environment (optional)
If you have docker and just want to spin the service stack up, skip to the next section.

After you've [cloned the repo](https://github.com/biscuit314/speer-notes), I recommend you create a virtual environment in the repo folder

Then, in switch to the `src/speer-notes` folder:

```bash
pip install -r requirements
```

### Spinning up the environment
First build the image defined in the `Dockerfile`.  You can use `docker build -t speer-notes`, in the `src/` folder, or the following shortcut which can be run anywhere in the repo:

```bash
hy docker build
```

Similarly, you can launch the service stack by running `docker compose up -d` in the `src/` folder, or use the following shortcut which can be run anywhere in the repo:

```bash
hy docker up
```

On first run this will download images for nginx, MongoDB, and Redis.

Once finished, the Notes service and supporting services are up and running, listening on port 2112.

### Preparing the database
When a fresh, empty MongoDB is launched, you have to first run a one-time script: in the `src/script` folder:

```bash
./prepare_database
```

This does two things:
* provision an admin user
  * username: sysop
  * password: swordfish
* creates the full-text search index

> NOTE: the `prepare_database` script runs with `bash`  If you are on Windows, you can skip that script and just run each of the python scripts it calls:
> * `create_sysop.py`
> * `create_full_text_search_index.py`



## Run the tests

### Start the databases

In order to run the tests, an instance of MongoDB and Redis must be running, accessible by `localhost` on their default ports (27017 and 6379 respectively)

If you have the `docker-compose.yml` stack running, this meets the criteria (the tests do not use the same databases as the running service - both can run at the same time)

If you do not have the `compose` stack running you can spin up temporary instances with the following:

```bash
docker run --rm -d -p 27017:27017 --name temp-mongo mongo
docker run --rm -d -p 6379:6379 --name temp-redis redis
```

> When you are finished, the following will stop and remove these containers:
>
> ```bash
> docker stop temp-mongo
> docker stop temp-redis
> ```



### Run the tests

Change to `src/speer-notes/__test__`  Then run the following:

```bash
pytest
```

### Read the test

There are two parts to the tests used to validate `speer-notes` does what it is supposed to do.  The first are the **executable specifications** found in `src/features`

These are written in Gherkin.  As you read each file, you will see that in plain English what the service is supposed to do is clearly and unambiguously defined.  It is clear to developers as well as business analysts and product owners that if the service does all of this it is ready to ship.

Each phrase under each Scenario is a step.  The step definitions are in the `__tests__` folder.  I am using an extension to `pytest` called `pytest-bdd` which glues all of this together.

You have probably seen this before, but if not - I'm sure you will agree this is a tremendous way to gain and communicate confidence that the service does what it is supposed to do.

## Postman exports

The repo includes two files for you to import into your Postman, both in the `src/postman` folder:

* `speer-notes.postman_environment.json` 
  * defines a variable `{{url}}`
  * to switch between `localhost` or some other location, you have one change to make for the entire collection to use the new location
* `Speer Technologies - Notes API.postman_collection.json` 
  * contains a number of requests to let you explore the URL space provided by the service.
  * Each folder has brief notes to guide you through, and each request is sensibly named

## My deployment

I have deployed an instance of the service, accessible to you from the following base URL:

```plaintext
https://speer-notes.pointw.com
```

This instance is empty except for the user `sysop` as provisioned with the `create_sysop.py` script mentioned above.

The easiest way to use it is to change the `{{url}}` variable in Postman to the above.

> NOTE: if using `curl` be sure to add the `-L` option which tells `curl` to follow redirects.
