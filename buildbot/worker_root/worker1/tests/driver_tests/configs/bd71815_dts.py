dts={
'name':'bd71815',
#'dts_list':['protection_0'],
'i2c':{
    'bus':      2,
    'address':  0x4b,
    },

'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'buck1',
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
        'of_match':'buck2',
        'dts':{
            'default':{
                'regulator-ramp-delay': 5000,
            },
            'ramprate2':{
                'regulator-ramp-relay': 1250,
            },
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        },
        'test':{
            'default':{
                'ramprate':{
                    'reg_address':          0x06,
                    'bitmask':              0b11000000,
                    'register_value':       0b01000000,
                },
                'ramprate2':{
                    'reg_address':          0x06,
                    'bitmask':              0b11000000,
                    'register_value':       0b11000000,
                    },
            },
            'protection_0':{

                },
        },
    }, #buck2 END
    'buck3':{       #datasheet: buck5
        'name': 'buck3',
        'of_match': 'buck3',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck3 END
    'buck4':{       #datasheet: buck6
        'name': 'buck4',
        'of_match':'buck4',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck4 END
    'buck5':{       #datasheet: buck7
        'name': 'buck5',
        'of_match':'buck5',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck5 END
    'ldo1':{       #datasheet: LDO1
        'name': 'buck6',
        'of_match':'ldo1',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck7 END
    'ldo2':{       #datasheet: LDO2
        'name': 'buck7',
        'of_match':'ldo2',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck8 END
    'ldo3':{       #datasheet: LDO3
        'name': 'buck8',
        'of_match':'ldo3',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck9 END
    'ldo4':{       #datasheet: LDO4
        'name': 'buck9',
        'of_match':'ldo4',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0,
                'regulator-boot-on': True,
            },
        }
    }, #buck10 END
    'ldo5':{       #datasheet: LDO5
        'name': 'buck10',
        'of_match':'ldo5',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck11 END
    'ldodvref':{       #datasheet: LDO5
        'name': 'ldodvref',
        'of_match':'ldodvref',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck11 END
    'ldolpsr':{       #datasheet: LDO5
        'name': 'ldolpsr',
        'of_match':'ldolpsr',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    }, #buck11 END
    'wled':{       #datasheet: LDO6
        'name': 'wled',
        'of_match':'wled',
        'dts':{
            'protection_0':{
                'regulator-ov-protection-microvolt':0,
                'regulator-uv-protection-microvolt':0, 
            },
        }
    } #buck12 END
} #regulators END    
} #bd71847 END
