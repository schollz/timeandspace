prereqs: desktop/.venv raspberrypi/.venv orchestator/orchestator

desktop/.venv:
	cd desktop && uv venv .venv && \
	. .venv/bin/activate && uv pip install -r requirements.txt

raspberrypi/.venv:
	cd raspberrypi && uv venv .venv && \
	. .venv/bin/activate && uv pip install -r requirements.txt
	

desk: stop desktop/.venv
	cd orchestrator/ && go build -v 
	cp ecosystem.desktop.js ecosystem.config.js
	pm2 start ecosystem.config.js
	pm2 log

pi:
	cp ecosystem.raspberrypi.js ecosystem.config.js
	pm2 start ecosystem.config.js

stop:
	-pm2 stop all && pm2 delete all

clean:
	rm -rf *log