from setuptools import setup, find_packages

setup(
	name='text-cleaner',
	version='0.1.0',
	description='A text cleaning tool for speech and text processing',
	author='Grammatek ehf',
	author_email='info@grammatek.com',
	url='https://github.com/grammatek/text-cleaner',
	packages=find_packages(),
	install_requires=[
		'setuptools',
		'bs4'
	],
	python_requires='>=3.5',
	entry_points={
			'console_scripts': [
				'text_cleaner=text_cleaner.clean:main'
							]
				}
	)
