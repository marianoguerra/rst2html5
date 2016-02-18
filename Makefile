
clean:
	sudo rm -rf rst2html5_tools.egg-info build smoketestoutput

install:
	sudo python setup.py install

smoketest:
	./smoketest.sh
	rm -rf smoketestoutput

release:
	python setup.py sdist upload
