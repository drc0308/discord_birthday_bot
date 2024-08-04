docker:
	docker build -t birthday-discord .

run:
	docker run -v  $(shell pwd)/birthdays.db:/app/birthdays.db birthday-discord

clean:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$|\.pytest_cache)" | xargs rm -rf

test:
	docker build -f Test.Dockerfile -t birthday-test .
	docker run birthday-test 

.PHONY: run clean test