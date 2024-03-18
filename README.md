# Mastodon bot that toots gigs in Sydney

## Run Local

`pip install -r requirements.txt`

`cp .env.example .env.prod`

Edit `.env.prod` with server url and app token.

`set -o allexport; source .env.prod; set +o allexport; ./gigs.py`