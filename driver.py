import json

class InfrastructureConfiguration:

	def __init__ (self):
		self.n_nodes = 3
		self.packages = ["openmpi", "openmpi-devel", "gcc", "gcc-c++", "ant", "java-1.8.0-openjdk-devel"]
		self.files = []

	def set_n_nodes (self, n_nodes):
		self.n_nodes = n_nodes

	def add_package (self, package_name):
		self.packages.append(package_name)

	def add_extra_files (self, file_name):
		self.files.apped(file_name)

	def create_ip_map (self):
		ip_map =  {"IpAddressConfig" : {}}
		for n in range(1,self.n_nodes+1):
			if (n < 10):
				node_resource_name = "Node0" + str(n)
			else:
				node_resource_name = "Node" + str(n)
			ip_map["IpAddressConfig"][node_resource_name] = { "IP" : "192.168.0." + str(n + 3) }
		#print(json.dumps(ip_map))
		return ip_map

	def create_hosts_file (self):
		host_file = {"/etc/hosts" : { "content" : { "Fn::Join" : ["", ["127.0.0.1    localhost    localhost\n"]]}}}
		for n in range(1,self.n_nodes+1):
			if (n < 10):
				node_resource_name = "node0" + str(n)
			else:
				node_resource_name = "node" + str(n)
			ip_addr = "192.168.0." + str(n + 3)
			host_file["/etc/hosts"]["content"]["Fn::Join"][1].append(ip_addr+"    "+node_resource_name+"    "+node_resource_name+"\n")
		#print(json.dumps(host_file))
		return host_file

	def create_package_list (self):
		package_list = { "packages" : {"yum" : {}} }
		for package in self.packages:
			package_list['packages']['yum'][package] = []
		#print(json.dumps(package_list))
		return package_list


	def create_extra_files (self):
		pass

	def create_nodes(self, host_file, package_list, extra_files):

		node_list = []
		for n in range(1,self.n_nodes+1):
			if (n < 10):
				node_resource_name = "StackNode0" + str(n)
				node_name = "Node0" + str(n)
			else:
				node_resource_name = "StackNode" + str(n)
				node_name = "Node" + str(n)
			try:
				node = json.loads(open("Templates/node.json").read())
				node['Properties']['NetworkInterfaces'][0]['PrivateIpAddress']['Fn::FindInMap'][1] = node_name
				node['Properties']['UserData']['Fn::Base64']['Fn::Join'][1][5] = "         --resource " + node_resource_name
				node['Properties']['Tags'].append({"Key" : "Name", "Value" : node_name})
				node['Metadata']['AWS::CloudFormation::Init']['setup'].update(package_list)
				node['Metadata']['AWS::CloudFormation::Init']['setup']['files'].update(host_file)
				node_list.append(node)
			except:
				print ("Error creating node")
		return node_list


	def generate_infra (self, output_name):
		ip_map = self.create_ip_map()
		host_file = self.create_hosts_file()
		package_list = self.create_package_list()
		extra_files = {} #self.create_extra_files()
		node_list = self.create_nodes(host_file, package_list, extra_files)
		try:
			base_infra = json.loads(open("Templates/base_infra.json").read())
		except:
			print ("Error loading files")

		base_infra['Mappings'].update(ip_map)
		for n in range(1,self.n_nodes+1):
			if (n < 10):
				node_resource_name = "StackNode0" + str(n)
			else:
				node_resource_name = "StackNode" + str(n)

			base_infra['Resources'][node_resource_name] = node_list[n-1]
		
		infra_file = open(output_name, "w")
		infra_file.write(json.dumps(base_infra))
		infra_file.close()