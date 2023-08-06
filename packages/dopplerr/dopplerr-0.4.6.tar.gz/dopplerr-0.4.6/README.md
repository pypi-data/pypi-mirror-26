# Dopplerr Subtitle Downloader

[![Build Status](https://travis-ci.org/Stibbons/dopplerr.svg?branch=master)](https://travis-ci.org/Stibbons/dopplerr)
[![Docker Automated buil](https://img.shields.io/docker/build/stibbons31/dopplerr.svg)](https://hub.docker.com/r/stibbons31/dopplerr/builds/)
[![Pypi package](https://badge.fury.io/py/dopplerr.svg)](https://pypi.python.org/pypi/dopplerr/) [![PyPI](https://img.shields.io/pypi/pyversions/dopplerr.svg)](https://pypi.python.org/pypi/dopplerr/)
[![Coveralls](https://coveralls.io/repos/github/Stibbons/dopplerr/badge.svg)](https://coveralls.io/github/Stibbons/dopplerr)
[![codecov](https://codecov.io/gh/Stibbons/dopplerr/branch/master/graph/badge.svg)](https://codecov.io/gh/Stibbons/dopplerr)
[![Maintainability](https://api.codeclimate.com/v1/badges/62d3040e8e7f37e637bf/maintainability)](https://codeclimate.com/github/Stibbons/dopplerr/maintainability)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Subtitle Download Web Service for Sonarr or Radarr. It uses [Subliminal](https://github.com/Diaoul/subliminal) to search automatically for missing subtitles on download notification.

-   Free software: MIT
-   Source: <https://github.com/Stibbons/dopplerr>
-   Python 3.
-   Docker image based on Alpine Linux and S6-Overlay (based on
    [Linuxserver](https://www.linuxserver.io/)'s images)

# Limitations

- only Sonarr notification
- video filename should not have been renamed
- season folder might exist, or not
- all series should be on the same root directory
- exact series title folder (no year, no extra)

# Usage

The best usage is through the docker image.

## Installation with Docker

Use my docker image:

    docker create \
        --name dopplerr \
        -p 8086:8086 \
        -e PUID=<UID> \
        -e PGID=<GID> \
        -v <path/to/animes>:/animes \
        -v <path/to/movies>:/movies \
        -v <path/to/series>:/tv \
        -e DOPPLERR_SUBLIMINAL_LANGUAGES="fra,eng" \
        stibbons31/dopplerr

Mount your media directories in `/`. Typically, `/animes` and `/tv` are from Sonarr, and
`/movies` from Radarr.

It is a good practice to run Sonarr and Radarr in their own container, so they also "see" their
media in path such as `/tv`, `/movies`, `/animes`. Mount these volume with the same name in the
`dopplerr` container. `DOPPLERR_MAPPING` allows developers to run dopplerr directly from their
PC and allow a different naming conventions (for instance, `/path/to/Movies` is where the
movies are stored, but in all containers see it mounted as `/movies`).

### Parameters

The parameters are split into two halves, separated by a colon, the left hand side representing the host and the right the container side. For example with a port -p external:internal - what this shows is the port mapping from internal to external of the container. So, `-p 8080:80` would expose port 80 from inside the container to be accessible from the host's IP on port 8080 (Ex: `http://192.168.x.x:8080`).

Example of starting command line arguments:

-   `-p 8086:8086` - the port webinterface
-   `-v /path/to/anime:/anime` - location of Anime library on disk
-   `-v /path/to/movies:/movies` - location of Movies library on disk
-   `-v /path/to/series:/tv` - location of TV library on disk
-   `-e PGID=1000` - for GroupID. See below for explanation
-   `-e PUID=100` - for UserID. See below for explanation
-   `-e DOPPLERR_SUBLIMINAL_LANGUAGES=fra,eng` - set wanted subtitles languages (mandatory)
-   `-e DOPPLERR_GENERAL_VERBOSE=1` - set verbosity. 1=verbose, 0=silent (optional)

Developers might also use:

-   `-e DOPPLERR_GENERAL_BASEDIR=/media` - set media base directory (optional)
    (needs something like `-v /path/to/anime:/media/anime` and so on)

### User / Group Identifiers

Sometimes when using data volumes (-v flags) permissions issues can arise between the host OS and the container. We avoid this issue by allowing you to specify the user PUID and group PGID. Ensure the data volume directory on the host is owned by the same user you specify and it will "just work" (TM).

In this instance PUID=1001 and PGID=1001. To find yours use id user as below:

    $ id <dockeruser>
    uid=1001(dockeruser) gid=1001(dockergroup) groups=1001(dockergroup)

### Wanted subtitle languages

Use a comma-separated list of 3-letter language descriptors you want Subliminal to try to download them.

Example:

    DOPPLERR_SUBLIMINAL_LANGUAGES=fra,eng

Descriptors are ISO-639-3 names of the language. See the [official Babelfish table](https://github.com/Diaoul/babelfish/blob/f403000dd63092cfaaae80be9f309fd85c7f20c9/babelfish/data/iso-639-3.tab) to find your prefered languages.

## Pipy Installation

Create a dedicated virtual environment and install it properly with the following commands:

    $ pip install dopplerr

Note: Do NOT install a Python application directly in your system. Always use a Virtualenv. Or let it be handled by your distribution's maintainer (use `apt` / `yum` / ...)

# Radarr/Sonarr Configuration

Go in Settings to configure a "Connect" WebHook:

-   Settings &gt; Connect &gt; add WebHook notification
-   Select **On Download** and **On Upgrade**
-   URL: ```http://<ip address>:8086/api/v1/notify/sonarr```

    or

    URL: ```http://<ip address>:8086/api/v1/notify/radarr```
-   Method: POST

# Two READMEs ?

There is a little trick to know about READMEs:

-   Docker Hub does not render README written in restructuredText correctly
-   Pypi does not render README written in Markdown correctly

So, a restructuredText version of the README is created from `README.md` on upload to Pypi.
Simple. So, when updating `README.md`, do not forget to regenerate `README.rst` using `make readme`.

# Contributing

Check out the source code

    git clone

Install requirement system-level dependencies with (or adapt accordingly):

    $ sudo ./bootstrap-system.sh

System dependencies:

- `git`
- `make`
- `pandoc`
- `pip`
- `pipenv`

This project uses `pipenv` to jump seamlessly into a virtualenv.

Setup your development environment with:

    $ make dev

Unit Tests with:

    $ make test-unit

or run it live with

    $ make run-local

Activate the environment (to start your editor from, for example):

    $ make shell

# Publishing new version

Please note that much part is automatized, for example the publication to Pypi is done automatically by Travis on successful tag build)

Test building Wheel package with:

    $ make release wheels

Create a release: create a tag with a Semver syntax.

    $ # ensure everything is committed
    $ git tag 1.2.3
    $ make release
    $ git push --tags

Optionally you can tag code locally and push to GitHub. `make release` is also executed during the Travis build, so if there is any files changed during the build (ex: `README.rst`), it will be automatically done and so the Pypi package will be coherent. Do not retag if the README has been updated on GitHub, it has been properly done in the Wheel/Source Packages on Pypi. So, no stress.

On successful travis build on the Tag, your Pypi package will be automatically updated.

Same, on Tag, a Docker tag is also automatically created.

Note:

> According to PBR, alpha versions are to be noted `x.y.z.a1`
