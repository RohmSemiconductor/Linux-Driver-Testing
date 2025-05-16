data={
'name':     'bd79703',
'type':     'DAC',
'adc':      'BeagleBone Black DAC',
'driver':   'rohm-bd79703.c',

'iio_device':{
    'name':     'bd79703',
#    'adc':      'TI-am335x-adc.2.auto',
    'adc':     'bd79124',
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
        0:0,
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        }
    }
}
