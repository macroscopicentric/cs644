# Web Server Class Project

This is a toy web server written as part of the classwork (final project) for Ian Fisher's [CS644 class](https://iafisher.com/cs644/fall2025). A web server was not an officially suggested final project for this particular class session, so most of the actual exercises were filched from [his spring session of the same class](https://iafisher.com/cs644/spring2025).

## Using the web server
To actually run the web server, do:

```sh
poetry run main --run
```

To just do a simple count of the log lines (each connection's messages get saved into the log in a single line, no matter how long), you can instead do:

```sh
poetry run main --count
```

## Development
This repo uses black for formatting, to run black yourself:

```sh
poetry run black .
```
