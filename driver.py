class InfrastructureConfiguration:

	def __init__ (self):
		self.n_nodes = 3
		self.packages = []
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
		pass

	def create_extra_files (self):
		pass

	def create_nodes(self, ip_map, host_file, package_list, extra_files):
		#node['Properties']['NetworkInterfaces'][0]['PrivateIpAddress']['Fn::FindInMap'][1] = "Node01"
		#UserData = "StackNode01"
		#Tags = "Node01"
		pass


	def generate_infra (self):
		ip_map = self.create_ip_map()
		host_file = self.create_hosts_file()
		#self.create_package_list()
		#self.create_extra_files()
		#self.create_nodes(ip_map, host_file, package_list, extra_files)
		try:
			base_infra = json.loads(open("Templates/base_infra.json").read())
			node = json.loads(open("Templates/node.json").read())
		except:
			print ("Error loading files")
		for n in range(1,self.n_nodes+1):
			if (n < 10):
				node_resource_name = "StackNode0" + str(n)
			else:
				node_resource_name = "StackNode" + str(n)

			#base_infra['Properties'][node_resource_name]