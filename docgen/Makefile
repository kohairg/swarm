.PHONY: install start stop clean setup run logs check-ports

install:
	pip install --upgrade pip wheel setuptools
	pip install -r requirements.txt

check-ports:
	@echo "Checking if required ports are available..."
	@lsof -i :8080 || true
	@lsof -i :50051 || true

stop:
	-docker compose down
	-docker rm -f docgen-weaviate-1 2>/dev/null || true

clean: stop
	pip uninstall -y langchain langchain-community langchain-core
	pip cache purge
	-docker volume prune -f

start: check-ports stop
	docker compose up -d
	@echo "Waiting for Weaviate to start..."
	@sleep 5

setup: start
	PYTHONPATH=$(PWD):$(PWD)/.. python setup_weaviate.py

run: setup
	PYTHONPATH=$(PWD):$(PWD)/.. python run.py

logs:
	docker compose logs -f weaviate