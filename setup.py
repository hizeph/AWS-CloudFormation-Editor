
import sys
from driver import InfrastructureConfiguration

class Setup:

	def __init__(self):
		self.conf = InfrastructureConfiguration()
		self.conf_map = {
			1: self.conf_nodes,
			2: self.conf_packages,
			4: self.show_conf,
			5: self.save_conf,
			6: sys.exit
		}

	def conf_nodes (self):
		try:
			read_input = input("\nTotal desired number of nodes: ")
			self.conf.set_n_nodes(int(read_input))
		except KeyboardInterrupt:
			self.overall_conf()

	def conf_packages (self):
		try:
			read_input = input("\nPackage name to add: ")
			self.conf.add_package(str(read_input))
		except KeyboardInterrupt:
			self.overall_conf()

	def show_conf (self):
		print("\nNumber of nodes: " + str(self.conf.n_nodes))
		print("Packages to install:");
		for package in self.conf.packages:
			print("\t" + str(package))

	def save_conf (self):
		try:
			read_input = input("\nName of the output file: ")
			self.conf.generate_infra(str(read_input))
			print("File saved")
		except KeyboardInterrupt:
			self.overall_conf()

	def overall_conf (self):
		while(True):
			try:
				print("\nConfiguration Options:\n")
				print("\t1 - Number of nodes")
				print("\t2 - Packages to install")
				print("\t3 - Custom files")
				print("\t4 - Show configuration")
				print("\t5 - Save configuration")
				print("\t6 - Quit")
				print("")
				read_input = input("Type option number: ")
				self.conf_map[int(read_input)]()
			except KeyboardInterrupt:
				print("")
				break


if __name__ == '__main__':
	setup = Setup()
	setup.overall_conf()