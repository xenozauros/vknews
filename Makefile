install: /usr/bin/python2

/usr/bin/python2:
	virtualenv .
	/usr/bin/pip install -r requirements.txt

serve: /usr/bin/python2
	/usr/bin/python2 ./manage.py runfcgi method=prefork host=127.0.0.1 port=8881 pidfile=/tmp/server.pid

deploy: /usr/bin/python2
	./server.sh restart

clean:
	rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/
