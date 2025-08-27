.PHONY: help lint test proto-gen

help:
	@echo "Commands:"
	@echo "  lint      : Run ruff linter and formatter."
	@echo "  test      : Run pytest."
	@echo "  proto-gen : Regenerate protobuf files."

lint:
	ruff check .
	ruff format .

test:
	pytest

proto-gen:
	@./scripts/gen_proto.sh
