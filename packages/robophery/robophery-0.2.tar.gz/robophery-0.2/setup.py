# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme:
    long_description = ''.join(readme.readlines())

setup(
    name='robophery',
    version='0.2',
    description='Python library for interfacing low level hardware sensors and actuators with MQTT bindings.',
    long_description=long_description,
    author='Aleš Komárek',
    author_email='ales.komarek@newt.cz',
    license='Apache Software License',
    url='http://www.github.cz/cznewt/robophery',
    packages=find_packages(exclude=['.txt']),
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'rp_manager = robophery.cli:manager_service',
            'rp_ft232h_discovery = robophery.utils.ft232h:discover_devices',
            'rp_am2320 = robophery.cli:module_am2320',
            'rp_bh1750 = robophery.cli:module_bh1750',
            'rp_bme280 = robophery.cli:module_bme280',
            'rp_bmp085 = robophery.cli:module_bmp085',
            'rp_dht11 = robophery.cli:module_dht11',
            'rp_dht22 = robophery.cli:module_dht22',
            'rp_ds18 = robophery.cli:module_ds18',
            'rp_ezoec = robophery.cli:module_ezoec',
            'rp_ezoph = robophery.cli:module_ezoph',
            'rp_htu21d = robophery.cli:module_htu21d',
            'rp_hcsr04 = robophery.cli:module_hcsr04',
            'rp_ina219 = robophery.cli:module_ina219',
            'rp_hd44780_pcf = robophery.cli:module_hd44780_pcf',
            'rp_l293d = robophery.cli:module_l293d',
            'rp_mcp9808 = robophery.cli:module_mcp9808',
            'rp_mpu6050 = robophery.cli:module_mpu6050',
            'rp_pfp = robophery.cli:module_pfp',
            'rp_relay = robophery.cli:module_relay',
            'rp_si7021 = robophery.cli:module_si7021',
            'rp_servo = robophery.cli:module_servo',
            'rp_sht3x = robophery.cli:module_sht3x',
            'rp_ssd1306 = robophery.cli:module_ssd1306',
            'rp_switch = robophery.cli:module_switch',
            'rp_tcs34725 = robophery.cli:module_tcs34725',
            'rp_tsl2561 = robophery.cli:module_tsl2561',
            'rp_tsl2591 = robophery.cli:module_tsl2591',
            'rp_vl53l0x = robophery.cli:module_vl53l0x',
        ],
    },
)
