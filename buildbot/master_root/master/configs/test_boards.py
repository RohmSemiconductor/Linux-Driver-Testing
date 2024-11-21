test_boards ={}

product_types = {
        'PMIC':             ['bd9576', 'bd71847', 'bd71837', 'bd71828', 'bd96801'],
        'accelerometer':    ['kx022acr_z', 'kx132acr_lbz']
        }

#test_boards['beagle1']={
#'name':'beagle1',
#'products':['bd9576','bd71847'],
#'power_port':'1',
#'arch':'arm32',
#}
#
#test_boards['beagle2']={
#'name':'beagle2',
#'products':['bd71815'],
#'power_port':'2',
#'arch':'arm32',
#}
#
#test_boards['beagle3']={
#'name':'beagle3',
#'products':['bd71828'],
#'power_port':'3',
#'arch':'arm32',
#}
#
#test_boards['beagle4']={
#'name':'beagle4',
#'products':['bd96801', 'bd71837'],
#'power_port':'4',
#'arch':'arm32',
#}

test_boards['beagle5']={
'name':'beagle5',
'products':['kx022acr_z'],
#'products':['kx022acr-z', 'kx132acr-lbz'],
'power_port':'4',
'arch':'arm32',
}
