# Nexus 9000 - FindMac.py

##Authors:

Koorapati, Sahaja Sahaja.Koorapati@nexusis.com

Richbourg, Brantley Brantley.Richbourg@NexusIS.com

Sanchez, Milo milo.sanchez@nexusis.com

##Installation

Here are the required modules:

Downlaod PyYAML from http://pyyaml.org/wiki/PyYAML

	sudo python setup.py install

Download and install LXML
	
	pip install lxml

Clone this repo

	git clone https://github.com/brichbourg/FindMac.git


##Usage
This script is designed to take a mac address, entered in the format xxxx.xxxx.xxxx and find its location on a set of N9Ks.  The list of N9Ks is in a file:

File Format - List the mgmt 0 address of each switch on a separate line.

1.2.3.4<br/>
5.6.7.8<br/>
9.10.11.12<br/>

To run the script, please enter the following:

	python findMac.py xxxx.xxxx.xxxx file.txt username password

NOTE: The mac address must be in the following format: xxxx.xxxx.xxxx

This script was built under the assumption that all of your N9Ks will take the same username and password.  Different username and passwords is currently not supported.