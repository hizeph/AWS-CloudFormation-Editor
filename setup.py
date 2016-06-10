
import sys, argparse, json
from configurator import InfrastructureConfiguration

def overall_conf ():
	print("\nConfiguration Options:\n")
	print("\t1 - Number of nodes")
	print("\t2 - Packages to install")
	print("\t3 - Custom files")
	print("\t4 - Save configuration")
	print("")
	read_input = input("Type option number: ")
	read_input = int(read_input)


def setup (argv):
	conf = InfrastructureConfiguration()
	conf.create_hosts_file()
	'''
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
	'''


if __name__ == '__main__':
	setup(sys.argv)