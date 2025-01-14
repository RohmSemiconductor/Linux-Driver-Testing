data={
'name':'kx134-1211',
'i2c':{
    'bus':      2,
    'address':  0x1F,
    },

'iio_device':{
    'name':     'kx134-1211',
},

'settings':{
    'gsel':{
        'reg_address':  0x1B,
        'reg_bitmask':  0b00011000,
        'list_g_ranges':[8, 16, 32, 64],
        'list_values':  [0.002394202, 0.004788403, 0.009576807, 0.019153613],
    },

    'sampling_frequency':{
        'reg_address':  0x21,
        'reg_bitmask':  0b00001111,
        ### Driver supports these sampling rates, values are in Hz
        'list_values': [0.78, 1.563, 3.125, 6.25, 12.5, 25.0, 50.0, 100.0, 200] #skip 200.0 for now
    },
    'axis':{
        'reg_bits':         16,
        'regs':{
            'x':{
                'low_reg':  0x08,
                'high_reg': 0x09,
            },
            'y':{
                'low_reg':  0x0A,
                'high_reg': 0x0B,
            },
            'z':{
                'low_reg':  0xC,
                'high_reg': 0xD,
            },
        },
    }
}

} #kx022acr-z end
