# KCK
KCK (or the Knowledge Construction Kit) is a framework, like Ruby-on-Rails, Django or
Laravel, but instead of making it easy to build data-driven web-sites, KCK manages the
data for data-driven applications and makes the data available fast.

## Features
* **Sophisticated data pipelines can be written simply.**  Folks with SQL chops can
  build a backend for their new React application in an afternoon.  With a little
  Python, it's pretty straightforward to turn petabytes of corporate data into
  simple statistics for the C-level dashboard.
* **It's really fast.**  KCK manages data flowing in and out of Postgres so it can keep
  its stable of data products up-to-date, but it serves data from a cache built on
  Cassandra and the data gets to the application immediately so long as it's in the
  cache.  And KCK helps make sure the data is in the cache and fresh, before an
  application needs it.
* **Plays well with others.**  KCK makes it easy to use SQL and SQLAlchemy, but it's
  Django-friendly too and it'll happily accept data from any source you can talk to
  with Python.
* **Includes HTTP Server with JWT.** KCK is accessible via an include HTTP server that
  can optionally use JWT to authenticate clients.
* **Makes tiny database servers look fast.** Seriously. KCK reduces database pressure
  to a minimum, then it spreads it out so your database writes don't have to compete
  with a deluge of read traffic from your web servers and background tasks.  And cached
  writes are on the TODO list.
* **Designed to scale.** Both the HTTP servers and the Cassandra cluster on which KCK
  depends can scale horizontally.

## Status
None of this code should be used in production.

With that said, the core parts are the cache, the http service, the refresh worker, and
the process worker.  The status of each is detailed below.

### The cache
The cache is working and it's pretty nifty.  Cache misses can cause _primers_ to fire,
returning the data and storing it in the cache on the way out so it'll be more quickly
available the next time it's requested.  Cache entries can be invalidated or they can be
set to expire after a certain amount of time.  *But cache entries can also be automatically
refreshed as data is updated, or at a set interval, or even when the system boots up.*

### The HTTP service
The HTTP service is working.  It's very basic, just a /fetch and an /update and,
optionally, JWT authentication so it can be used as a backend for mobile apps or
newer Javascript web apps made with React or Angular. So there's a lot of power
in a pretty simple wrapper and it's easily consumed by other services, languages,
etc.

### The refresh and process workers are _in-progress_
To be fully-functional, there needs to be a refresh worker and a process worker running and
neither of those are working yet.

The process worker is pretty simple and a good chunk of use cases don't require it at all.
It mostly just needs to run a single method every so often so that will go quickly once
I sit down to write it.

The refresh worker, unfortunately, is more important than the process worker, so I'm
working on it first.  I've just completed an overhaul of the background refresh queue
code and it's working in a very simple way, but it needs to be scalable and it needs
to choose tasks to refresh a bit more carefully than it currently does before it's
performing up to spec.  So it's still a few weeks out.

## System overview
Every piece is scalable and the most user-facing components are the most scalable.
The diagram below shows the basics of the KCK system structure.



![Scaling KCK](misc/kck_system_design.png)

