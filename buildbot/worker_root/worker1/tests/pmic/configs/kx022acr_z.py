data={
'name':'kx022acr-z',
'i2c':{
    'bus':      2,
    'address':  0x1F,
    },

'iio_device':{
    'name':     'kx022-accel',
},

'settings':{
    'gsel':{
        'reg_address':  0x18,
        'reg_bitmask':  0b00011000,
        'list_g_ranges':[2, 4, 8, 16],
        'list_values':  [0.000598550, 0.001197101, 0.002394202, 0.004788403],
    },

    'sampling_frequency':{
        'reg_address':  0x1B,
        'reg_bitmask':  0b00001111,
        ### Driver supports these sampling rates, values are in Hz
        'list_values': [0.78, 1.563, 3.125, 6.25, 12.5, 25.0, 50.0, 100.0, 200.0]
    },
    'axis':{
        'reg_bits':         16,
        'regs':{
            'x':{
                'low_reg':  0x06,
                'high_reg': 0x07,
            },
            'y':{
                'low_reg':  0x08,
                'high_reg': 0x09,
            },
            'z':{
                'low_reg':  0xA,
                'high_reg': 0xB,
            },
        },
    }
}

} #kx022acr-z end
