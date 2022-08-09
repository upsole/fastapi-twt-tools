# TWT-TOOLS WEB API

FastAPI implementation of my library [twt-tools](https://github.com/upsole/twt_tools)

## Routes

- GET `/ok` 
Simple healthchecl

- GET `/thread/{id}` 
id is expected to be the tweet id of the last tweet in the thread.

Returns PDF file stream.

- GET `/user/archive`
Expects params (user) id and limit.
Returns the user's archive up to limit in HTML format

## .env
`PORT` and `HOST` are needed for basic functionality.
You need to set up `CORS_ORIGIN` if you intend to use it with a  frontend application
`COMPOSE_PORT` is used by docker compose.

### Docker and Nginx
`nginx` contains some lightweigth config for a reverse proxy with rate limiting
capabilities. Swap $DOMAIN_NAME with your domain and replace the files in your 
server nginx directory.

The API is dockerized and ready to be run after filling .env 
