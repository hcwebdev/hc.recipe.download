# -*- coding: utf-8 -*-
"""Recipe for downloading files and packages"""

import os
import shutil
import urlparse
import urllib
import tempfile

import zc.buildout

import logging

TRUE_VALUES = ('yes', 'true', '1', 'on')

class Recipe(object):
    """zc.buildout recipe"""
    
    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(self.name)
        
        raw_urls    = options.get('urls', '').split('\n')
        base_url    = options.get('base_url', '')
        files       = options.get('files', '').split('\n')
        if base_url and files:
            raw_urls.extend(['%s/%s' % (base_url, f.strip()) for f in files if f])
        
        find_links  = options.get('find-links', '').split('\n')
        self.find_links = [l.strip() for l in find_links if l.strip()]
        
        buildout['buildout'].setdefault(
            'download-cache',
            os.path.join(buildout['buildout']['directory'], 'downloads'))
        
        options.setdefault(
            'destination', 
            os.path.join(buildout['buildout']['parts-directory'], name))
        
        options['location'] = options['destination']
        self.offline = buildout['buildout'].get('offline', 'false').strip() in TRUE_VALUES
        self.install_from_cache = buildout['buildout'].get('install-from-cache', 'false').strip() in TRUE_VALUES
        
        self.urls = []
        for url in raw_urls:
            if not url: continue
            try:
                _, _, urlpath, _, _, _ = urlparse.urlparse(url)
                self.urls.append([url, urlpath.split('/')[-1]])
            except IndexError:
                self.logger.error('Unable to parse URL: %s' % url)
                raise zc.buildout.UserError('Invalid URL')
    
    
    def install(self):
        """Installer"""
        options         = self.options
        download_dir    = self.buildout['buildout']['download-cache']
        destination     = options.get('destination')

        if not os.path.isdir(download_dir):
            self.logger.info('Creating download directory: %s' % download_dir)
            os.makedirs(download_dir)
        
        for url, filename in self.urls:
            download_filename = os.path.join(download_dir, filename)
            file_exists = os.path.exists(download_filename)
            
            if self.install_from_cache or self.offline:
                if not file_exists:
                    self.logger.error('Unable to download file in offline mode. Either '
                                      'run the buildout in online mode or place a copy of '
                                      'the file in %s' % download_filename)
                    raise zc.buildout.UserError('Offline error')
            else:
                if file_exists:
                    self.logger.info('Using a cached copy from %s' % download_filename)
                else:
                    # Download the file if we don't have a local copy
                    urllib.urlretrieve(url, download_filename)
        
        parts = []
        
        # Create destination directory
        if not os.path.isdir(destination):
            os.mkdir(destination)
            parts.append(destination)
        
        for _, filename in self.urls:
            # Simply copy the file to destination
            download_filename = os.path.join(download_dir, filename)
            shutil.copy(download_filename, destination)
            
            if not destination in parts:
                parts.append(os.path.join(destination, self.filename))
        
        return parts
    
    def update(self):
        """Updater"""
        pass
    

