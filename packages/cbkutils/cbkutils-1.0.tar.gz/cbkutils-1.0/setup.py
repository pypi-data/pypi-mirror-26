from setuptools import setup

setup(name='cbkutils',
      version='1.0',
      description='Simple helpers',
      url='http://github.com/cidrblock/cbkutils',
      author='Bradley A. Thornton',
      author_email='brad@thethorntons.net',
      license='MIT',
      packages=[
        'cbkutils',
        'cbkutils.backports',
        'cbkutils.backports.shutil_get_terminal_size'
      ],
      install_requires=[
        'Jinja2',
        'jsonpickle',
        'MarkupSafe',
        'Pygments',
        'PyYAML'
      ],
      zip_safe=False)
