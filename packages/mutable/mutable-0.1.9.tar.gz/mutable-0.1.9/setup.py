# Thanks to http://peterdowns.com/posts/first-time-with-pypi.html - it's been a while
from distutils.core import setup
setup(
  name = 'mutable',
  packages = ['mutable'],
  version = '0.1.9',
  license = 'MIT',
  description = 'Object class and decorator for dynamic class props from dict, JSON or command-line input',
  author = 'Andreas Urbanski',
  author_email = 'urbanski.andreas@gmail.com',
  url = 'https://github.com/nardeas/mutable',
  download_url = 'https://github.com/nardeas/mutable/archive/0.1.9.tar.gz',
  keywords = ['mutable', 'json', 'class', 'dynamic', 'props', 'fields']
)
