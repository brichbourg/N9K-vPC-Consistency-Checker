'''
Cisco Nexus 9000 - vPC Consistency Checker Script
Author: Brantley Richbourg
email: brichbourg@gmail.com

Version: 1.01
'''



from device import Device
import xmltodict
import json
import sys
import os.path

def get_hostname(show_hw_dict):
	hostname = show_hw_dict['ins_api']['outputs']['output']['body']['host_name']
	return hostname

def list_vpc_nums(vpcdata):
	
	#This takes the dictionary of vpc information and returns justs the vpc ids as an integer	
	list_vpc_ids = []

	for each in vpcdata:
		vpc_id_int = int(each['vpc-id'])
		list_vpc_ids.append(vpc_id_int)
		
	return list_vpc_ids

#This functions displays generic vPC information and then calls vpc_con_check function to look for problems.
def vpc_check(vpcinput,vpcconinput):
	
	vpcdata = vpcinput['ins_api']['outputs']['output']['body']
	
	#This is used as a check to see if mismatches are found.  
	vpc_error_exist = False

	domainid = vpcdata['vpc-domain-id']
	numofvpcs = vpcdata['num-of-vpcs']
	vpcrole = vpcdata['vpc-role']
	print 'The vPC domain ID is %s' % domainid
	print 'Total vPCs: %s' % numofvpcs
	print 'Role: %s' % vpcrole

	#Calls the vPC Consistency Checker function (vpc_con_check) to check the global vPC settings
	vpc_con_check(None,vpcconinput)

	vpclist = vpcinput['ins_api']['outputs']['output']['body']['TABLE_vpc']['ROW_vpc']
	return vpclist

#This function is the meat of the script.  This is where the values are compared to find mismatches with vPC settings.
def vpc_con_check (vpcid,vpcconinput):

	#This is used later as a check to see if mismatches are found.  Used for controlling print output later  
	vpc_error_exist = False

	#This piece check to see if the data is from the global setting or not.  It is used to control print output later.
	vpcglobal_checker = vpcconinput['ins_api']['outputs']['output']['input']
	if vpcglobal_checker == 'show vpc consistency-parameters global':
		is_vpc_data_global = True
	else:
		is_vpc_data_global = False

	#This prints a line for non-global vPC data to show what vPC number is being checked.
	if is_vpc_data_global == False:
		print '*' * 15
		print '* vPC', vpcid
		print '*' * 15
	
	#This puts the data we need to check in a dictonary 	
	vpcdata = vpcconinput['ins_api']['outputs']['output']['body']['TABLE_vpc_consistency']['ROW_vpc_consistency']
	
	#For loop to run over each dictionary of vPCs that are configured and to look for mismatches 
	for each in vpcdata:

		param_name = each ['vpc-param-name']
		localvalue = each ['vpc-param-local-val']
		peervalue = each ['vpc-param-peer-val']
	
		if localvalue != peervalue:
			print param_name, 'is not consistent'
			print 'Local Value: ', localvalue
			print 'Peer Value:', peervalue, '\n'


			#This will set a variable so the "All good" print statement doesn't print
			vpc_error_exist = True

	
	#This checks to see if certain conditions are present so the correct message is printed when no issues are detected.
	if vpc_error_exist == False: 
		if is_vpc_data_global == True:
			print '\n<No global consistency issues>\n'
	if vpc_error_exist == False:
		if is_vpc_data_global == False:
			print '<<<No consistency errors with vPC', vpcid, '>>>'

def main():
	args = sys.argv
	
	if len(args) == 4:

		#This section will check to see if the file pass to Python in a argument actually exists
		if os.path.exists(args[1]):
			switch_ips = open(args[1]).read().splitlines()
			#print switch_ips
		else:
			print 'File ', os.path.realpath(args[1]), 'does not exist.  Please try again'
			sys.exit(1)
	
		#For look to open each switch in the list of IP addresses passed via CLI arguments
		for switch_ip in switch_ips:

			switch = Device(ip=switch_ip,username=args[2],password=args[3])
			switch.open()

			#These lines gat the XML output from the XML API on the N9K
			getswitchhardwaredata = switch.show('show hardware')
			getswitchvpcdata = switch.show('show vpc')
			getvpccondata = switch.show('show vpc consistency-parameters global')
		
			#These lines parse the XML into JSON format
			getswitchvpcdatajson = xmltodict.parse(getswitchvpcdata[1])
			getswitchhardwaredatajson = xmltodict.parse(getswitchhardwaredata[1])
			getvpccondatajson = xmltodict.parse(getvpccondata[1])

			
			#This grabs the name on the switch
			switchname = get_hostname(getswitchhardwaredatajson)
			
			#<<<This is the start of outputting information regarding a switch>>>
			print '=' * 20, switchname, '=' * 20
			
			#This sends the show vpc command and show vpc con global command JSON data to the function to check for problems.
			#This will also return a list of the indivdual vPCs that are configured on the switch.
			vpcinfo = vpc_check(getswitchvpcdatajson,getvpccondatajson)

			#Calls a function to return the vPC IDs from the switch.
			vpc_list = list_vpc_nums(vpcinfo)
			# print vpc_list, 'DEBUG: VPC NUMBERS LIST'

			#Now we take the list of vPC IDs and call the NXAPI with the command show vpc con vpc X
			for each in vpc_list:
				stringeach = str(each)
				string_cmd = 'show vpc consistency-parameters vpc '
				string_cmd += stringeach
				
				#This line takes the string_cmd variable and uses that to run the commmand with the customer VPC ID
				getvpccondetail = switch.show(string_cmd)

				#Parse the XML to JSON
				getvpccondetailjson = xmltodict.parse(getvpccondetail[1])
				# print getvpccondetailjson, 'VPC CON DETAIL JSON'

				#This calls a function to check each indivdual vPC for inconsistencies
				vpc_con_check(each,getvpccondetailjson)
			
			#<<<This is the end of outputting information regarding a switch>>>
			print '=' * 20, switchname, '=' * 20 , '\n'
			

		
	else:
		print 'ERROR: Invalid syntax\n'\
		'Example: \"python vPCconcheck.py file.txt username password\"'
		sys.exit(1)

if __name__ == "__main__":
	main()

