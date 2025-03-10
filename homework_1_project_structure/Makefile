install:
	poetry python install 3.11 || { echo "Python has been already installed"; } && \
	poetry env use python3.11 && \
	poetry install

activate: install
	poetry self add poetry-plugin-shell && \
	poetry shell;

test: activate
	poetry run pytest

run: install activate
	pwd && \
	poetry run python project/main.py --config /project/config/config.json
