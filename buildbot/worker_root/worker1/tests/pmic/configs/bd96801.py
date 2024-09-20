data={
'name':'bd96801',
'i2c':{
    'bus':      2,
    'address':  0x60,
},

'regulators':{
    'buck1':{
        #### 'name' = sysfs file name
        'name': 'buck1',
        'of_match': 'buck1',
        #### bd96801 has disable register, so reading ((0x0B return value) AND regulator_en_bitmask) == 0 means regulator is enabled
        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b00000001,

        'settings':{
            #### 'voltage' is the '...INI_VOUT' register
            'voltage':{
                'locked': True,
                'volt_reg_address': 0x21,
                'volt_reg_bitmask': 0b11111111,
                'volt_sel':     False,
                'range':{
                    'r1':{
                        'is_linear':    True,
                        'start_mV':     500,
                        'step_mV':      5,
                        'start_reg':    0x00,
                        'stop_reg':     0xC8,
                    },
                    'r2':{
                        'is_linear':    True,
                        'start_mV':     1550,
                        'step_mV':      50,
                        'start_reg':    0xC9,
                        'stop_reg':     0xEC,
                    },
                    'r3':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0xED,
                        'stop_reg':     0xFF,
                    },
                },
            },
            #### 'voltage_tune' is the BUCK#_TUNE register, which is an offset setting from the initial voltage setting ###
            'voltage_tune':{
                'reg_address':             0x28,
                'reg_bitmask':             0b00011111,

                'volt_sel': False,

                'range':{
                    'positive':{
                        'is_linear':    True,
                        'start_mV':     0,
                        'step_mV':      10,
                        'start_reg':    0x00,
                        'stop_reg':     0x0F,
                    },
                    'negative':{
                        'is_linear':    True,
                        'start_mV':     -150,
                        'step_mV':      10,
                        'start_reg':    0x10,
                        'stop_reg':     0x1F,
                    },
                },
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x28,
                'reg_bitmask':              0b11000000,
                'range':{
                    ### Datasheet has Volt / millisecond values, same as mV/us
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [1, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b11000000,
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
                    'regulator-ramp-delay': 1000,
                },
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 2.5 mV/us'
                },
            },
        },

    }, #buck1 END

    'buck2':{
        'name': 'buck2',
        'of_match':'buck2',

        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b00000010,

        'settings':{
            'voltage':{
                'locked': True,
                'volt_reg_address': 0x22,
                'volt_reg_bitmask': 0b11111111,
                'volt_sel':     False,
                'range':{
                    'r1':{
                        'is_linear':    True,
                        'start_mV':     500,
                        'step_mV':      5,
                        'start_reg':    0x00,
                        'stop_reg':     0xC8,
                    },
                    'r2':{
                        'is_linear':    True,
                        'start_mV':     1550,
                        'step_mV':      50,
                        'start_reg':    0xC9,
                        'stop_reg':     0xEC,
                    },
                    'r3':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0xED,
                        'stop_reg':     0xFF,
                    },
                },

            },
            #### 'voltage_tune' is the BUCK#_TUNE register, which is an offset setting from the initial voltage setting ###
            'voltage_tune':{
                'reg_address':             0x29,
                'reg_bitmask':             0b00011111,

                'volt_sel': False,

                'range':{
                    'positive':{
                        'is_linear':    True,
                        'start_mV':     0,
                        'step_mV':      10,
                        'start_reg':    0x00,
                        'stop_reg':     0x0F,
                    },
                    'negative':{
                        'is_linear':    True,
                        'start_mV':     -150,
                        'step_mV':      10,
                        'start_reg':    0x10,
                        'stop_reg':     0x1F,
                    },
                },
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x29,
                'reg_bitmask':              0b11000000,
                'range':{
                    ### Data sheet has Volt / millisecond values
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [1, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b11000000,
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
            },
        },

    }, #buck2 END

    'buck3':{
        'name': 'buck3',
        'of_match':'buck3',

        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b00000100,

        'settings':{
            'voltage':{
                'locked': True,
                'volt_reg_address': 0x23,
                'volt_reg_bitmask': 0b11111111,
                'volt_sel':     False,
                'range':{
                    'r1':{
                        'is_linear':    True,
                        'start_mV':     500,
                        'step_mV':      5,
                        'start_reg':    0x00,
                        'stop_reg':     0xC8,
                    },
                    'r2':{
                        'is_linear':    True,
                        'start_mV':     1550,
                        'step_mV':      50,
                        'start_reg':    0xC9,
                        'stop_reg':     0xEC,
                    },
                    'r3':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0xED,
                        'stop_reg':     0xFF,
                    },
                },

            },
            #### 'voltage_tune' is the BUCK#_TUNE register, which is an offset setting from the initial voltage setting ###
            'voltage_tune':{
                'reg_address':             0x2A,
                'reg_bitmask':             0b00011111,

                'volt_sel': False,

                'range':{
                    'positive':{
                        'is_linear':    True,
                        'start_mV':     0,
                        'step_mV':      10,
                        'start_reg':    0x00,
                        'stop_reg':     0x0F,
                    },
                    'negative':{
                        'is_linear':    True,
                        'start_mV':     -150,
                        'step_mV':      10,
                        'start_reg':    0x10,
                        'stop_reg':     0x1F,
                    },
                },
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x2A,
                'reg_bitmask':              0b11000000,
                'range':{
                    ### Data sheet has Volt / millisecond values
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [1, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b11000000,
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
                    'regulator-ramp-delay': 10000,
                },
            },
        },

    }, #buck3 END

    'buck4':{
        'name': 'buck4',
        'of_match':'buck4',

        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b00001000,

        'settings':{
            'voltage':{
                'locked': True,
                'volt_reg_address': 0x24,
                'volt_reg_bitmask': 0b11111111,
                'volt_sel':     False,
                'range':{
                    'r1':{
                        'is_linear':    True,
                        'start_mV':     500,
                        'step_mV':      5,
                        'start_reg':    0x00,
                        'stop_reg':     0xC8,
                    },
                    'r2':{
                        'is_linear':    True,
                        'start_mV':     1550,
                        'step_mV':      50,
                        'start_reg':    0xC9,
                        'stop_reg':     0xEC,
                    },
                    'r3':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0xED,
                        'stop_reg':     0xFF,
                    },
                },

            },
            #### 'voltage_tune' is the BUCK#_TUNE register, which is an offset setting from the initial voltage setting ###
            'voltage_tune':{
                'reg_address':             0x2B,
                'reg_bitmask':             0b00011111,

                'volt_sel': False,

                'range':{
                    'positive':{
                        'is_linear':    True,
                        'start_mV':     0,
                        'step_mV':      10,
                        'start_reg':    0x00,
                        'stop_reg':     0x0F,
                    },
                    'negative':{
                        'is_linear':    True,
                        'start_mV':     -150,
                        'step_mV':      10,
                        'start_reg':    0x10,
                        'stop_reg':     0x1F,
                    },
                },
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x2B,
                'reg_bitmask':              0b11000000,
                'range':{
                    ### Data sheet has Volt / millisecond values
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [1, 5, 10, 20],
                        'start_reg':            0b00000000,
                        'stop_reg':             0b11000000,
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
                    'regulator-ramp-delay': 20000,
                },
            },
        },

    }, #buck4 END

    'ldo5':{
        'name': 'buck5',
        'of_match':'ldo5',

        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b00010000,

        'settings':{
            'voltage':{
                'locked': True,
                'volt_reg_address': 0x25,
                'volt_reg_bitmask': 0b11111111,
                'volt_sel':     False,
                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     300,
                        'step_mV':      25,
                        'start_reg':    0x00,
                        'stop_reg':     0x78,
                    },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x79,
                        'stop_reg':     0xFF,
                    },
                },
            },
        },
    }, #ldo5 END

    'ldo6':{       #datasheet: ldo6
        'name': 'buck6',
        'of_match':'ldo6',

        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b00100000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x26,
                'volt_reg_bitmask':         0b11111111,

                'volt_sel': False,

                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     300,
                        'step_mV':      25,
                        'start_reg':    0x00,
                        'stop_reg':     0x78,
                    },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x79,
                        'stop_reg':     0xFF,
                    },
                },
            }
        },
    }, #ldo6 END

    'ldo7':{       #datasheet: ldo7
        'name': 'buck7',
        'of_match':'ldo7',

        'regulator_en_address':         0x0B,
        'regulator_en_bitmask':         0b01000000,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x27,
                'volt_reg_bitmask':         0b11111111,

                'volt_sel': False,

                'range':{
                    'values':{
                        'is_linear':    True,
                        'start_mV':     300,
                        'step_mV':      25,
                        'start_reg':    0x00,
                        'stop_reg':     0x78,
                    },
                    'flat':{
                        'is_linear':    True,
                        'start_mV':     3300,
                        'step_mV':      0,
                        'start_reg':    0x79,
                        'stop_reg':     0xFF,
                    },
                },
            },
	    },
    }, #ldo7 END
} #regulators END
} #bd96801 END
