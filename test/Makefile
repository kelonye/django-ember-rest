test:
	@./manage.py test --failfast

boot: server.sqlite3
	@python manage.py runserver

server.sqlite3:
	@./manage.py syncdb --noinput
	@./manage.py loaddata server/fixtures/*

clean:
	@rm -rf server.sqlite3

.PHONY: clean