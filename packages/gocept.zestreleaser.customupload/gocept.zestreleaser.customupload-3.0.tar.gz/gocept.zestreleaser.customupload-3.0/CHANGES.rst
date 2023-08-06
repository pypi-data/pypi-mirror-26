Changelog
=========

3.0 (2017-11-20)
----------------

- Support non-default port numbers for scp and sftp
  [erral]

- Claim support for Python 3.6 and PyPy3.

- Drop support for Python 2.6 and 3.3.


2.0 (2015-11-18)
----------------

- Move repos to https://bitbucket.org/gocept/gocept.zestreleaser.customupload

- Make tests compatible to ``zest.releaser >= 3.51``.

- Claim Python 3.3 to 3.5 and PyPy support, thus requiring
  ``zest.releaser >= 5.0``.

- Drop Python 2.5 support.

1.4 (2012-07-31)
----------------

- If the destination URL contains username and password, do not display the
  password on the console when asking for upload.

- Allow options in HTTP(S) PUT (WebDAV) upload.

- Added some trove classifiers to indicate suported Python versions.


1.3 (2012-05-15)
----------------

- Allow uploading via SFTP (patch by Godefroid Chapelle <gotcha@bubblenet.be>).


1.2.1 (2012-05-07)
------------------

- Fixed documentation of SCP upload configuration.


1.2 (2012-01-20)
----------------

- Add second plugin point that builds and uploads documentation


1.1.0 (2011-11-18)
------------------

- Allow uploading via HTTP PUT (WebDAV) [CZ].


1.0.3 (2011-11-11)
------------------

- Make matching package names case insensitive [bug reported by
  maurits@vanrees.org].


1.0.2 (2010-07-22)
------------------

- Upload everything from the dist/ directory, so it works for any egg format,
  .zip, .tar.gz, .egg, or else [suggestion by maurits@vanrees.org].


1.0.1 (2010-07-22)
------------------

- Added a MANIFEST.in so that the created egg actually works.


1.0 (2010-07-22)
----------------

- first release [WS].
