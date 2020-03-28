app.py: SophieOpferman.db

SophieOpferman.db: buildDB.py
	python3 buildDB.py

clean:
	rm SophieOpferman.db

run:
	python3 app.py
