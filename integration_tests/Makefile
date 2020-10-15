test-setup: build-applicationd

build-applicationd: egg-info
	docker build -t wazoplatform/wazo-applicationd ..

clean:
	docker rmi -f wazoplatform/wazo-applicationd

egg-info:
	cd .. && python setup.py egg_info

test:
	pytest -x

.PHONY: test-setup build-applicationd egg-info test clean
