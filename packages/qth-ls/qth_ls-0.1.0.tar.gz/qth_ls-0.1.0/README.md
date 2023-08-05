Qth `ls`
========

A library for watching Qth registrations in `meta/ls/`.

This library is intended for 'meta' Qth clients, such as Qth Alias, which
need to track the registration of Qth paths over time. Qth `ls` presents a
fairly minimal API. In brief:

* `qth_ls.Ls(qth_client, loop)`: Creates a Qth `Ls` object.
* `ls.watch_path("qth/path/here", callback)`: Call `callback` when the path's
  registration changes, providing the list of registrations for that path or
  `None`.
* `ls.unwatch_path("qth/path/here", callback)`: Unregister a callback.

(See the [docstrings](./qth_ls/__init__.py) for details.)

The library takes care of messy details such as subscribing to and checking all
subpaths, for example for `foo/bar/baz` it will check `meta/ls/`,
`meta/ls/foo/` and `meta/ls/foo/bar/`.
