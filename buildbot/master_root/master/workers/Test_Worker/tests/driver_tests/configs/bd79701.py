data={
'name':     'bd79701',
'type':     'DAC',
'adc':      'BeagleBone Black DAC',
'driver':   'rohm-bd79703.c',

'iio_device':{
    'name':     'bd79701',
#    'adc':      'TI-am335x-adc.2.auto',
    'adc':     'bd79104',
    },

'info':{
    'bits':8,

    ### Channels are mapped in this manner
    ### DAC channel : ADC channel
    ###
    ### This Dictionary is used to write,
    ### and then read corresponding ADC
    ### channel

    'channels':{
        0:2,
        1:3,
        2:4,
        }
    }
}
