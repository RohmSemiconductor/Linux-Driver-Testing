####### BUILDERS

builders = {}

builders['builder_test_linux']= {
    'name': "builder_test_linux",
    'workernames': ["worker1"],
#    'factory': factory_test_linux,
}
builders['builder_linux-next']= {
    'name': "builder_linux-next",
    'workernames': ["worker1"],
    'factory': "factory",
}
