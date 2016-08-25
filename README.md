NZ: A Newznab API Command-Line Interface
========================================

Welcome to `nz`, a simple command line interface to
[Newznab](http://www.newznab.com) servers using the [Newznab Web
API](http://newznab.readthedocs.io/en/latest/misc/api/).

Installation
------------

To install, simply clone the repository, and run `pip install` on it. If you'd
like to avoid having `nz` installed in your system version of Python, I'd
recommend using [pipsi](https://pypi.io/project/pipsi/) to install it instead.

Configuration
-------------

The `nz` command takes and `--endpoint` and an `--apikey` argument, but these
two configurations can be loaded from the `NZ_ENDPOINT` and `NZ_APIKEY`
environment variables, to improve your user experience.

Usage
-----

As of the current release, here is the output of `nz --help`:

```
Usage: nz [OPTIONS] COMMAND [ARGS]...

  Command line interface to Newznab API endpoints.

Options:
  --endpoint TEXT  The Newznab API endpoint to use.  [required]
  --apikey TEXT    API key for your Newznab endpoint.  [required]
  --debug          Enable debug
  --version        Show the version and exit.
  --help           Show this message and exit.

Commands:
  categories  Category related commands.
  nzb         Commands for a particular NZB.
  search      Search for content.
```

License
-------

This repository is released under the [GNU GPL Version 3
license](https://www.gnu.org/licenses/gpl-3.0.txt).
