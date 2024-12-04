import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx022acr_z
from test_util import check_result
from sensor_class import sensor
kx022acr_z = sensor(kx022acr_z)

from time import sleep


### Only Z-axis is tested in this test. It is the only axis which' value can be relied to be
### fairly close to earths gravitational acceleration.
def test_gscale_ms2(command):
    result = kx022acr_z.test_gscale(command, 'z', 'raw_scale', tolerance=0)
#    result = kx022acr_z.test_gscale(command, 'y', 'raw_scale', append_results=True, tolerance=0)
#    result = kx022acr_z.test_gscale(command, 'x', 'raw_scale', append_results=True, tolerance=0)

    print("driver_read_raw: "+str(result['return']))
    print("last divided: "+str(result['expect_perfect']))
    print("low_limit: "+str(result['expect_low']))
    print("high_limit: "+str(result['expect_high']))
    print("return_diff: "+str(result['return_diff']))

    check_result(result)

#    for item in result.items():
#        print(item)
#        print(len(item[1]))
#
#    test_fail = 1
#    assert test_fail == 0
#    x = 0
#    result  = kx022acr_z.init_test_gscale(command,'ms2', 'z')
#    bits = kx022acr_z.board.data['settings']['axis']['reg_bits']
#    for value in kx022acr_z.board.data['settings']['gsel']['list_values']:
#        result['gscale'].append(kx022acr_z.board.data['settings']['gsel']['list_g_ranges'][x])
#        result['gscale_multiplier'].append(kx022acr_z.board.data['settings']['gsel']['list_values'][x])
#        kx022acr_z.write_in_accel_scale(value, command)
##        result['raw'] = kx022acr_z.driver_read_raw_xyz(command, 'z')
##        if result['last_raw'] != None:
##            print("jeejee")
#        result['driver_signed'].append(kx022acr_z.get_signed_value(kx022acr_z.driver_read_raw_xyz(command, 'z'), bits))
#        result['register_signed'].append(kx022acr_z.get_signed_value(kx022acr_z.reg_read_raw_xyz(command, 'z'), bits))
#
#
#        print(driver_signed)
#        print(register_signed)
#        x = x + 1
        #  NONIIN JÄRJESTYS ON OIKEA, OTA TUOSTA
        # TUO REKISTERISTÄ LUETTU ARVO JA VERTAA SITÄ
        # KÄYTÄ VAIKKA SITÄ KAHEN KOMPLEMENTTIA
        #
        # VERTAA read reg raw ja z_raw driver
        # VERTAA m/s² molemmista laskettuna myös, ja vaikka tuota
        # iio generic bufferia myös
        # m/s² myös rekisteristä luettuun

        # Eli: Tekaseppa semmonen test_match funktio mikä palauttaa
        # sallitun arvoalueen jne..

#        print("read reg raw:")
#        z_reg_raw = kx022acr_z.reg_read_raw_xyz(command, 'z')
#        print(z_reg_raw)
#        print(z_reg_raw * value)
#
#        z_raw = kx022acr_z.driver_read_raw_xyz(command, 'z')
#        print("z_raw driver:")
#        print(z_raw)
#        print(int(z_raw)* value)
#
#        print("iio_generic_buf m/s2:")
#        iio_ms2 = kx022acr_z.driver_read_ms2_xyz(command, 'z')
#        print(iio_ms2)
#        print("\n")

        #Check that raw value is scaling
        #Check that m/s² is around the same
        #Read raw in values here an
#    print(result)
#    check_result(result)
