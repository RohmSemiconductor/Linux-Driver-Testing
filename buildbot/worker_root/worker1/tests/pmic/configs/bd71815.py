data={
'name':'bd71815',
'i2c':{
    'bus':      2,
    'address':  0x4b,
    },

'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'buck1',

        'regulator_en_address':         0x02,
        'regulator_en_bitmask':         0b00000100,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

        'settings':{
            'voltage':{
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
                },
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x02,
                'reg_bitmask':              0b11000000,
                'range':{
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [10, 5, 2.5, 1.25],
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
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 10 mV/us'
                },
            },

            'ramprate2':{
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
        'of_match':'buck2',

        'regulator_en_address':         0x03,
        'regulator_en_bitmask':         0b00000100,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

        'settings':{
            'voltage':{
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
                },
            },
            'ramprate':{
                'of_match': 'regulator-ramp-delay',
                'reg_address':              0x03,
                'reg_bitmask':              0b11000000,
                'range':{
                    'values':{
                        'is_linear':            False,
                        'list_mV':              [10, 5, 2.5, 1.25],
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
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 5 mV/us'
                },
            },

            'ramprate2':{
                'dts_properties':{
                    'regulator-ramp-delay': 1250,
                },
                'dts_error_comments':{
                    'regulator-ramp-delay': ' FAILURE: ramp rate failed to set to 1.25 mV/us'
                },
            },
	    },

    }, #buck2 END

    'buck3':{
        'name': 'buck3',
        'of_match': 'buck3',

        'regulator_en_address':         0x04,
        'regulator_en_bitmask':         0b00000100,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

        'settings':{
            'voltage':{
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
                }
            },
	    },
    }, #buck3 END

    'buck4':{
        'name': 'buck4',
        'of_match':'buck4',

        'regulator_en_address':     0x05,
        'regulator_en_bitmask':     0b00000100,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #buck4 END

    'buck5':{
        'name': 'buck5',
        'of_match':'buck5',

        'regulator_en_address':     0x06,
        'regulator_en_bitmask':     0b00000100,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #buck5 END

    'ldo1':{
        'name': 'buck6',
        'of_match':'ldo1',

        'regulator_en_address':     0x10,
        'regulator_en_bitmask':     0b01000000,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #ldo1 END

    'ldo2':{
        'name': 'buck7',
        'of_match':'ldo2',

        'regulator_en_address':     0x11,
        'regulator_en_bitmask':     0b00000100,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #ldo2 END

    'ldo3':{
        'name': 'buck8',
        'of_match':'ldo3',

        'regulator_en_address':     0x11,
        'regulator_en_bitmask':     0b01000000,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #ldo3 END

    'ldo4':{
        'name': 'buck9',
        'of_match':'ldo4',

        'regulator_en_address':     0x12,
        'regulator_en_bitmask':     0b00000100,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #ldo4 END

    'ldo5':{
        'name': 'buck10',
        'of_match':'ldo5',

        'regulator_en_address':     0x12,
        'regulator_en_bitmask':     0b01000000,

        'settings':{
            'voltage':{
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
            },
	    },
    }, #ldo5 END

    'wled':{
        'name': 'wled',
        'of_match':'wled',

        'regulator_en_address':     0x0E,
        'regulator_en_bitmask':     0b00000100,

        'settings':{
            'voltage':{
                'volt_reg_address':         0x0F,       #VOLT_H register
                'volt_reg_bitmask':         0b00111111,

                'volt_sel':False,

                'range':{
                        'values1':{
                        'is_linear':False,
                        'start_mV':800,
                        'step_mV':50,
                        'list_mV':[0.01,0.02,0.03,0.05,0.07,0.1,0.2,0.3,0.5,0.7],
                        'start_reg':0x0,
                        'stop_reg':0x09,
                    },
                        'values2':{
                        'is_linear':True,
                        'start_mV':1,
                        'step_mV':1,
                        'start_reg':0x0A,
                        'stop_reg':0x22,
                    },
                         #     'flat':{
                         #     'is_linear':True,
                         #     'start_mV':1600,
                         #     'step_mV':100,
                         #     'start_reg':0x00,
                         #     'stop_reg':0x03,
                         # }
                }
            },
	    },
    }, #wled END

    'ldodvref':{
        'name': 'ldodvref',
        'of_match':'ldodvref',
        'dts_only': True,
    }, #ldodvref END

    'ldolpsr':{
        'name': 'ldolpsr',
        'of_match':'ldolpsr',
        'dts_only': True,
    }, #ldolpsr END

} #regulators END
} #bd##### END
