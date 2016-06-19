import json

class InfrastructureConfiguration:

	def __init__ (self):
		self.n_nodes = 3
		self.packages = ["openmpi", "openmpi-devel", "gcc", "gcc-c++", "ant", "java-1.8.0-openjdk-devel"]
		self.scripts = [{"name" : "custom.py", "interpreter" : "python" }, {"name" : "custom.sh", "interpreter" :"bash"}]

	def set_n_nodes (self, n_nodes):
		self.n_nodes = n_nodes

	def add_package (self, package_name):
		self.packages.append(package_name)

	def add_custom_script (self, script_name, interpreter):
		self.scripts.append({"name" : script_name, "interpreter" : interpreter})

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
				node_name = "node0" + str(n)
			else:
				node_name = "node" + str(n)
			ip_addr = "192.168.0." + str(n + 3)
			host_file["/etc/hosts"]["content"]["Fn::Join"][1].append(ip_addr+"    "+node_name+"    "+node_name+"\n")
		#print(json.dumps(host_file))
		return host_file

	def create_package_list (self):
		package_list = { "packages" : {"yum" : {}} }
		for package in self.packages:
			package_list['packages']['yum'][package] = []
		#print(json.dumps(package_list))
		return package_list

	def parse_custom_scripts (self):
		custom_init = {"files" : {}, "commands" : {}}
		for custom_script in self.scripts:
			script_name = custom_script['name']
			try:
				script = open("CustomScripts/" + script_name).read()
				path = "/home/ec2-user/.initScripts/" + script_name
				parsed_script = { path : {"content" :  {"Fn::Join" : ["\n",[]]}}}
				for line in script.split('\n'):
					line = line.replace("\n", "\\n")
					parsed_script[path]['content']['Fn::Join'][1].append(line)
				custom_init['files'].update(parsed_script)
				custom_init['commands']["run_"+script_name] = {}
				custom_init['commands']["run_"+script_name]["command"] = custom_script['interpreter'] + " " + path
				custom_init['commands']["run_"+script_name]['ignoreErrors'] = "true"
			except:
				print("\n\nError reading custom scripts")
				raise
		#print(custom_init)
		return custom_init

	def create_nodes(self, host_file, package_list, custom_init):

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
				node['Metadata']['AWS::CloudFormation::Init']['custom'].update(custom_init)
				node_list.append(node)
			except:
				print("\n\nError creating nodes")
				raise
		return node_list


	def generate_infra (self, output_name):
		ip_map = self.create_ip_map()
		host_file = self.create_hosts_file()
		package_list = self.create_package_list()
		custom_init = self.parse_custom_scripts()
		node_list = self.create_nodes(host_file, package_list, custom_init)
		try:
			base_infra = json.loads(open("Templates/base_infra.json").read())
		except:
			print("\n\nError loading files")
			raise

		base_infra['Mappings'].update(ip_map)
		base_infra['Resources']['NATInstance']['Metadata']['AWS::CloudFormation::Init']['setupNAT']['files'].update(host_file)
		for n in range(1,self.n_nodes+1):
			if (n < 10):
				node_resource_name = "StackNode0" + str(n)
			else:
				node_resource_name = "StackNode" + str(n)

			base_infra['Resources'][node_resource_name] = node_list[n-1]
		
		infra_file = open(output_name, "w")
		infra_file.write(json.dumps(base_infra))
		infra_file.close()