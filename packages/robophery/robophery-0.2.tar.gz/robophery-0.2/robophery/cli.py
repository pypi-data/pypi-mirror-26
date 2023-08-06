#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from oslo_config import cfg
from robophery.base import ModuleManager
from robophery.conf import *

GPIO_OPTS = [
    cfg.Opt('data_pin',
            short='p',
            default=None,
            help='Module GPIO pin'),
]


BLE_OPTS = [
    cfg.Opt('addr',
            short='a',
            default=None,
            help='Module MAC address'),
]


def _config(module_conf, opts=None):
    conf = {
        'log_level': 'debug',
        'log_handlers': ['console', ],
        'read_interval': 2500,
        'platform': 'raspberrypi',
        'config': RPI_PLATFORM
    }
    conf['config']['comm'] = {}
    conf['config']['module'] = {
        'module': module_conf,
    }
    if opts is not None:
        CONF = cfg.CONF
        CONF.register_cli_opts(opts)
        CONF(sys.argv[1:])
        conf['config']['module']['module'].update(CONF)
    return conf

# Manager service


def manager_service():
    sys.path.append("/etc/robophery")
    from robophery_conf import CONF
    manager = ModuleManager(**CONF)
    manager.run()

# I2C modules


def module_am2320():
    config = _config(AM2320_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_bme280():
    config = _config(BME280_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_bmp085():
    config = _config(BMP085_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_bh1750():
    config = _config(BH1750_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_ezoec():
    config = _config(EZOEC_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_ezoph():
    config = _config(EZOPH_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_htu21d():
    config = _config(HTU21D_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_ina219():
    config = _config(INA219_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_mcp9808():
    config = _config(MCP9808_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_mpu6050():
    config = _config(MPU6050_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_si7021():
    config = _config(SI7021_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_sht3x():
    config = _config(SHT3X_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_ssd1306():
    config = _config(SSD1306_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_tcs34725():
    config = _config(TCS34725_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def module_tsl2561():
    config = _config(TSL2561_MODULE)
    manager = ModuleManager(**config)
    manager.run()


TSL2591_OPTS = [
    cfg.Opt('gain',
            short='g',
            default=0x00,
            help='Gain'),
    cfg.Opt('integration',
            short='i',
            default=0x00,
            help='Integration time'),
]


def module_tsl2591():
    config = _config(TSL2591_MODULE, TSL2591_OPTS)
    manager = ModuleManager(**config)
    manager.run()


def module_vl53l0x():
    config = _config(VL53L0X_MODULE)
    manager = ModuleManager(**config)
    manager.run()

# GPIO modules


def module_dht11():
    config = _config(DHT11_MODULE, GPIO_OPTS)
    if config['config']['module']['module']['data_pin'] is None:
        raise ValueError("Data pin must be set.")
    manager = ModuleManager(**config)
    manager.run()


def module_dht22():
    config = _config(DHT22_MODULE, GPIO_OPTS)
    if config['config']['module']['module']['data_pin'] is None:
        raise ValueError("Data pin must be set.")
    manager = ModuleManager(**config)
    manager.run()


def module_hcsr04():
    OPTS = [
        cfg.Opt('trigger_pin',
                short='t',
                help='Trigger pin'),
        cfg.Opt('echo_pin',
                short='e',
                help='Echo pin'),
    ]
    config = _config(HCSR04_MODULE, OPTS)
    if config['config']['module']['module']['trigger_pin'] is None:
        raise ValueError("Trigger pin must be set.")
    if config['config']['module']['module']['echo_pin'] is None:
        raise ValueError("Echo pin must be set.")
    manager = ModuleManager(**config)
    manager.run()


def module_l293d():
    OPTS = [
        cfg.Opt('power_pin',
                short='a',
                help='L293D pin 1 or pin 9: On or off'),
        cfg.Opt('forward_pin',
                short='b',
                help='L293D pin 2 or pin 10: Anticlockwise positive'),
        cfg.Opt('backward_pin',
                short='c',
                help='L293D pin 7 or pin 15: Clockwise positive'),
    ]
    config = _config(L293D_MODULE, OPTS)
    if config['config']['module']['module']['power_pin'] is None:
        raise ValueError("Power pin must be set.")
    if config['config']['module']['module']['forward_pin'] is None:
        raise ValueError("Forward pin must be set.")
    if config['config']['module']['module']['backward_pin'] is None:
        raise ValueError("Backward pin must be set.")
    manager = ModuleManager(**config)
    manager.run()


def module_hd44780_pcf():
    config = _config(HD44780_PFC_MODULE, GPIO_OPTS)
    manager = ModuleManager(**config)
    manager.run()


def module_relay():
    config = _config(RELAY_MODULE, GPIO_OPTS)
    if config['config']['module']['module']['data_pin'] is None:
        raise ValueError("Data pin must be set.")
    manager = ModuleManager(**config)
    manager.run()


def module_switch():
    config = _config(SWITCH_MODULE, GPIO_OPTS)
    if config['config']['module']['module']['data_pin'] is None:
        raise ValueError("Data pin must be set.")
    manager = ModuleManager(**config)
    manager.run()

# PWM modules


def module_servo():
    OPTS = [
        cfg.Opt('data_pin',
                short='p',
                default=None,
                help='Module GPIO pin'),
        cfg.Opt('angle',
                short='a',
                default=90)
    ]
    config = _config(SERVO_MODULE, OPTS)
    manager = ModuleManager(**config)
    manager.run()


# BLE modules


def module_pfp():
    config = _config(PFP_MODULE, BLE_OPTS)
    if config['config']['module']['module']['addr'] is None:
        raise ValueError("MAC address must be set.")
    manager = ModuleManager(**config)
    manager.run()

# 1-wire modules


def module_ds18():
    OPTS = [
        cfg.Opt('type',
                short='t',
                default="ds18b20",
                help='Specific type of Dallas DS18 family midule.'),
        cfg.Opt('addr',
                short='a',
                default='0',
                help='Specific module address at 1-wire bus.')
    ]
    config = _config(DS18_MODULE, OPTS)
    manager = ModuleManager(**config)
    manager.run()
