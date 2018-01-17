from setuptools import setup

setup(name='iotscanning',
      version='0.1',
      description='Pentesting tool to scan iot devices.',
      url='http://github.com/JurreitJ/IoTScanning',
      author='Jennifer Jurreit',
      author_email='j.jurreit@gmx.de',
      license='BSD',
      packages=['iotscanning'],
      install_requires=['urllib3', 'beautifulsoup4', 'netaddr', 'python-nmap', 'paramiko'],
      dependency_links=["https://github.com/riverloopsec/killerbee/"],
      zip_safe=False)