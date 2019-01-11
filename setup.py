#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
from setuptools import setup
#from distutils.core import setup

setup(
  name = 'xetrapal',         # How you named your package folder (MyLib)
  packages = ['xetrapal'],   # Chose the same as "name"
  version = '0.0',      # Start with a small number and increase it with every change you make
  license='GNU General Public License v3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automation and orchestration framework',   # Give a short description about your library
  author = u'हैकरgram',                   # Type in your name
  author_email = 'listener@hackergram.org',      # Type in your E-Mail
  url = 'https://github.com/hackergram/xetrapal',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hackergram/xetrapal/archive/0.0.tar.gz',    # I explain this later on
  keywords = ['automation', 'orchestration' ],   # Keywords that define your package best

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3.0',   # Again, pick a license
    'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to suppots
    'Programming Language :: Python :: 2.7',	
  ],
)
op=os.popen("sudo -H pip install -r requirements.txt").read()
print op
