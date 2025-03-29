install:
	poetry python install 3.12 || { echo "Python has been already installed"; } && \
	poetry env use python3.12 && \
	poetry install

activate: install
	poetry self add poetry-plugin-shell && \
	poetry shell;

typing: activate
	poetry run mypy .

run: install typing
	pwd && \
	poetry run python project/main.py --config /project/config/config.json
