import sys, argparse

def overall_conf ():
	print("\nConfiguration Options:\n")
	print("\t1 - Node configuration")
	print("\t2 - Network configuration")
	print("")


def init (argv):
	parser = argparse.ArgumentParser(description = "Manage AWS CloudFormation Template")
	parser.add_argument('action', choices = (
		'std',
		'conf'))
	args = parser.parse_args(argv[1:])
	if args.action == 'std':
		# Load all std
		print ("std")
		pass
	elif args.action == 'conf':
		# Load std and display options
		overall_conf()
		pass
	else:
		assert False


if __name__ == '__main__':
    init(sys.argv)