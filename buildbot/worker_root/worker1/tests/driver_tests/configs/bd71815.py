data={
'name':'bd71815',
'i2c':{
    'bus':      2,
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
        'bitmask':                      0x0F,
        'setting':                      0x0F,
        },
    'mvrfltmask2':{
        'address':                      0x24,
        'bitmask':                      0x3F,
        'setting':                      0x3F,
        },
},

'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'buck1',
        'regulator_en_address':         0x02,
        'regulator_en_bitmask':         0b00000100,

        'control_reg_address':          0x05,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate_bitmask':   0b11000000,

        'volt_reg_address':             0x0D,
        'volt_reg_bitmask':             0b01111111,
        
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
        'of_match':'buck2',
        'regulator_en_address':         0x03,
        'regulator_en_bitmask':         0b00000100,

        'control_reg_address':          0x06,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate':           0b11000000,

        'volt_reg_address':             0x10,
        'volt_reg_bitmask':             0b01111111,
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
        'of_match': 'buck3',
        'regulator_en_address':         0x04,
        'regulator_en_bitmask':         0b00000100,

        'control_reg_address':          0x09,
        'control_reg_bitmask':          0b00001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

        'volt_reg_address':             0x14,
        'volt_reg_bitmask':             0b00000111,

        'volt_sel':True,
        'volt_sel_address':             0x14,
        'volt_sel_bitmask':             0b11000000,
        'range':{
                0b00000000:{
                'volt_sel_reg':         0b00000000,
                'is_linear':False,
                'list_mV':[700,800,900,1000,1050,1100,1200,1350],
                'start_reg':0x00,
                'stop_reg':0x07,
            },
                0b01000000:{
                'volt_sel_reg':         0b01000000,
                'is_linear':True,
                'start_mV':550,
                'step_mV':50,
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
    }, #buck3 END
    'buck4':{
        'name': 'buck4',
        'of_match':'buck4',
        'regulator_en_address':     0x05,
        'regulator_en_bitmask':     0b00000100,

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
                'stop_reg':0x03,
            },
                0b00100000:{
                'is_linear':True,
                'start_mV':1600,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0x03,
            }
        }
    }, #buck4 END
    'buck5':{
        'name': 'buck5',
        'of_match':'buck5',
        'regulator_en_address':     0x06,
        'regulator_en_bitmask':     0b00000100,


        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x19,
        'volt_reg_bitmask':         0b00000000,

        'volt_sel':True,
        'volt_sel_bitmask':         0b00100000,
        'no_regulator_volt':        True,
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
            }
        }
    }, #buck5 END
    'buck6':{       #datasheet: LDO1
        'name': 'buck6',
        'of_match':'ldo1',
        'regulator_en_address':     0x10,
        'regulator_en_bitmask':     0b01000000,

        'volt_reg_address':         0x1A,
        'volt_reg_bitmask':         0b00001111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':1800,
                'step_mV':100,
                'start_reg':0x00,
                'stop_reg':0xF,
            },
                #     'flat':{
                #     'is_linear':True,
                #     'start_mV':1600,
                #     'step_mV':100,
                #     'start_reg':0x00,
                #     'stop_reg':0x03,
                # }
        }
    }, #buck6 END
    'buck7':{       #datasheet: LDO2
        'name': 'buck7',
        'of_match':'ldo2',
        'regulator_en_address':     0x11,
        'regulator_en_bitmask':     0b00000100,

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
    }, #buck7 END
    'buck8':{       #datasheet: LDO3
        'name': 'buck8',
        'of_match':'ldo3',
        'regulator_en_address':     0x11,
        'regulator_en_bitmask':     0b01000000,

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
    }, #buck8 END
    'buck9':{       #datasheet: LDO4
        'name': 'buck9',
        'of_match':'ldo4',
        'regulator_en_address':     0x12,
        'regulator_en_bitmask':     0b00000100,

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
    }, #buck9 END
    'buck10':{       #datasheet: LDO5
        'name': 'buck10',
        'of_match':'ldo5',
        'regulator_en_address':     0x12,
        'regulator_en_bitmask':     0b01000000,

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
    }, #buck7 END
} #regulators END    
} #bd##### END
