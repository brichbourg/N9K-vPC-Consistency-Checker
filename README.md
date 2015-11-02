# N9K vPC Consistency Checker

##Author:

Brantley Richbourg (brichbourg@gmail.com)

##Installation

Here are the required modules:


Download and install LXML
	
	sudo pip install lxml
	sudo pip install pyyaml

Clone this repo

	git clone https://github.com/brichbourg/N9K-vPC-Consistency-Checker.git


##Usage

This script is run with the following syntax:

	python vpcconcheck.py hostsip.txt username password 

##Information

N9K vPC Consistency Checker is a Python script that is written to use the XML API of the Cisco Nexus 9000 Data Center Switch.  This script will log into each switch that an IP address has been provided for in the hostsip.txt file (or another text file that is passed to the script with command line arguments).  Once it is logged in, it will download vPC consistency information and look for any mismatches within the global vPC settings, and the indivdual vPC settings for each vPC that is defined on the switch.  If an mismatch is found, it will tell you which switch and what the mismatch is.

This script requires all switches to have the same username and password (passed via command line arguments).

###Sample Output - No Mismatchs Detected

	Brantleys-MacBook-Pro:$ python vpcconcheck.py hostips.txt admin cisco
	==================== n9k1 ====================
	The vPC domain ID is 10
	Total vPCs: 2
	Role: primary

	===No global consistency issues===

	===No vPC consistency issues===

	==================== n9k1 ==================== 

	==================== n9k2 ====================
	The vPC domain ID is 10
	Total vPCs: 2
	Role: secondary

	===No global consistency issues===

	===No vPC consistency issues===

	==================== n9k2 ==================== 

	Brantleys-MacBook-Pro:$ 

### Sample Output - Mismatch Detected

	Brantleys-MacBook-Pro:$ python vpcconcheck.py hostips.txt admin cisco
	==================== n9k1 ====================
	The vPC domain ID is 10
	Total vPCs: 2
	Role: primary
	
	===No global consistency issues===

	******************************
	*MISMATCH DETECTED in vPC 18
	******************************
	Value Name: Allowed VLANs
	Local Value:  100
	Peer Value: 1
	****************************** 

	==================== n9k1 ==================== 

	==================== n9k2 ====================
	The vPC domain ID is 10
	Total vPCs: 2
	Role: secondary
	No global consistency issues

	******************************
	*MISMATCH DETECTED in vPC 18
	******************************
	Value Name: Allowed VLANs
	Local Value:  1
	Peer Value: 100
	****************************** 

	==================== n9k2 ==================== 

	Brantleys-MacBook-Pro:$ 
