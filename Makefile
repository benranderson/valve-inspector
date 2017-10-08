help:
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with pylnt"
	@echo "  test        run all your tests using py.test"

deps:
	pip install -r requirements.txt

clean:
	python manage.py clean

lint:
	pylint app/

test:
	py.test tests

deploy:
	git add .
	git commit -m "$(m)"
	git push origin master
	heroku maintenance:on
	git push heroku master
	heroku run python manage.py deploy
	heroku restart
	heroku maintenance:off
