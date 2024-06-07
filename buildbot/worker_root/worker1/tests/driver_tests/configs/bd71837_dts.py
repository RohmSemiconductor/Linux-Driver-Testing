dts={
'name':'bd71837',
#'dts_list':['protection_0'],
'i2c':{
    'bus':      1,
    'address':  0x4b,
    },

'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'BUCK1',
        'dts':{
            'default':{
                'regulator-ramp-delay': 10000,
            },
            'ramprate2':{
                'regulator-ramp-delay': 2500,
            },
        },
        'test':{
            'default':{
                'ramprate':{
                    'reg_address':          0x05,
                    'bitmask':              0b11000000,
                    'register_value':       0b00000000,
                },
            },
            'ramprate2':{
                'ramprate':{
                    'reg_address':          0x05,
                    'bitmask':              0b11000000,
                    'register_value':       0b10000000,
                    },
            },
        },
    }, #buck1 END
    'buck2':{
        'name': 'buck2',
        'of_match':'BUCK2',
        'dts':{
            'default':{
                'regulator-ramp-delay': 5000,
            },
            'ramprate2':{
                'regulator-ramp-relay': 1250,
            },
        },
        'test':{
            'default':{
                'ramprate':{
                    'reg_address':          0x06,
                    'bitmask':              0b11000000,
                    'register_value':       0b01000000,
                },
            },
            'ramprate2':{
                'ramprate':{
                    'reg_address':          0x06,
                    'bitmask':              0b11000000,
                    'register_value':       0b11000000,
                    },
            },
        },
    }, #buck2 END
    'buck3':{       #datasheet: buck5
        'name': 'buck3',
        'of_match': 'BUCK3',
        'dts':{
            'default':{
                'regulator-ramp-delay': 5000,
            },
            'ramprate2':{
                'regulator-ramp-relay': 1250,
            },
        },
        'test':{
            'default':{
                'ramprate':{
                    'reg_address':          0x07,
                    'bitmask':              0b11000000,
                    'register_value':       0b01000000,
                },
            },
            'ramprate2':{
                'ramprate':{
                    'reg_address':          0x07,
                    'bitmask':              0b11000000,
                    'register_value':       0b11000000,
                    },
            },
        },
    }, #buck3 END
    'buck4':{       #datasheet: buck6
        'name': 'buck4',
        'of_match':'BUCK4',
        'dts':{
            'default':{
                'regulator-ramp-delay': 5000,
            },
            'ramprate2':{
                'regulator-ramp-relay': 1250,
            },
        },
        'test':{
            'default':{
                'ramprate':{
                    'reg_address':          0x07,
                    'bitmask':              0b11000000,
                    'register_value':       0b01000000,
                },
            },
            'ramprate2':{
                'ramprate':{
                    'reg_address':          0x08,
                    'bitmask':              0b11000000,
                    'register_value':       0b11000000,
                    },
            },
        },
    }, #buck4 END
    'buck5':{       #datasheet: buck7
        'name': 'buck5',
        'of_match':'BUCK5',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck5 END
    'buck6':{       #datasheet: buck8
        'name': 'buck6',
        'of_match':'BUCK6',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck6 END
    'buck7':{       #datasheet: buck8
        'name': 'buck7',
        'of_match':'BUCK7',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck7 END
    'buck8':{       #datasheet: buck8
        'name': 'buck8',
        'of_match':'BUCK8',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck8 END
    'ldo1':{       #datasheet: LDO1
        'name': 'buck9',
        'of_match':'LDO1',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck7 END
    'ldo2':{       #datasheet: LDO2
        'name': 'buck10',
        'of_match':'LDO2',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck8 END
    'ldo3':{       #datasheet: LDO3
        'name': 'buck11',
        'of_match':'LDO3',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck9 END
    'ldo4':{       #datasheet: LDO4
        'name': 'buck12',
        'of_match':'LDO4',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0,
                'regulator-boot-on': True,
            },
        }
    }, #buck10 END
    'ldo5':{       #datasheet: LDO5
        'name': 'buck13',
        'of_match':'LDO5',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck11 END
    'ldo6':{       #datasheet: LDO6
        'name': 'buck14',
        'of_match':'LDO6',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck12 END
    'ldo7':{       #datasheet: LDO6
        'name': 'buck15',
        'of_match':'LDO7',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    } #buck12 END
} #regulators END    
} #bd71847 END
