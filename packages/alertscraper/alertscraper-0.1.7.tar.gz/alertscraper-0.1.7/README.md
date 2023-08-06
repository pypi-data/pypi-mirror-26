# alertscraper

![alertscraper badge](https://badge.fury.io/py/alertscraper.png)

![travis badge](https://travis-ci.org/michaelpb/alertscraper.png?branch=master)

General purpose flexible tool for scraping a given URL for a certain type of
items, and then email if new items are added. Useful for monitoring ad or
auction websites. Could also be useful for setting up email alerts on your own
site.

# WARNING

* Check the Terms of Service of the site before you use this tool! For some
  sites, using this tool may violate their terms of service, and should not be
  used.

# Limitations

* This code ONLY scrapes based on the initial HTTP request. Websites that
  function as single-page apps will not work. This could be supported in the
  future using JSON, or integrating with something heavier weight like
  Selenium.

# Usage

## Installation

Assuming Python's `pip` is installed (for Debian-based systems, this can be
installed with `sudo apt-get install python-pip`), alertscraper can be installed
directly from PyPI:

```
pip install alertscraper
```

Python versions 3.3+ (and 2.6+) are supported and tested against.

## Quick start

`alertscraper` is based on URLs, and maintains a history file for each URL
that you scrape so it knows when something is new.

Start by navigating in your web-browser to the website you want to scrape, and
then copying and pasting the URL. Then, inspect the page source of the site and
see if you can figure out the DOM path to the relevant element. In this case,
it was a `li` element with the class name `result` so the combined thing
becomes `li.result`.

```
alertscraper 'https://some-site.org/?query=guitar&maxprice=550' li.result
```

This will download the given URL and list the text content of each item
specified. This lets you know your query is correct.

Now we want to save this to a database file, that is, say that "I've seen
everything currently posted and am only now interested in new stuff".

```
alertscraper 'https://some-site.org/?query=guitar&maxprice=550' li.result --file=guitars.txt
```

Notice that it prints out again all the links it found.  If we were to run the
command again, it would not print them out since it will have stored them as
"already seen".

Finally, lets run the command to email us everything that has not yet been seen.

```
alertscraper 'https://some-site.org/?query=guitar&maxprice=550' li.result --file=guitars.txt --email=myemail@gmail.com
```

This only runs once. If you want it to run continually, I'd recommend putting
it in a cronjob. Eventually I may add a daemon mode, but this is good for now.

Happy scraping!

# Contributing

* [CONDUCT.md](CONDUCT.md)

New features, tests, and bug fixes are welcome!
