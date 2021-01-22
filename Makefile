path = src spec
files = `find $(path) -name '*.py'` setup.py

test:
	mamba $(path) --format=documentation --enable-coverage

format:
	- add-trailing-comma $(files)
	- pyformat -i $(files)
	- isort -rc $(path)

lint:
	flake8 $(path)

commit_check:
	cz check --rev-range origin/master..HEAD

bump:
	cz bump --changelog --check-consistency --yes
