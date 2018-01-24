from setuptools import setup

setup(name='iotscanner',
      version='0.1',
      description='Pentesting tool to scan iot devices.',
      url='http://github.com/JurreitJ/IoTScanning',
      author='Jennifer Jurreit',
      author_email='j.jurreit@gmx.de',
      license='GNU',
      packages=['iotscanner'],
      install_requires=['urllib3', 'beautifulsoup4', 'netaddr', 'python-nmap', 'paramiko'],
      zip_safe=False)
