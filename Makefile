
.PHONY: install
install:
	sudo apt install -y python3-cartopy libgeos-dev libproj-dev
	poetry install
	poetry run pip install --force-reinstall shapely --no-binary shapely

.PHONY: jupyter
jupyter:
	poetry run jupyter lab
