data={
'name':'bd79703',
'adc': 'BeagleBone Black DAC',
'driver': 'rohm-bd79703.c',

'iio_device':{
    'name':     'bd79703',
#    'adc':      'TI-am335x-adc.2.auto',
    'adc':     'bd79124',
    },

'info':{
    'bits':8,

    ### Channels are mapped in this manner
    ### DAC channel : ADC channel
    'channels':{
        0:0,
        1:1,
        2:2,
    }
    }
}
