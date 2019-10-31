# edc : Energy Dashboard Command Line Interface
# Copyright (C) 2019  Todd Greenwood-Geer (Enviro Software Solutions, LLC)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

.PHONY: all
all: help

.PHONY: help
help:
	# -----------------------------------------------------------------------------
	#  
	#  Targets:
	#
	#	help		: show this message
	#	clean		: remove build artifacts
	#	setup		: create the conda environment
	#	build		: build from source
	#	pub		: publish build artifacts to prod pypi (conda activate eap-dev first)
	#
	# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# TARGETS
# -----------------------------------------------------------------------------

.PHONY: clean
clean:
	rm -rf venv
	rm -rf build
	rm -rf dist
	rm -rf energy_dashboard_library.egg-info
	rm -rf energy_dashboard_client.egg-info
	-rm *.log

.PHONY: setup
setup:
	-conda env create --file builder.yml
	echo "activate environment with..."
	echo "$ conda activate builder"

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

.PHONY: pub
pub: clean build
	twine upload --repository pypi dist/*
