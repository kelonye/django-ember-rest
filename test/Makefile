test:
	@./manage.py test --failfast

boot: blog.sqlite3
	@python manage.py runserver

blog.sqlite3:
	@./manage.py syncdb --noinput
	@./manage.py loaddata blog/fixtures/*

clean:
	@rm -rf blog.sqlite3

.PHONY: clean