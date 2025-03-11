# speer-notes

![Speer Technologies](../../img/speer-banner.svg)

## Introduction

Here is a brief summary of how the code is organized.

### Repo structure

```plaintext
speer-notes/
├── img/                                      # Speer logos
├── README.md
└── src/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── features/                             # location of the Gherkin files - when reading the tests, start here
    ├── nginx/                                # request throttling is configured here
    ├── postman/                              # export files from my Postman collection and environment
    ├── scripts/
    │   ├── prepare_database                  # run this on an empty database
    │   ├── create_sysop.pytest               # creates the first admin user
    │   ├── create_full_text_search_index.py
    │   └── rate_limit_test.py
    └── speer-notes
        ├── affordances/                      # where non-domain endpoints are defined (auth, share, search)
        ├── auth/
        │   ├── auth_handlers.py              # where a token is converted to claims
        │   └── authorization.py              # where claims are considerd in granting access per resource/method
        ├── configuration/
        │   ├── hypermea_settings.py          # the set of runtime configuration parameters out-of-the-box
        │   └── api_settings.py               # where additional runtime configuration parameters can be defined
        ├── domain/                           # notes and users are defined here, auto-generating the basic CRUD routes
        ├── hooks/                            # code that fires before/after various events
        ├── integration/                      # where configuring additional/external services (e.g. Redis, S3, auth0...)
        ├── _env.conf                         # override envars for developer (excluded by .gitignore)
        ├── run.py                            # launch the service with this
        ├── hypermea_service.py               # the definition of the service class
        ├── README.md                         # you are reading this file now
        ├── requirements.txt
        ├── pytest.ini
        ├── settings.py                       # Eve settings
        ├── validation                        # where you would create custom schema types and other validations
        └── __tests__                         # the step definitions for the features mentioned above
```

### Rate limiting

The rates are configured by environment variables.  The value for each of the following must be in the form of

`(number of requests , time window in seconds)`

e.g.
```bash
HY_RATE_LIMIT = (300, 900)  # 300 requests every 15 minutes
```

You can include arithmetic expressions for readability

e.g.
```bash
HY_RATE_LIMIT = (300, 60 * 15)  # 300 requests every 15 minutes
```

This will set the rate for all `GET`, `POST`, `PATCH`, and `DELETE` requests.  If you only want to set the rate for one of these methods, e.g. `GET`:

```bash
HY_RATE_LIMIT_GET = (300, 60 * 15)  # 300 requests every 15 minutes
```

When using `HY_RATE_LIMIT` and a method specific version, the method specific version takes precedence.

Each response includes the following custom headers so a client can track how close they are to the limit:

| Header                | Description                                                                                                     |
| ----------------------| --------------------------------------------------------------------------------------------------------------- |
| X-RateLimit-Remaining | How many requests are remaining before hitting the limit                                                        |
| X-RateLimit-Limit     | What the limit is                                                                                               |
| X-RateLimit-Reset     | A julian date of when the remaining count is reset (or when the block will be removed if the limit is exceeded) |


### Request throttling

In addition to the configuration mentioned below, this service stack (which uses nginx to implement request throttling) has this additional configuration step:

Here is the current contents of `src/nginx/default.conf`

```plaintext
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=1000r/s;

server {
    listen 2112;

    location / {
        limit_req zone=api_limit burst=200 nodelay;
        proxy_pass http://speer-notes:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```

There are two values you can change to adjust request throttling:

* `limit_req_zone $binary_remote_addr zone=api_limit:10m rate=1000r/s;` (line 1)
* `limit_req zone=api_limit burst=200 nodelay;` (line 7)

Please [read the nginx docs](http://nginx.org/en/docs/http/ngx_http_limit_req_module.html) for more information.

> NOTE: using a docker volume to supply nginx with configuration is a shortcut I used for this assignment.  In production I would use template/keyword replacement so DevOps has a consistent way to configure all services in the stack - especially important when using `k8s`!

### Additional notes

* I implemented `/api/notes/:id/share` with `POST` as mentioned in the requirements.  This can be improved by making it a `PUT` instead as the operation is idempotent.
* Though not stated in the requirements, I ensured no clear-text passwords
  * passwords sha256 hashed before saving to the database
  * before hashing, the password is prepended with the username
  * it is therefore not obvious when two users happen to have the same password
  * this also prevents credential theft by copying a password into another user's record
* When you `GET` a collection (e.g. `/api/notes`) the response contains a header `X-Total-Count` which tells you how many are in the collection
  * This header also appears in a `HEAD` requests, so you can see how many notes there are without having to `GET` the entire collection


## End of introduction

The above I wrote for the Speer Test Center.  The remainder of this `README.md` was generated by **hypermea**.  It is still in beta, so what follows is about 95% accurate and 70% complete.

## Configuration

The API is configured via environment variables.  These can be set in in several ways:

* Your OS

  * `set var=value` in Windows
  * `export var=value` in Linux

* In `docker-compose.yml`

  ```yml
  environment:
   - var1=value1
   - var2=value2
  ```


* In Kubernetes
  ```bash
  spec:
    containers:
      - name: speer-notes
        image: speer-notes
        env:
          - name: var1
            value: value1
  ```
  
* In `_env.conf` (this is useful to set values for use in your IDE, this file is listed in `.gitignore` and `.dockerignore` - lines that begin with `#` are treated as comments)  Takes precedence over OS envars.

  ```bash
  var1=value1
  var2=value2
  ```

The base variables are prefixed with HY_ .  The environment variables you can set are:

| Variable                  | Description                                                  | Default                                                     |
| ------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| HY_API_NAME               | The name of your API.  Appears in logs and emails.           | The name you used with `hypermea api create` (i.e. speer-notes)  |
| HY_MONGO_ATLAS            | Set to Enabled (or True, or Yes) to use the following Mongo values to construct the MONGO_URI.  If disabled, will use a non-Atlas connection. | Disabled  |
| HY_MONGO_HOST             |                                                              | localhost                                                   |
| HY_MONGO_PORT             | (ignored if HY_MONGO_ATLAS is enabled)                       | 27017                                                       |
| HY_MONGO_DBNAME           |                                                              | The name you used with `hypermea api create` (i.e. speer-notes)  |
| HY_API_PORT               |                                                              | 2112                                                        |
| HY_INSTANCE_NAME          | This name appears in logs and in error emails                | The hostname the API is running on (`socket.gethostname()`) |
| HY_TRACE_LOGGING          | When enabled, causes logs to include enter/exit/exception details for each method - not something to have enabled in production. | Enabled  |
| HY_PAGINATION_LIMIT       | When sending the `max_results` query string, any number greater than this is reduced to this. | 3000                       |
| HY_PAGINATION_DEFAULT     | The default number of documents sent, overridden by the `max_results` query string            | 1000                       |
| HY_LOG_TO_FOLDER          | (disable if deploying as serverless as there is no folder to log to) | Disabled                                            |
| HY_SEND_ERROR_EMAILS      | (only works if the following values are set)                 | Enabled                                                     |
| HY_SMTP_HOST              |                                                              |                                                             |
| HY_SMTP_PORT              |                                                              | 25                                                          |
| HY_ERROR_EMAIL_RECIPIENTS |                                                              |                                                             |
| REDIS_HOST                |                                                              | localhost                                                   |
| REDIS_PORT                |                                                              | 6379                                                        |
| REDIS_DB                  |                                                              | 0                                                           |


Optional environment variables

| Variable             | Description                             |
| -------------------- | --------------------------------------- |
| HY_MONGO_USERNAME    | (required if HY_MONGO_ATLAS is enabled) |
| HY_MONGO_PASSWORD    | (required if HY_MONGO_ATLAS is enabled) |
| HY_MONGO_AUTH_SOURCE | Eve pass-through                        |
| HY_MEDIA_BASE_URL    | Eve pass-through                        |
| HY_PUBLIC_RESOURCES  | not yet implemented                     |
| HY_URL_PREFIX        | If the API will be deployed behind a URL with a path, use this variable to set that path.  For example, if you deploy the API behind https://example.com/api/my_service, then set HY_URL_PREFIX to "api/my_service" |
| HY_CACHE_CONTROL     | Sets the Cache-Control header (e.g. `no-cache, no-store, must-revalidate`) |
| HY_CACHE_EXPIRES     | Sets the Cache-Expires header (value is in secods)           |
| HY_ADD_ECHO          | If enabled, an undocumented endpoint will be created whose relative path is `/_echo`.  PUT {"message": {}, "status_code: int"} to this endpoint and it will be echoed back to you and logged (`.info` if < 400, `.warning` if < 500, else `.error`).  Useful to test the behaviour of error codes (e.g. with logging configurations) |
behaviour of error codes (e.g. with logging configurations) |
| HY_ADD_ECHO          | If enabled, an undocumented endpoint will be created whose relative path is `/_echo`.  PUT {"message": {}, "status_code: int"} to this endpoint and it will be echoed back to you and logged (`.info` if < 400, `.warning` if < 500, else `.error`).  Useful to test the behaviour of error codes (e.g. with logging configurations) |
| HY_ADD_ECHO          | If enabled, an undocumented endpoint will be created whose relative path is `/_echo`.  PUT {"message": {}, "status_code: int"} to this endpoint and it will be echoed back to you and logged (`.info` if < 400, `.warning` if < 500, else `.error`).  Useful to test the behaviour of error codes (e.g. with logging configurations) |


If using auth (e.g. `hypermea api create speer-notes --add-auth` )

| Variable               | Description                                                  | Default                                          |
|------------------------| ------------------------------------------------------------ | ------------------------------------------------ |
| AUTH_ADD_BASIC         | When enabled, allows a basic authentication scheme with root/password | No                                               |
| AUTH_ROOT_PASSWORD     | When AUTH_ADD_BASIC is enabled, this is the password the root user uses to gain access to the API. | password                                         |
| AUTH_REALM             | Appears in the `WWW-Authenticate` header in unauthorized requests. | speer-notes.pointw.com                       |
| AUTH_JWT_DOMAIN        |                                                              | speer-notes.us.auth0.com                     |
| AUTH_JWT_AUDIENCE      | This is the identifier a client uses when requesting a token from the auth provider.  It is a URI only (identifier only), not an actual URL (i.e. no requests are made to it) | https://pointw.com/speer-notes               |
| AUTH0_API_AUDIENCE     | When speer-notes requests a token to use the Auth0 API, this is the audience for the token. | https://speer-notes.us.auth0.com/api/v2/     |
| AUTH0_API_BASE_URL     | The base of the Auth0 API                                    | https://speer-notes.us.auth0.com/api/v2      |
| AUTH0_CLAIMS_NAMESPACE | If you configure Auth0 to insert additional claims, use this value as a namespace (prefix). | https://pointw.com/speer-notes               |
| AUTH0_TOKEN_ENDPOINT   | When speer-notes needs to call the Auth0 API, it uses this endpoint to request a token. | https://speer-notes.us.auth0.com/oauth/token |
| AUTH0_CLIENT_ID        | When speer-notes needs to call the Auth0 API, it uses this client id/secret to authenticate.  These are not the client id/secret of your application. | --your-client-id--                               |
| AUTH0_CLIENT_SECRET    |                                                              | --your-client-secret--                           |

## Project Structure

| File                            | Description                                                                                                                                                                                                                                                         |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| hypermea_service.py                  | Defines the HypermeaService class, the http server that powers the API.                                                                                                                                                                                             |
| run.py                          | Instantiates an HypermeaService object and starts it (with SIGTERM for docker stop).                                                                                                                                                                                |
| settings.py                     | Where you set the values of Eve [global configuration](https://docs.python-eve.org/en/stable/config.html#global-configuration) settings.  Key values are provided by `configuration/__init__.py` which are overridable by environment variables (or by `_env.conf`) |
| _env.conf                       | Set temporary/dev values for settings here.  Will not be added to container build.  If not using containers, be sure not to copy this to production.                                                                                                                |
| logging.yml                     | Configuration of the Python logging module.                                                                                                                                                                                                                         |
| requirements.txt                | Standard file for listing python libraries/dependencies - install with `pip install -r requirements.txt` .                                                                                                                                                          |
| win_service.py                  | *under development* - Lets you deploy the API as a windows service.                                                                                                                                                                                                 |
| **configuration**               |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; \_\_init\_\_.py    | Settings used by the application (some set default Eve values in `settings.py` .                                                                                                                                                                                    |
| **domain**                      | Where your domain resources will be created when you use `hypermea resource create` .                                                                                                                                                                               |
| &nbsp;&nbsp; _common.py         | Fields applied to all resources (skipped if API was created with `--no_common` ).                                                                                                                                                                                   |
| &nbsp;&nbsp; _settings.py       | Defines the `/_settings` endpoint, which you GET to see the application settings.                                                                                                                                                                                   |
| &nbsp;&nbsp; \_\_init\_\_.py    | Wires up all resources and makes them available to `HypermeaService` .                                                                                                                                                                                              |
| **hooks**                       | Wires up [Eve event hooks](https://docs.python-eve.org/en/stable/features.html#eventhooks) for logging, relationship navigation, etc.                                                                                                                               |
| &nbsp;&nbsp; _error_handlers.py |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; _logs.py           |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; _settings.py       |                                                                                                                                                                                                                                                                     |
| &nbsp;&nbsp; \_\_init\_\_.py    | Add your custom hooks/routes here.                                                                                                                                                                                                                                  |
| **validation**                  | This module is added when you run `add-validation` .                                                                                                                                                                                                                |
| &nbsp;&nbsp; validator.py       | Add custom validators and/or types to the `CustomHypermeaValidator` class defined here.                                                                                                                                                                             |
| **auth**                        | This module is added when you run `add-auth` (see docs for customization details).                                                                                                                                                                                  |
| &nbsp;&nbsp; auth_handlers.py   | Where you add/modify authentication handlers, (e.g. if you wish to support Digest or custom auth scheme).                                                                                                                                                           |
| &nbsp;&nbsp; authorization.py   | Defines `HypermeaAuthorization` which provides authentication to `HypermeaService` .                                                                                                                                                                                |
| &nbsp;&nbsp; \_\_init\_\_.py    | Defines the settings used by the `auth` module.                                                                                                                                                                                                                     |
| **templates**                   | This folder is added when you run `add-websocket`.                                                                                                                                                                                                                  |
| &nbsp;&nbsp; ws.html            | Contains Javascript clients use to connect to the web socket.                                                                                                                                                                                                       |
| &nbsp;&nbsp; chat.html          | An ultra simple client you can use to test the web socket.  You should delete after testing.                                                                                                                                                                        |
| **websocket**                   | This module is added when you run `add-websocket`.                                                                                                                                                                                                                  |
| &nbsp;&nbsp; \_\_init\_\_.py    | This is where you can add web socket event handlers and/or send/emit methods to broadcast onto the socket.  It currently has 'hello world' code, including the chat application (see /templates).  You should remove these as you see fit.                          |


## Additional features

`speer-notes` is built with [hypermea](https://github.com/pointw-dev/hypermea) which enchances [Eve](https://docs.python-eve.org/en/stable/).  What follows is a list of some of the additional features.  While this document is being developed, you can learn more from its [feature documentation](https://docs.python-eve.org/en/stable/features.html).

### Pagination

* When doing a GET on a collection, the default max results is set to 1000 (change this default at deploy time by setting HY_PAGINATION_DEFAULT)

* You can override this value with a query string: e.g. `GET {features_url}?max_results=50`

* The max_results cannot exceed HY_PAGINATION_LIMIT which is currently set to 3000 (changeable at deploy time)

* The response body will contain a _meta object which lets you know if you have all of the items in the collection.  E.g. the above request had this _meta object:

  ```json
   "_meta": {
    "page": 1,
      "max_results": 50,
      "total": 3291
  }   
  ```

* If the response body did not return all items in the collection:
  * _meta.max_results will be less than _meta.total
  * You can also use the **next**, **prev**, **last** affordances (see above)

* You can jump to any page with a query string, e.g. 

  ```
  GET {features_url}?page=2
  GET {features_url}?max_results=50&page=7 
  ```

* https://docs.python-eve.org/en/stable/features.html#pagination

### Filtering

* You can filter a collection with query strings, e.g. GET `{features_url}?where=category=="Exterior Features"`
* There are two types of where values
  * Python: create a conditional expression (e.g. `field==value`, `field!=value`, `field==value1 or field==value2`)
  * Mongo: use the mongo query definition language (e.g. `{ "_updated": {"$gte": "2021-10-01"}}` )
    * Note:  When the API is behind an AWS API Gateway (as it currently is when running "serverless"), the **curly brackets must be urlencoded**.
* https://docs.python-eve.org/en/stable/features.html#filtering

### Sorting

* Not much I can add that isn't in the doc...
* https://docs.python-eve.org/en/stable/features.html#sorting)

### Optimistic Concurrency

* To change a document after it has been POST’ed, you must supply an If-Match header with the correct ETag.  

  * If you do not, you will receive a 428 Precondition Failed.
  * This applies to PATCH, PUT, DELETE requests.  

* e.g. To Change the name of a feature:

  ```
  GET {feature_item_url}
  etag = response.body._etag
  data = {"name": "New Name"}
  PATCH {feature_item_url} -H "If-Match {etag}" -d data
  ```

* If you receive a 412 Precondition Failed, that means someone else made a change between the GET and the PATCH.  The client will have to handle this as appropriate (notify the user, offer to refresh/merge, etc.)
* https://docs.python-eve.org/en/stable/features.html#data-integrity-and-concurrency-control

