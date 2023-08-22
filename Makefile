MAKEFLAGS += --silent

report:
	python manage.py generate_report $(filter-out $@,$(MAKECMDGOALS))

test:
	python manage.py test -s -v $(filter-out $@,$(MAKECMDGOALS))

bundle:
	git bundle create foris.gitbundle --all