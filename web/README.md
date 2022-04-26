# Develop for the web interface

Start the development container:

```
$ make run-dev
```

Inside the container, start the server:

```
PYTHONPATH=/build/zmifanva/web pserve --reload /build/zmifanva/web/development.ini
```

The `pserve` tool automatically restarts the server after a change in Python files.

The web tool connects to the translation services. Start them:

```
$ make run-jb-en
$ make run-en-jb
```
