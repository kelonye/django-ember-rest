publish:
	@python setup.py sdist upload

clean:
	@rm -rf build dist django_ember_rest.egg-info $(shell find -name ='*.pyc')

.PHONY: publish clean