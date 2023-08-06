FILES= Makefile README.txt LICENSE.txt iptables_converter.py iptables_converter_tests.py


pkg:
	find . -type f | grep pyc$ | sudo xargs rm -f
	find . -type d | grep __pycache__ | sudo xargs rm -rf
	sudo rm -rf build dist iptables_converter.egg-info
	sudo rm -rf /usr/local/bin/ip6tables_converter
	sudo rm -rf /usr/local/bin/iptables_converter
	sudo rm -f /usr/local/lib/python2.7/dist-packages/iptables_converter-0.9.10-py2.7.egg
	sudo rm -f /usr/local/lib/python3.5/dist-packages/iptables_converter-0.9.10-py3.5.egg
	python setup.py build
	python setup.py sdist bdist_wheel install

prep:
	rm -rf build dist iptables_converter.egg-info
	python setup.py clean
	python setup.py sdist
	# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	# twine upload --repository-url https://pypi.python.org/pypi dist/*

v:
	git grep -i version | egrep -vi '(LICENSE|ipv)'

t:
	flake8 iptables_converter tests
	py.test --cov=iptables_conv --cov=tests --cov-report=term-missing

th:
	py.test --cov=iptables_conv --cov=tests --cov-report=html -v

f:
	py.test --flake8 iptables_conv/iptables_converter.py tests/test_iptables_converter.py

#----------------------------------------------------------------

doc:
	$(MAKE) -C docs html

clean:
	@python setup.py clean --bdist-base build
	@find . -type f | grep pyc$ | sudo xargs rm -f
	@find . -type d | grep __pycache__ | sudo xargs rm -rf
	@rm -rf *~ *.pyc .pybuild/ .coverage htmlcov build docs/build/* .tox
	@rm -rf iptables_converter.egg-info
	@rm -rf dist __pycache__ *.py3
	$(MAKE) -C docs clean
	@[ ! -d debian ] || dh_clean

