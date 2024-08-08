install:
	@python3 -m venv .venv
	@. .venv/bin/activate
	@pip install -r .github/requirements.txt


run_standalone: install
	@pip install -r .github/devrequirements.txt
	@python3 scrape.py 
	@php -S 10.0.0.2:8000 -t .
