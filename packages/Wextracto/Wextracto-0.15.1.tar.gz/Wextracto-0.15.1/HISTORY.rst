.. :changelog:

Release History
---------------

0.15.1 (2017-10-24)
+++++++++++++++++++

  * Add warc_protocol, warc_version, warc_headers to wex response
  * Some (partial) support for Python 2.6


0.14.1 (2017-08-17)
+++++++++++++++++++

  * Fix errors in PhantomJS responses
  * Handle non utf-8 urls


0.14.0 (2017-07-10)
+++++++++++++++++++

  * Ensure utf-8 is tried first even if not declared


0.12.0 (2017-04-03)
+++++++++++++++++++

  * Support onInitialized in PhantomJS required modules


0.10.1 (2016-09-26)
+++++++++++++++++++

  * Add --label argument for easy process-wide labelling


0.9.6 (2016-09-09)
++++++++++++++++++

  * Fix shutdown error caused by daemon thread for timeout with phantomjs
  * Fix handling of directories in tarfiles read from stdin (-)


0.9.5 (2016-09-06)
++++++++++++++++++

  * Small fix to avoid non-integer status code when error occur with PhantomJS


0.9.4 (2016-06-21)
++++++++++++++++++

  * Support 'params' keyword argument on URL.get


0.9.2 (2016-05-13)
++++++++++++++++++

  * Fix bug in handling HTML comments when fixing numeric character references


0.9.1 (2016-04-26)
++++++++++++++++++

  * Fix bug when using nested Cache objects


0.9.0 (2016-04-16)
++++++++++++++++++

  * Add support for reading WARC response format


0.8.8 (2016-04-11)
++++++++++++++++++

  * Fix bug in handling of invalid numeric character references


0.8.5 (2015-12-07)
++++++++++++++++++

  * Allow utf-8 in HTTP headers (only applies to PY2)


0.8.3 (2015-09-23)
++++++++++++++++++

  * Fix bug in HTTP decode caused by magic bytes handling.


0.8.2 (2015-09-21)
++++++++++++++++++

  * Add magic_bytes to Response for more reliable wex.http:decode behaviour.


0.7.9 (2015-08-18)
++++++++++++++++++

  * Re-worked encoding for HTML to pre-parse


0.7 (2015-06-04)
++++++++++++++++++

  * Better proxy support

0.4 (2015-02-12)
++++++++++++++++++

  * Now we flatten labels and values.
  * href and src become href_url and src_url.

0.3 (2014-12-29)
++++++++++++++++++

* Some API changes + switch to "tab-separated JSON".

0.2.2 (2014-10-24)
++++++++++++++++++

* Uploaded sdist to PyPI for "pip install wextracto" simplicity.

0.1 (2014-10-16)
++++++++++++++++++

* Initial release as open source
