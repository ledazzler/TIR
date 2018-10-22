import json
import csv
import glob
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj

if __name__ == "__main__":
    # the result dictionary
    result = {
        "features": [],
        "interfaces": {}
    }
 
    # create CiscoConfParse object using a configuration file stored in the
    # same directory as the script
    confparse = CiscoConfParse("example_config.txt")
	
	# extract the interface name and description
    # first, we get all interface commands from the configuration
    interface_cmds = confparse.find_objects(r"^interface ")
	
	# iterate over the resulting IOSCfgLine objects
    for interface_cmd in interface_cmds:
	
		# get the interface name (remove the interface command from the configuration line)
        intf_name = interface_cmd.text[len("interface "):]
        result["interfaces"][intf_name] = {}
        
		# extract IP addresses if defined
        IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"
        for cmd in interface_cmd.re_search_children(IPv4_REGEX):
            # ciscoconfparse provides a helper function for this task
            ipv4_addr = interface_cmd.re_match_iter_typed(IPv4_REGEX, result_type=IPv4Obj)
 
            result["interfaces"][intf_name].update({
                "ipv4": {
                    "address": ipv4_addr.ip.exploded,
                    "netmask": ipv4_addr.netmask.exploded
                }
            })