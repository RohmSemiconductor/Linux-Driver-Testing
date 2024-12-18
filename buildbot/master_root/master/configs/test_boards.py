test_boards ={}

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
test_boards['pmic'] = {
    'power_ports':{
        '1':{
            'beagle1':{
                'name':'beagle1',
                'products':['bd9576', 'bd71847'],
                'power_port':'1',
                'arch':'arm32',
            }
        }

        '2':{
            'beagle2':{
                'name':'beagle2',
                'products':['bd71815'],
                'power_port':'2',
                'arch':'arm32',
            }
        }
        '3':{
            'beagle3':{
                'name':'beagle3',
                'products':['bd71828'],
                'power_port':'3',
                'arch':'arm32',
            }
            'beagle4':{
                'name':'beagle4',
                'products':['bd96801', 'bd71837'],
                'power_port':'3',
                'arch':'arm32',
            }
        }
    } # end of pmic 'power_ports'
} # end of pmic


test_boards['accelerometer'] = {
    'power_ports':{
        '4':{
            'beagle5':{
                'name':'beagle5',
                'power_port':'4',
                'products':['kx022acr_z', 'kx132acr_lbz'],
                'arch':'arm32',
            }
        }
    }
}
