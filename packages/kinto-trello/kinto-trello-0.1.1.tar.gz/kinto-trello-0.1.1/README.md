# Kinto for Trello

This project implement an authentifcation policy for [Kinto][] using [Trello][] tokens.

[kinto]: https://www.kinto-storage.org/
[trello]: http://trello.com/

## Install

    pip install kinto-trello

## Usage


    kinto.includes = kinto_trello

Config:

    multiauth.policies = trello
    multiauth.policy.trello.use = kinto_trello.authentication.FxAOAuthAuthenticationPolicy
    trello.apikey = ''

## License

MIT
