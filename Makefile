.PHONY: install test gui cli clean build

install:
	pip install -e .

test:
	PYTHONPATH=src python -m pytest -q

gui:
	ai-video-gui

cli:
	ai-video

build:
	python -m build

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	rm -rf build dist *.egg-info src/*.egg-info