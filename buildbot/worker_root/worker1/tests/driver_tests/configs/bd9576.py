data={
'name':'bd9576',
'i2c':{
    'bus':      2,
    'address':  0x30,
    },

'regulators':{
    'VD50':{
        'name': 'buck1',
        'of_match': 'regulator-vd50',
        'regulator_en_address':         0x41,
        'regulator_en_bitmask':         0b11111111,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

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

        'settings':{
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

        #### DEVICE TREE TEST SECTION 
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{

            'default':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 360000,
                    'regulator-uv-error-microvolt': 360000,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to set to 360 mV',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to set to 360 mV',
                },
            },

            'ovd_uvd_disable':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 0,
                    'regulator-uv-error-microvolt': 0,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to disable',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to disable',
                },

            },
        },
    }, # VD50

    'VD18':{
        'name': 'buck2',
        'of_match':'regulator-vd18',

        'regulator_en_address':         0x42,
        'regulator_en_bitmask':         0b11111111,

        'regulator_sel_bitmask':        0b00000010,
        'regulator_pwm_fix_bitmask':    0b00001000,

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

        'settings':{
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
        },

        #### DEVICE TREE TEST SECTION 
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{

            'default':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 18000,
                    'regulator-uv-error-microvolt': 109000,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to set to 18 mV',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to set to 109 mV',
                },
            },

            'ovd_uvd_disable':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 0,
                    'regulator-uv-error-microvolt': 0,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to disable',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to disable',
                },

            },
        },
    }, #VD18 END

    'VDDDR':{
        'name': 'buck3',
        'of_match': 'regulator-vdddr',
        'regulator_en_address':         0x43,
        'regulator_en_bitmask':         0b11111111,

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
        },
        
        'settings':{
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
        },

        #### DEVICE TREE TEST SECTION 
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ov-warn-microvolt': 110000,
                    'regulator-uv-warn-microvolt': 110000,
                },
                'dts_error_comments':{
                    'regulator-ov-warn-microvolt': ' FAILURE: OVD SET failed to set to 110 mV (high clip)',
                    'regulator-uv-warn-microvolt': ' FAILURE: UVD SET failed to set to 110 mV (high clip)',
                },
            },

            'ovd_uvd_disable':{
                'dts_properties':{
                    'regulator-ov-warn-microvolt': 0,
                    'regulator-uv-warn-microvolt': 0,
                },
                'dts_error_comments':{
                    'regulator-ov-warn-microvolt': ' FAILURE: OVD SET failed to disable',
                    'regulator-uv-warn-microvolt': ' FAILURE: UVD SET failed to disable',
                },
            },
        },
    }, #VDDDR END

    'VD10':{
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
             
        },

        'settings':{
            'ovd':{
                'of_match': 'regulator-ov-error-microvolt',
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
        },

        #### DEVICE TREE TEST SECTION 
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 26000,
                    'regulator-uv-error-microvolt': 26000,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to set to 26 mV (default)',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to set to 26 mV (default)',
                },
            },

            'ovd_uvd_disable':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 0,
                    'regulator-uv-error-microvolt': 0,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to disable',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to disable',
                },
            },
        },
    }, #VD10 END

    'VOUTL1':{
        'name': 'buck5',
        'of_match':'regulator-voutl1',

        'regulator_en_address':     0x45,
        'regulator_en_bitmask':     0b11111111,


        'volt_reg_address':         0x5C,
        'volt_reg_bitmask':         0b00000111,

        'volt_change_not_allowed_while_on': True,
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
        },

        'settings':{
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
        },

        #### DEVICE TREE TEST SECTION 
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{
            'default':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 34000,
                    'regulator-uv-error-microvolt': 34000,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to set to 34 mV (low clip)',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to set to 34 mV (low clip)',
                },
            },

            'ovd_uvd_disable':{
                'dts_properties':{
                    'regulator-ov-error-microvolt': 0,
                    'regulator-uv-error-microvolt': 0,
                },
                'dts_error_comments':{
                    'regulator-ov-error-microvolt': ' FAILURE: OVD SET failed to disable',
                    'regulator-uv-error-microvolt': ' FAILURE: UVD SET failed to disable',
                },
            },
        },
    }, #VOUTL1 END

    'VOUTS1':{
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

        'settings':{
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
        },

        #### DEVICE TREE TEST SECTION 
        #   'dts' is used to generate device tree source files
        #   'dts_error_comments' is error message if setting failed

        'dts':{

            'default':{
                'dts_properties':{
                    'regulator-oc-protection-microamp': 1350000,
                    'regulator-oc-warn-microamp': 350000,
                },
                'dts_error_comments':{
                    'regulator-oc-error-microamp': ' FAILURE: OCP SET failed to set to 1350 mA (high clip)',
                    'regulator-oc-warn-microamp': ' FAILURE: OCW SET failed to set to 350 mA (low clip)',
                },
            },

            'ovd_uvd_disable':{
                'dts_properties':{
                    'regulator-oc-protection-microamp': 0,
                    'regulator-oc-warn-microamp': 0,
                    },
                'dts_error_comments':{
                    'regulator-oc-error-microamp': ' FAILURE: OCP SET failed to disable',
                    'regulator-oc-warn-microamp': ' FAILURE: OCW SET failed to disable',
                },
            },
        },
    }, #VOUTS1 END

} #regulators END    
} #bd9576 END
