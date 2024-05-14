data={
#'name':'',
'name':'bd71837',
'i2c':{
    'bus':      1,
    'address':  0x4b,
    },
'debug':{
    'vrfaulten':{
        'address':                      0x21,
        'bitmask':                      0x01,
        'setting':                      0x01,
     },
    'mvrfltmask0':{
        'address':                      0x22,
        'bitmask':                      0xFF,
        'setting':                      0xFF,
        },
    'mvrfltmask1':{
        'address':                      0x23,
        'bitmask':                      0xFF,
        'setting':                      0xFF,
        },
    'mvrfltmask2':{
        'address':                      0x24,
        'bitmask':                      0x7F,
        'setting':                      0x7F,
        },
},

'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'BUCK1',
        'regulator_en_address':         0x05,
        'regulator_en_bitmask':         0b00000001,

        'control_reg_address':          0x05,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate_bitmask':   0b11000000,

        'volt_reg_address':             0x0D,
        'volt_reg_bitmask':             0b00111111,
        
        'volt_sel': False,
        
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     700,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x3C,
            },
            # 'flat':{
            #     'is_linear':True,
            #     'start_mV':1300,
            #     'step_mV':0,
            #     'start_reg':0x3D,
            #     'stop_reg':0x7F,
            # }
        }
    }, #buck1 END
    'buck2':{
        'name': 'buck2',
        'of_match':'BUCK2',
        'regulator_en_address':         0x06,
        'regulator_en_bitmask':         0b00000001,

        'control_reg_address':          0x06,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate':           0b11000000,

        'volt_reg_address':             0x10,
        'volt_reg_bitmask':             0b00111111,
        'volt_sel': False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     700,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x3C,
            },
            # 'flat':{
            #     'is_linear':True,
            #     'start_mV':1300,
            #     'step_mV':0,
            #     'start_reg':0x3D,
            #     'stop_reg':0x7F,
            # }
        }
    }, #buck2 END
    'buck3':{
        'name': 'buck3',
        'of_match':'BUCK3',
        'regulator_en_address':         0x07,
        'regulator_en_bitmask':         0b00000001,

        'control_reg_address':          0x07,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate':           0b11000000,

        'volt_reg_address':             0x12,
        'volt_reg_bitmask':             0b00111111,
        'volt_sel': False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     700,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x3C,
            },
            # 'flat':{
            #     'is_linear':True,
            #     'start_mV':1300,
            #     'step_mV':0,
            #     'start_reg':0x3D,
            #     'stop_reg':0x7F,
            # }
        }
    }, #buck3 END
    'buck4':{
        'name': 'buck4',
        'of_match':'BUCK4',
        'regulator_en_address':         0x08,
        'regulator_en_bitmask':         0b00000001,

        'control_reg_address':          0x08,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate':           0b11000000,

        'volt_reg_address':             0x13,
        'volt_reg_bitmask':             0b00111111,
        'volt_sel': False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     700,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x3C,
            },
            # 'flat':{
            #     'is_linear':True,
            #     'start_mV':1300,
            #     'step_mV':0,
            #     'start_reg':0x3D,
            #     'stop_reg':0x7F,
            # }
        }
    }, #buck4 END
    'buck5':{
        'name': 'buck5',
        'of_match': 'BUCK5',
        'regulator_en_address':         0x09,
        'regulator_en_bitmask':         0b00000001,

        'control_reg_address':          0x09,
        'control_reg_bitmask':          0b00001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':             0x14,
        'volt_reg_bitmask':             0b00000111,

        'volt_sel':True,
        'volt_sel_address':             0x14,
        'volt_sel_bitmask':             0b10000000,
        'range':{
                0b00000000:{
                'is_linear':False,
                'list_mV':[700,800,900,1000,1050,1100,1200,1350],
                'start_reg':0x00,
                'stop_reg':0x07,
            },
                0b10000000:{
                'is_linear':False,
                'list_mV':[675,775,875,975,1025,1075,1175,1325],
                'start_reg':0x00,
                'stop_reg':0x07,
            }
        } #ranges ok
    }, #buck5 END
    'buck6':{   
        'name': 'buck6',
        'of_match':'BUCK6',
        'regulator_en_address':     0x0A,
        'regulator_en_bitmask':     0b00000001,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x15,
        'volt_reg_bitmask':         0b00000011,

        'volt_sel':False,
        'range':{
                0b00000000:{
                'is_linear':True,
                'start_mV':3000,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x03,
            },
        }
    }, #buck6 END
    'buck7':{
        'name': 'buck7',
        'of_match':'BUCK7',
        'regulator_en_address':     0x0B,
        'regulator_en_bitmask':     0b00000001,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x16,
        'volt_reg_bitmask':         0b00000111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':False,
                'list_mV':[1605,1695,1755,1800,1845,1905,1950,1995],
                'start_reg':0x00,
                'stop_reg':0x07,
                }
        }
    }, #buck7 END
    'buck8':{
        'name': 'buck8',
        'of_match':'BUCK8',
        'regulator_en_address':     0x0C,
        'regulator_en_bitmask':     0b00000001,


        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x17,
        'volt_reg_bitmask':         0b00111111,

        'volt_sel':False,
        'volt_sel_bitmask':         0b00100000,
        'no_regulator_volt':        True,
        'range':{
                'values':{
                'is_linear':    True,
                'start_mV':     800,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x3C,
            },
        }
    }, #buck8 END
    'buck9':{       #datasheet: LDO1
        'name': 'buck9',
        'of_match':'LDO1',
        'regulator_en_address':     0x18,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x18,
        'volt_reg_bitmask':         0b00000011,
        'volt_sel':True,
        'volt_sel_bitmask':         0b00100000,
        'range':{
                0b00000000:{
                'is_linear':True,
                'start_mV':3000,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x3,
            },
                0b00100000:{
                'is_linear':True,
                'start_mV':1600,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x3,
            },
                #     'flat':{
                #     'is_linear':True,
                #     'start_mV':1600,
                #     'step_mV':100,
                #     'start_reg':0x00,
                #     'stop_reg':0x03,
                # }
        }
    }, #buck9 END
    'buck10':{       #datasheet: LDO2
        'name': 'buck10',
        'of_match':'LDO2',
        'regulator_en_address':     0x19,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x19,
        'volt_reg_bitmask':         0b00000000,
        'volt_sel':True,
        'volt_sel_bitmask':         0b00100000,
        'range':{
                0b00000000:{
                'is_linear':True,
                'start_mV':900,
                'step_mV':0,
                'start_reg':0x00,
                'stop_reg':0x00,
            },
                0b00100000:{
                'is_linear':True,
                'start_mV':800,
                'step_mV':0,
                'start_reg':0x00,
                'stop_reg':0x00,
            },
                #     'flat':{
                #     'is_linear':True,
                #     'start_mV':1600,
                #     'step_mV':100,
                #     'start_reg':0x00,
                #     'stop_reg':0x03,
                # }
        }
    }, #buck10 END
    'buck11':{       #datasheet: LDO3
        'name': 'buck11',
        'of_match':'LDO3',
        'regulator_en_address':     0x1A,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x1A,
        'volt_reg_bitmask':         0b00001111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':1800,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x0F,
            },
                 #     'flat':{
                 #     'is_linear':True,
                 #     'start_mV':1600,
                 #     'step_mV':100,
                 #     'start_reg':0x00,
                 #     'stop_reg':0x03,
                 # }
        }
    }, #buck11 END
    'buck12':{       #datasheet: LDO4
        'name': 'buck12',
        'of_match':'LDO4',
        'regulator_en_address':     0x1B,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x1B,
        'volt_reg_bitmask':         0b00001111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':900,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x09,
            },
                 #     'flat':{
                 #     'is_linear':True,
                 #     'start_mV':1600,
                 #     'step_mV':100,
                 #     'start_reg':0x00,
                 #     'stop_reg':0x03,
                 # }
        }
    }, #buck12 END
    'buck13':{       #datasheet: LDO5
        'name': 'buck13',
        'of_match':'LDO5',
        'regulator_en_address':     0x1C,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x1C,
        'volt_reg_bitmask':         0b00001111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':1800,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x0F,
            },
                 #     'flat':{
                 #     'is_linear':True,
                 #     'start_mV':1600,
                 #     'step_mV':100,
                 #     'start_reg':0x00,
                 #     'stop_reg':0x03,
                 # }
        }
    }, #buck13 END
    'buck14':{       #datasheet: LDO6
        'name': 'buck14',
        'of_match':'LDO6',
        'regulator_en_address':     0x1D,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x1D,
        'volt_reg_bitmask':         0b00001111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':900,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x09,
            },
                 #     'flat':{
                 #     'is_linear':True,
                 #     'start_mV':1600,
                 #     'step_mV':100,
                 #     'start_reg':0x00,
                 #     'stop_reg':0x03,
                 # }
        }
    }, #buck14 END
    'buck15':{       #datasheet: LDO7
        'name': 'buck15',
        'of_match':'LDO7',
        'regulator_en_address':     0x1E,
        'regulator_en_bitmask':     0b01000000,

        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x1E,
        'volt_reg_bitmask':         0b00001111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':1800,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x0F,
            },
                 #     'flat':{
                 #     'is_linear':True,
                 #     'start_mV':1600,
                 #     'step_mV':100,
                 #     'start_reg':0x00,
                 #     'stop_reg':0x03,
                 # }
        }
    } #buck15 END
# root@arm:/sys/kernel/mva_test/regulators# echo 3200000 3200000 > buck13_set
# bash: echo: write error: Device or resource busy

} #regulators END    
} #bd71837 END
