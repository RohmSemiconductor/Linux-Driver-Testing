data={
'name':'bd71828',
'i2c':{
    'bus':      2,
    'address':  0x4b,
    },

### 'debug' is to disable vrfault at sanitycheck stage

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

### 
'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'BUCK1',

        'regulator_en_address':         0x08,
        'regulator_en_bitmask':         0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':             0x0D,
                'volt_reg_bitmask':             0b11111111,

                'volt_sel': False,

                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     500,
                        'step_mV':      6.25,
                        'start_reg':    0x00,
                        'stop_reg':     0xEF,
                        },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     2000,
                        'step_mV':      0,
                        'start_reg':    0xF0,
                        'stop_reg':     0xFF,
                        },
                },
            },
            'idle_on':{
                'reg_address':          0x08,
                'reg_bitmask':          0b00000010,
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x0A,
                'reg_bitmask':              0b00000110,
                'range':{
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [2.5, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b00000110,
                    },
                },    
            },
        }, 

        #### DEVICE TREE TEST SECTION
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ramp-delay': 2500,
                },
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 2.5 mV/us'
                },
            },
        },

    }, #buck1 END

    'buck2':{
        'name': 'buck2',
        'of_match':'BUCK2',

        'regulator_en_address':         0x12,
        'regulator_en_bitmask':         0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':             0x17,
                'volt_reg_bitmask':             0b11111111,

                'volt_sel': False,

                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     500,
                        'step_mV':      6.25,
                        'start_reg':    0x00,
                        'stop_reg':     0xEF,
                        },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     2000,
                        'step_mV':      0,
                        'start_reg':    0xF0,
                        'stop_reg':     0xFF,
                        },
                },
            },
            'idle_on':{
                'reg_address':          0x12,
                'reg_bitmask':          0b00000010,
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x14,
                'reg_bitmask':              0b00000110,
                'range':{
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [2.5, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b00000110,
                    },
                },
            },
        }, 

        #### DEVICE TREE TEST SECTION
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ramp-delay': 5000,
                },
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 5 mV/us'
                },
            },
        }
    }, #buck2 END

    'buck3':{
        'name': 'buck3',
        'of_match':'BUCK3',

        'regulator_en_address':         0x1C,
        'regulator_en_bitmask':         0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':             0x1E,
                'volt_reg_bitmask':             0b11111111,

                'volt_sel': False,

                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     1200,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x0F,
                        },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     2000,
                        'step_mV':      0,
                        'start_reg':    0x10,
                        'stop_reg':     0x1F,
                        },
                },
            },
            'idle_on':{
                'reg_address':          0x1C,
                'reg_bitmask':          0b00000010,
            },
        }, 

        #### DEVICE TREE TEST SECTION
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

    }, #buck3 END

    'buck4':{
        'name': 'buck4',
        'of_match':'BUCK4',

        'regulator_en_address':         0x1F,
        'regulator_en_bitmask':         0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':             0x21,
                'volt_reg_bitmask':             0b00111111,

                'volt_sel': False,

                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     1000,
                        'step_mV':      25,
                        'start_reg':    0x00,
                        'stop_reg':     0x1F,
                    },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     1800,
                        'step_mV':      0,
                        'start_reg':    0x20,
                        'stop_reg':     0x3F,
                        },
                },
            },
            'idle_on':{
                'reg_address':          0x1F,
                'reg_bitmask':          0b00000010,
            },
        }, 

        #### DEVICE TREE TEST SECTION
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

    }, #buck4 END

    'buck5':{
        'name': 'buck5',
        'of_match': 'BUCK5',

        'regulator_en_address':         0x22,
        'regulator_en_bitmask':         0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':             0x24,
                'volt_reg_bitmask':             0b11111111,

                'volt_sel':False,

                'range':{
                        'values':{
                        'is_linear':    True,
                        'start_mV':     2500,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x0F,
                    },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x10,
                        'stop_reg':     0x1F,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x22,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #buck5 END

    'buck6':{
        'name': 'buck6',
        'of_match':'BUCK6',

        'regulator_en_address':     0x25,
        'regulator_en_bitmask':     0b00001000,
        'volt_change_not_allowed_while_on': True,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x2A,
                'volt_reg_bitmask':         0b11111111,

                'volt_sel':False,

                'range':{
                        'values':{
                        'is_linear':True,
                        'start_mV':500,
                        'step_mV':6.25,
                        'start_reg':0x00,
                        'stop_reg':0xEF,
                        },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     2000,
                        'step_mV':      0,
                        'start_reg':    0xF0,
                        'stop_reg':     0xFF,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x25,
                'reg_bitmask':          0b00000010,
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x27,
                'reg_bitmask':              0b00000110,
                'range':{
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [2.5, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b00000110,
                    },
                },
            },
	    },
        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ramp-delay': 10000,
                },
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 10 mV/us'
                },
            },
        },
    }, #buck6 END

    'buck7':{
        'name': 'buck7',
        'of_match':'BUCK7',

        'regulator_en_address':     0x2F,
        'regulator_en_bitmask':     0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x34,
                'volt_reg_bitmask':         0b11111111,

                'volt_sel':False,
                
                'range':{
                        'values':{
                        'is_linear':True,
                        'start_mV':500,
                        'step_mV':6.25,
                        'start_reg':0x00,
                        'stop_reg':0xEF,
                        },
                        'flat':{
                        'is_linear':    True,
                        'start_mV':     2000,
                        'step_mV':      0,
                        'start_reg':    0xF0,
                        'stop_reg':     0xFF,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x2F,
                'reg_bitmask':          0b00000010,
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x31,
                'reg_bitmask':              0b00000110,
                'range':{
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [2.5, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b00000110,
                    },
                },
            },
	    },
        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ramp-delay': 20000,
                },
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 20 mV/us'
                },
            },
        },
    }, #buck7 END

    'ldo1':{
        'name': 'buck8',
        'of_match':'LDO1',
        'regulator_en_address':     0x39,
        'regulator_en_bitmask':     0b00001000,

        'volt_change_not_allowed_while_on': True,
        'settings':{
            'voltage':{	
                'volt_reg_address':         0x3A,
                'volt_reg_bitmask':         0b00111111,

                'volt_sel': False,
                
                'range':{
                    'values':{
                        'is_linear':True,
                        'start_mV':800,
                        'step_mV':50,
                        'start_reg':0x00,
                        'stop_reg':0x31,
                        },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x32,
                        'stop_reg':     0x3F,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x39,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #ldo1 END

    'ldo2':{       #datasheet: LDO2
        'name': 'buck9',
        'of_match':'LDO2',
        'regulator_en_address':     0x3B,
        'regulator_en_bitmask':     0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x3C,
                'volt_reg_bitmask':         0b00111111,

                'volt_sel': False,
                
                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     800,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x31,
                        },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x32,
                        'stop_reg':     0x3F,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x3B,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #ldo2 END

    'ldo3':{       #datasheet: LDO3
        'name': 'buck10',
        'of_match':'LDO3',
        'regulator_en_address':     0x3D,
        'regulator_en_bitmask':     0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x3E,
                'volt_reg_bitmask':         0b00111111,

                'volt_sel': False,
                
                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     800,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x31,
                        },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x32,
                        'stop_reg':     0x3F,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x3D,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #ldo3 END

    'ldo4':{       #datasheet: LDO4
        'name': 'buck11',
        'of_match':'LDO4',
        'regulator_en_address':     0x3F,
        'regulator_en_bitmask':     0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x40,
                'volt_reg_bitmask':         0b00111111,

                'volt_sel': False,
                
                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     800,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x31,
                        },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x32,
                        'stop_reg':     0x3F,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x3F,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #ldo4 END

    'ldo5':{       #datasheet: LDO5
        'name': 'buck12',
        'of_match':'LDO5',
        'regulator_en_address':     0x41,
        'regulator_en_bitmask':     0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x43,       #LDO5_VOLT_L
                'volt_reg_bitmask':         0b00111111,

                'volt_sel': False,
                
                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     800,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x31,
                        },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x32,
                        'stop_reg':     0x3F,
                        },
                }
            },
            'idle_on':{
                'reg_address':          0x41,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #ldo5 END

    'ldo6':{       #datasheet: LDO6
        'name': 'buck13',
        'of_match':'LDO6',

        'regulator_en_address':     0x44,
        'regulator_en_bitmask':     0b00001000,
        'no_voltage_register':      True,
        'settings':{
            'idle_on':{
                'reg_address':          0x44,
                'reg_bitmask':          0b00000010,
            },
	    },
    }, #ldo6 END

    'ldo7':{       #datasheet: LDO_SNVS
        'name': 'buck14',
        'of_match':'LDO7',

        'regulator_en_address':     0x45,
        'regulator_en_bitmask':     0b00001000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x46,
                'volt_reg_bitmask':         0b00111111,

                'volt_sel': False,
                
                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     800,
                        'step_mV':      50,
                        'start_reg':    0x00,
                        'stop_reg':     0x31,
                        },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x32,
                        'stop_reg':     0x3F,
                        },
                }
            },
	    },
            'idle_on':{
                'reg_address':          0x45,
                'reg_bitmask':          0b00000010,
            },
    } #ldo7 END

} #regulators END    
} #bd71828 END
