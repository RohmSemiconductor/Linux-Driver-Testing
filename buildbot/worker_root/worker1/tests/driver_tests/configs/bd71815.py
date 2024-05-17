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

        'volt_reg_address':             0x07,       #VOLT_H register
        'volt_reg_bitmask':             0b00111111,
        
        'volt_sel': False,
        
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     800,
                'step_mV':      25,
                'start_reg':    0x0,
                'stop_reg':     0x30,
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

        'volt_reg_address':             0x09,       #VOLT_H
        'volt_reg_bitmask':             0b00111111,
        'volt_sel': False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     800,
                'step_mV':      25,
                'start_reg':    0x0,
                'stop_reg':     0x30,
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

        'volt_reg_address':             0x0B,
        'volt_reg_bitmask':             0b00011111,

        'volt_sel':False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     1200,
                'step_mV':      50,
                'start_reg':    0x0,
                'stop_reg':     0x1E,
            },
        } #ranges ok
    }, #buck3 END
    'buck4':{
        'name': 'buck4',
        'of_match':'buck4',
        'regulator_en_address':     0x05,
        'regulator_en_bitmask':     0b00000100,

        'volt_reg_address':         0x0C,
        'volt_reg_bitmask':         0b00011111,
        'volt_sel':False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     1100,
                'step_mV':      25,
                'start_reg':    0x0,
                'stop_reg':     0x1E,
            },
        }
    }, #buck4 END
    'buck5':{
        'name': 'buck5',
        'of_match':'buck5',
        'regulator_en_address':     0x06,
        'regulator_en_bitmask':     0b00000100,

        'volt_reg_address':         0x0D,
        'volt_reg_bitmask':         0b00011111,

        'volt_sel':False,
        'range':{
            'values':{
                'is_linear':    True,
                'start_mV':     1800,
                'step_mV':      50,
                'start_reg':    0x0,
                'stop_reg':     0x1E,
            },
        }
    }, #buck5 END
    'buck6':{       #datasheet: LDO1
        'name': 'buck6',
        'of_match':'ldo1',
        'regulator_en_address':     0x10,
        'regulator_en_bitmask':     0b01000000,

        'volt_reg_address':         0x14,
        'volt_reg_bitmask':         0b00111111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':800,
                'step_mV':50,
                'start_reg':0x0,
                'stop_reg':0x32,
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

        'volt_reg_address':         0x15,
        'volt_reg_bitmask':         0b00111111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':800,
                'step_mV':50,
                'start_reg':0x0,
                'stop_reg':0x32,
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

        'volt_reg_address':         0x16,
        'volt_reg_bitmask':         0b00111111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':800,
                'step_mV':50,
                'start_reg':0x0,
                'stop_reg':0x32,
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

        'volt_reg_address':         0x17,
        'volt_reg_bitmask':         0b00111111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':800,
                'step_mV':50,
                'start_reg':0x0,
                'stop_reg':0x32,
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

        'volt_reg_address':         0x18,       #VOLT_H register
        'volt_reg_bitmask':         0b00111111,
        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':800,
                'step_mV':50,
                'start_reg':0x0,
                'stop_reg':0x32,
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
