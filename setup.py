
import sys, argparse, subprocess

def node_config ():
	print("node_config")
	pass

def net_config ():
	print("net_config")
	pass

def save_config ():
	print("save_config")
	pass

def overall_conf ():
	print("\nConfiguration Options:\n")
	print("\t1 - Node configuration")
	print("\t2 - Network configuration")
	print("\t3 - Save configuration")
	print("")
	read_input = input("Type option number: ")
	read_input = int(read_input)
	try:
		conf_dict[read_input]()
	except:
		overall_conf()

conf_dict = {
	1: node_config,
	2: net_config,
	3: save_config }

def setup (argv):
	parser = argparse.ArgumentParser(description = "Manage AWS CloudFormation Template")
	parser.add_argument('action', choices = (
		'std',
		'conf'))
	args = parser.parse_args(argv[1:])
	if args.action == 'std':
		# Load all std
		print ("std")
	elif args.action == 'conf':
		# Load std and display options
		overall_conf()
	else:
		assert False


if __name__ == '__main__':
    setup(sys.argv)