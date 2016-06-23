# AWS-CloudFormation-Editor

Requirements

  Python 2+ with argparse and json packages.
  
  
Execution

  setup.py
  
    -h, --help
      Shows this help
    -o, --output OUTPUT
      Reads the configuration file, generates the infrastructure and saves it as OUTPUT
    -f, --file FILE
      Sets the configuration file and runs the wizard
    -n, --nodes NODES
      Sets the number o nodes in the infrastructure, to a maximum of 124. This option overrides the configuration file and runs the wizard
    no args
      Loads standard configuration file and runs a wizard to guide through the options

Configuration File

    {
      "n_nodes" : 3,
      "packages" :
      [
        "gcc",
        "gcc­c++"
      ],
      "custom_scripts" :
      [
        { "name" : "custom.py", "interpreter" : "python" },
        { "name" : "custom.sh", "interpreter" : "bash" }
      ]
    }
