dts={
'name':'bd9576',
'i2c':{
    'bus':      2,
    'address':  0x30,
    },

'regulators':{
    'VD50':{    # VOUT1
        'name': 'buck1',
        'of_match': 'regulator-vd50',
        'dts':{
            'ov_uv':{
                'regulator-ov-error-microvolt':360000,
                'regulator-uv-error-microvolt':360000, 
            },
        },
        'test':{
            'ov_uv':{
                'ovd_set':{
                    'reg_address':          0x51,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 ovd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
                'uvd_set':{
                    'reg_address':          0x52,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 uvd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
            },
        },
    },
    'VD18':{    # VOUT2
        'name': 'buck2',
        'of_match':'regulator-vd18',
        'dts':{
            'ov_uv':{
                'regulator-ov-error-microvolt':360000,
                'regulator-uv-error-microvolt':360000, 
            },
        },
        'test':{
            'ov_uv':{
                'ovd_set':{
                    'reg_address':          0x51,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 ovd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
                'uvd_set':{
                    'reg_address':          0x52,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 uvd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
            },
        },
    },
    'VDDDR':{   # VOUT3
        'name': 'buck3',
        'of_match': 'BUCK3',
        'dts':{
            'ov_uv':{
                'regulator-ov-error-microvolt':360000,
                'regulator-uv-error-microvolt':360000, 
            },
        },
        'test':{
            'ov_uv':{
                'ovd_set':{
                    'reg_address':          0x51,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 ovd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
                'uvd_set':{
                    'reg_address':          0x52,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 uvd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
            },
        }
    },
    'VD10':{    # VOUT4
        'name': 'buck4',
        'of_match':'BUCK4',
        'dts':{
            'ov_uv':{
                'regulator-ov-error-microvolt':360000,
                'regulator-uv-error-microvolt':360000, 
            },
        },
        'test':{
            'ov_uv':{
                'ovd_set':{
                    'reg_address':          0x51,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 ovd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
                'uvd_set':{
                    'reg_address':          0x52,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 uvd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
            },
        },
    },
    'VOUTL1':{  # VOUTL1
        'name': 'buck5',
        'of_match':'BUCK5',
        'dts':{
            'ov_uv':{
                'regulator-ov-error-microvolt':360000,
                'regulator-uv-error-microvolt':360000, 
            },
        },
        'test':{
            'ov_uv':{
                'ovd_set':{
                    'reg_address':          0x51,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 ovd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
                'uvd_set':{
                    'reg_address':          0x52,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 uvd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
            },
        }
    },
    'VOUTS1':{  # VOUTS1
        'name': 'buck6',
        'of_match':'BUCK6',
        'dts':{
            'ov_uv':{
                'regulator-ov-error-microvolt':360000,
                'regulator-uv-error-microvolt':360000, 
            },
        },
        'test':{
            'ov_uv':{
                'ovd_set':{
                    'reg_address':          0x51,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 ovd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
                'uvd_set':{
                    'reg_address':          0x52,
                    'bitmask':              0b01111111,
                    'register_value':       0x47,
                    'comment':              "FAILURE: BUCK1 uvd_set: setting to allowed range with non-default value failed! 360mV, expected 0x47",
                },
            },
        }
    },
} #regulators END    
} #bd9576 END
