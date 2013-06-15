test:
	@make --no-print-directory -C test

example:
	@make boot --no-print-directory -C test

publish:
	@python setup.py sdist upload

clean:
	@rm -rf build dist django_ember_rest.egg-info $(shell find -name ='*.pyc')
	@make clean --no-print-directory -C test

.PHONY: clean publish example test