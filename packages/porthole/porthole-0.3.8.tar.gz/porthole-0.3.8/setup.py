from setuptools import setup

setup(name='porthole',
      version='0.3.8',
      description='An automated reporting package.',
      author='Billy McMonagle',
      author_email='speedyturkey@gmail.com',
      url='https://github.com/speedyturkey/porthole',
      packages=['porthole'],
      install_requires=[
                        'pymysql',
                        'xlsxwriter',
                        'SQLAlchemy'
                    ],
      zip_safe=False)
