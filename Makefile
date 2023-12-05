install-dependencies:
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

install-cli:
	pip install -e .

test:
	pytest

test-coverage:
	coverage run --source=. -m pytest
	coverage report
	coverage html
	cd htmlcov && open index.html

remove-cli:
	pip uninstall pypony
