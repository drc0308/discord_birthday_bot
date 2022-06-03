docker:
	docker build -t birthday-discord .

run:
	docker run -v  $(shell pwd)/birthdays.db:/app/birthdays.db birthday-discord

.PHONY: run 