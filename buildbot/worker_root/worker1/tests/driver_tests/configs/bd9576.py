data={
'name':'bd9576',
'i2c':{
    'bus':      2,
    'address':  0x30,
    },

'regulators':{
    'buck1':{
        'name': 'buck1',
        'of_match': 'regulator-vd50',
        'regulator_en_address':         0x41,
        'regulator_en_bitmask':         0b11111111,

        'control_reg_address':          0x05,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate_bitmask':   0b11000000,

        'volt_reg_address':             0x50,
        'volt_reg_bitmask':             0b00000111,
        
        'volt_sel': False,
        
        'range':{
            'values':{
                'is_linear':            True,
                'is_offset_bipolar':    True,
                'offset_sign_bitmask':  0b1000000,
                'offset_sign_address':  0x50,
                'start_mV':             5000,
                'step_mV':              100,
                'start_reg':            0x00,
                'stop_reg':             0x05,
            }
        },
        'limit_settings':{
            'ovd':{
                'of_match': 'regulator-ov-error-microvolt',
                'reg_address': 0x51,
                'reg_bitmask': 0b01111111,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             225,
                        'step_mV':              5,
                        'start_reg':            0x2C,
                        'stop_reg':             0x54,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             225,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x2B,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             425,
                        'step_mV':              0,
                        'start_reg':            0x55,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            },
            'uvd':{
                'of_match': 'regulator-uv-error-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x52,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             225,
                        'step_mV':              5,
                        'start_reg':            0x2C,
                        'stop_reg':             0x54,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             225,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x2B,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             425,
                        'step_mV':              0,
                        'start_reg':            0x55,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            }
        },
    }, #buck1 END
    'buck2':{
        'name': 'buck2',
        'of_match':'regulator-vd18',
        'regulator_en_address':         0x42,
        'regulator_en_bitmask':         0b11111111,

        'control_reg_address':          0x06,
        'control_reg_bitmask':          0b11001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,
        'regulator_ramprate':           0b11000000,

        'volt_reg_address':             0x53,
        'volt_reg_bitmask':             0b00000111,
        'volt_sel': False,
        'range':{
            'values':{
                'is_linear':    True,
                'is_bipolar':   True,
                'sign_bitmask': 0b1000000,
                'sign_address': 0x53,
                'start_mV':     1800,
                'step_mV':      20,
                'start_reg':    0x00,
                'stop_reg':     0x07,
            },
        },
        'limit_settings':{
            'ovd':{
                'of_match': 'regulator-ov-error-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x54,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              1,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             110,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            },
            'uvd':{
                'of_match': 'regulator-uv-error-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x55,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              1,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             110,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            }
        }
    }, #buck2 END
    'buck3':{
        'name': 'buck3',
        'of_match': 'regulator-vdddr',
        'regulator_en_address':         0x43,
        'regulator_en_bitmask':         0b11111111,

        'control_reg_address':          0x09,
        'control_reg_bitmask':          0b00001011,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

        'volt_reg_address':             0x56,
        'volt_reg_bitmask':             0b00011111,

        'volt_sel': False,
        'range':{
            'values':{
                'is_linear':    True,
                'is_bipolar':   True,
                'sign_bitmask': 0b1000000,
                'sign_address': 0x56,
                'start_mV':     1350,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x1F,
            },     
        }, #ranges ok
        'limit_settings':{

            'ovd':{
                'of_match': 'regulator-ov-warn-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x57,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              1,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             110,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            },
            'uvd':{
                'of_match': 'regulator-uv-warn-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x58,
                'range': {
                    'values':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              1,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             110,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            }
        }
    }, #buck3 END
    'buck4':{
        'name': 'buck4',
        'of_match':'regulator-vd10',
        'regulator_en_address':     0x44,
        'regulator_en_bitmask':     0b11111111,

        'volt_reg_address':         0x59,
        'volt_reg_bitmask':         0b00011111,
        
        'volt_sel':False,
        'range':{
            'values':{
                'is_linear':    True,
                'is_bipolar':   True,
                'sign_bitmask': 0b1000000,
                'sign_address': 0x59,
                'start_mV':     1030,
                'step_mV':      10,
                'start_reg':    0x00,
                'stop_reg':     0x1F,
            },
             
        }, #ranges ok
        'limit_settings':{
            'ovd':{
                'of_match': 'regulator-ov-warn-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x5A,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              1,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             110,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            },
            'uvd':{
                'of_match': 'regulator-uv-error-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x5B,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              1,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             17,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             110,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            }
        }
    }, #buck4 END
    'buck5':{
        'name': 'buck5',
        'of_match':'regulator-voutl1',
        'regulator_en_address':     0x45,
        'regulator_en_bitmask':     0b11111111,


        'volt_change_not_allowed_while_on': True,
        'volt_reg_address':         0x5C,
        'volt_reg_bitmask':         0b00000111,

        'volt_sel':False,
        'range':{
            'values':{
                'is_linear':    True,
                'is_bipolar':   True,
                'sign_bitmask': 0b1000000,
                'sign_address': 0x5C,
                'start_mV':     2500,
                'step_mV':      40,
                'start_reg':    0x00,
                'stop_reg':     0x7,
            },

        }, #ranges ok
        'limit_settings':{
            'ovd':{
                'of_match': 'regulator-ov-error-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x5D,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             34,
                        'step_mV':              2,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             34,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             220,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            },
            'uvd':{
                'of_match': 'regulator-uv-error-microvolt',
                'reg_bitmask':              0b01111111,
                'reg_address':              0x5E,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             34,
                        'step_mV':              2,
                        'start_reg':            0x10,
                        'stop_reg':             0x6D,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             34,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x0F,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             220,
                        'step_mV':              0,
                        'start_reg':            0x6E,
                        'stop_reg':             0x7F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                    }
                }
            }
        }
    }, #buck5 END
    'buck6':{
        'name': 'buck6',
        'of_match':'regulator-vouts1',
        'regulator_en_address':     0x46,
        'regulator_en_bitmask':     0b11111111,

        'volt_sel':False,
        'range':{
                'values':{
                'is_linear':True,
                'start_mV':3300,
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
        },
        'limit_settings':{
            'ocw':{ #start_mV, step_mV are milliamperes here
                'of_match': 'regulator-oc-warn-microamp',
                'reg_bitmask':              0b00111111,
                'reg_address':              0x5F,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             200,
                        'step_mV':              50,
                        'start_reg':            0x04,
                        'stop_reg':             0x18,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             200,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x03,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             1200,
                        'step_mV':              0,
                        'start_reg':            0x19,
                        'stop_reg':             0x3F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                        }
                }
            },
            'ocp':{
                'of_match': 'regulator-oc-protection-microamp',
                'reg_bitmask':              0b00111111,
                'reg_address':              0x60,
                'range':{
                    'values':{
                        'is_linear':            True,
                        'start_mV':             300,
                        'step_mV':              50,
                        'start_reg':            0x06,
                        'stop_reg':             0x1B,
                    },
                    'clip_low':{
                        'is_linear':            True,
                        'start_mV':             300,
                        'step_mV':              0,
                        'start_reg':            0x01,
                        'stop_reg':             0x05,
                    },
                    'clip_high':{
                        'is_linear':            True,
                        'start_mV':             1350,
                        'step_mV':              0,
                        'start_reg':            0x1C,
                        'stop_reg':             0x3F,
                    },
                    'disabled':{
                        'is_linear':            True,
                        'start_mV':             0,
                        'step_mV':              0,
                        'start_reg':            0x00,
                        'stop_reg':             0x00,
                        }
                }
            }
        }
    }, #buck6 END
} #regulators END    
} #bd##### END
