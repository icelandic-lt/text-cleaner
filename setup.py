from setuptools import setup, find_packages

setup(
	name="text-cleaner", 
	packages=find_packages(),
	install_requires=['setuptools'],
	python_requires='>=3.5',
	entry_points={
			'console_scripts': [
				'text_cleaner=text_cleaner.clean:main'
							   ]
				 }
	)
	