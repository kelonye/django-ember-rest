component = ./node_modules/component-hooks/node_modules/.bin/component

test:
	@make --no-print-directory -C test

example:
	@make boot --no-print-directory -C test

publish:
	@python setup.py sdist upload

deps:
	@pip install -r requirements.txt

clean:
	@rm -rf build dist django_ember_rest.egg-info $(shell find -name ='*.pyc')
	@make clean --no-print-directory -C test

.PHONY: clean publish example test