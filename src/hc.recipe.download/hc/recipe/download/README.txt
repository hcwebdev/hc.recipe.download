==========================
hc.recipe.download package
==========================

.. contents::

What is hc.recipe.download ?
============================

Download files and packages to a local directory.

How to use hc.recipe.download ?
===============================

The recipe downloads from an http server::

  >>> server_data = tmpdir('server_data')
  >>> write(server_data, 'file1.txt', 'test1')
  >>> write(server_data, 'file2.txt', 'test1')
  >>> write(server_data, 'file3.txt', 'test1')
  >>> write(server_data, 'file4.txt', 'test1')

  >>> server_url = start_server(server_data)

We need some buildout vars::

  >>> write('buildout.cfg', '''
  ... [buildout]
  ... parts=test1
  ...
  ... [test1]
  ... recipe=hc.recipe.download
  ... urls=
  ...       %(server_url)s/file1.txt
  ... base_url=%(server_url)s
  ... files=
  ...       file2.txt
  ...       file3.txt
  ... ''' % dict(server_url=server_url))


Now we can download the files::
  
  >>> print system(buildout)
  Installing test1.
  test1: Creating download directory: /sample-buildout/downloads
  <BLANKLINE>



It works::

  >>> ls(sample_buildout, 'downloads')
  - file1.txt
  - file2.txt
  - file3.txt


  >>> ls(sample_buildout, 'parts', 'test1')
  - file1.txt
  - file2.txt
  - file3.txt


Another attempt::

  >>> write('buildout.cfg', '''
  ... [buildout]
  ... parts=test2
  ...
  ... [test2]
  ... recipe=hc.recipe.download
  ... urls=
  ...   http://www.example.com/file4.txt
  ... find-links=%(server_url)s
  ... ''' % dict(server_url=server_url))


Now we can fetch some urls::
  
  >>> print system(buildout)
  Uninstalling test1.
  Installing test2.
  <BLANKLINE>


It removes the old files and downloaded the new file::

  >>> ls(sample_buildout, 'downloads')
  - file1.txt
  - file2.txt
  - file3.txt
  - file4.txt

  >>> ls(sample_buildout, 'parts')
  d test2

  >>> ls(sample_buildout, 'parts', 'test2')
  - file4.txt


Another attempt::

  >>> write('buildout.cfg', '''
  ... [buildout]
  ... parts=test3
  ...
  ... [test3]
  ... recipe=hc.recipe.download
  ... urls=
  ...   http://www.example.com/file1.txt
  ...   http://www.example.com/file2.txt
  ... find-links=%(server_url)s
  ... ''' % dict(server_url=server_url))


Now we will reuse the cached copies::
  
  >>> print system(buildout)
  Uninstalling test2.
  Installing test3.
  test3: Using a cached copy from /sample-buildout/downloads/file1.txt
  test3: Using a cached copy from /sample-buildout/downloads/file2.txt
  <BLANKLINE>


It removes the old files and downloaded the new file::

  >>> ls(sample_buildout, 'downloads')
  - file1.txt
  - file2.txt
  - file3.txt
  - file4.txt

  >>> ls(sample_buildout, 'parts')
  d test3

  >>> ls(sample_buildout, 'parts', 'test3')
  - file1.txt
  - file2.txt



