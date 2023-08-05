from setuptools import setup

setup(name='optics',
      version='0.0.1',
      description='Transfer matrix simulation of 1D optical multilayers',
      url='http://github.com/remy1618/opt_sim',
      author='Remy Ko',
      author_email='remy.ko@mail.utoronto.ca',
      license='MIT',
      packages=['optics'],
      include_package_data=True,
      python_requires='>=2.7, !=3.*, <4',
      install_requires=[
          'numpy>=1.7',
          'matplotlib>=1.1'
      ],
      zip_safe=False)