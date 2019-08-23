from distutils.core import setup
setup(
  name='marketify',
  packages=['marketify'],
  version='0.1',
  license='MIT',
  description='A micro-library that pulls data from exchanges',
  author='Marcelino Franco',
  author_email='mcfranco16@gmail.com',
  url='https://github.com/mfranco1/marketify',
  download_url='https://github.com/mfranco1/marketify/archive/v_01.tar.gz',
  keywords=['Trading', 'Market', 'Exchange', 'Websocket', 'Async'],
  install_requires=[
      'aiodns',
      'aiohttp',
      'Rx',
      'websockets',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)