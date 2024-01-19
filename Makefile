RUN := poetry run

install:
	poetry install

lint:
	$(RUN) flake8 ./menu_app/

local_deploy:
	$(RUN) uvicorn menu_app.main:app --reload
