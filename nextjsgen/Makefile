.PHONY: install start stop clean setup run logs check-ports

install:
	pip install --upgrade pip wheel setuptools
	pip install --no-cache-dir -r requirements.txt

check-ports:
	@echo "Checking if required ports are available..."
	@lsof -i :5432 || true
	@lsof -i :3000 || true

stop:
	-docker compose down
	-docker rm -f nextjsgen-postgres-1 nextjsgen-nextjs-dev-1 2>/dev/null || true

clean: stop
	pip cache purge
	-docker volume prune -f
	rm -rf generated/*

start: check-ports stop
	docker compose up -d
	@echo "Waiting for PostgreSQL to start..."
	@sleep 5

setup: start
	PYTHONPATH=$(PWD)/.. python database.py

run: setup
	PYTHONPATH=$(PWD)/.. python run.py

logs:
	docker compose logs -f 