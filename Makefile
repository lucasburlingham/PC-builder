install:
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt


run_standalone:
	. .venv/bin/activate
	python3 scrape.py 
