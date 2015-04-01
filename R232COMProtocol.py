#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015 Demo User <debian@beaglebone>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""Voltronic Power RS232 communication protocol"""
from __future__ import absolute_import

def _(msg) : return msg
forecast_text = {
#Set configuration to the Device
		#SETTING_FEED_IN_ENABLE 
		"ENFC1\r": _("4"),
		#SETTING_FEED_IN_DISABLE
		"ENFC0\r": _("4"),
		#PV_SUPPLY_PRIORITY_BLG
		"PRIO01\r": _("4"),
		#PV_SUPPLY_PRIORITY_LBG
		"PRIO02\r": _("4"),
		#PV_SUPPLY_PRIORITY_LGB
		"PRIO03\r": _("4"),
		#SET_FLOATING_CHARGING_VOLTAGE" 
		"MCHGV\r": _("4"),
		#SET_BULK_CHARGING_VOLTAGE" 
		"BCHGV\r": _("4"),
		#SET_REDISCHARGING_VOLTAGE" 
		"DSUBV\r": _("4"),
		#SET_CUT_OFF_VOLTAGE" 
		"BSDV\r": _("4"),
		#SET_MODE_OFF_GRID" 
		"DMODEL150\r": _("4"),
		#SET_MODE_ON_GRID" 
		"DMODEL100\r": _("4"),
		#SET_DEVICE_MODE" 
		"DMODEL\r": _("4"),
		#GO_TO_STANDBY" 
		"GTS1\r": _("4"),
		#RETURN_FROM_STANDBY" 
		"GTS0\r": _("4"),
		#UNLOCK_MCU" 
		"OEEPB\r": _("4"),
		#SET_ENABLE_DISABLE" 
		"ENF\r": _("4"),
		#SET_AC_CHARGING_TIME" 
		"PKT\r": _("4"),
		#SET_SYS_TIME" 
		"DAT\r": _("4"),
		#Envoyer le courant de charge Max
		#SET_CHARGING_CURRENT
		"MCHGC\r": _("4"),
		#SET_LCD" 
		"LST\r": _("4"),
		#SET_MIN_FREQUENCE" 
		"GOLF\r": _("4"),
		#SET_MAX_FREQUENCE" 
		"GOHF\r": _("4"),
		#SET_MIN_VOLTAGE" 
		"GOLV\r": _("4"),
		#SET_NOMINAL_VOLTAGE" 
		"V\r": _("4"),
		#SET_MAX_VOLTAGE" 
		"GOHV\r": _("4"),
		#SET_NOMINAL_FREQUENCE" 
		"F\r": _("4"),
		#SET_ALLOW_GENERATOR" 
		"GNTM1\r": _("4"),
		#SET_BATTERIE" 
		"LBF\r": _("4"),
		#SET_LITHIUM" 
		"BSDP\r": _("4"),
		#TURN_ON_OUTPUT" 
		"SON\r": _("4"),
	    #TURN_OFF_OUTPUT" 
		"SOFF\r": _("4"),
	    #SET_ACOUTPUT_TIME" 
		"LDT\r": _("4"),
		
#Get configuration from the Device		
		#GET_CHARGE_STATUS" 
		"QCHGS\r": _("17"),
		#GET_CUTOFF_DISCHARGE_VOL" 
		"QBSDV\r": _("17"),
		#GET_DEVICE_MODE" 
		"QDM\r": _("4"),
		#GET_AC_CHARGING_TIME" 
		"QPKT\r": _("9"),
		#GET_SYS_TIME" 
		"QT\r": _("15"),
		#Get vente status for verification
		#GET_ENABLE_DISABLE_STATUS
		"QENF\r": _("21"),
		#Recuperer le courant de charge 
		#String GET_CHARGING_CURRENT
		"QPIGS\r": _("133"),
		#GET_LCD" 
		"QLST\r": _("3"),
		#GET_FREQUENCE" 
		"QGOF\r": _("9"),
		#GET_VOLTAGE" 
		"QGOV\r": _("11"),
		#GET_NOMINAL" 
		"QPIRI\r": _("38"),
		#GET_ALLOW_GENERATOR" 
		"OFFC00.2 53.0 060\r": _("3"),
		#GET_BATTERIE" 
		"QEBGP\r": _("6"),
		#GET_LITHIUM" 
		"QBSDP\r": _("3"),
		#GET_ID" 
		"QID\r": _("15"),
		#GET_TEMPERATURE" 
		"QTPR\r":_("13"),
		#GET_ERROR" 
		"QPIWS\r": _("128"),
		#GET_ENERGY_HEURE" 
		"QEH\r": _("6"),
		#GET_ENERGY_DAY" 
		"QED\r": _("7"),
		#GET_ENERGY_MONTH" 
		"QEM\r": _("8"),
		#GET_ENERGY_YEAR" 
		"QEY\r": _("9"),
	    #GET_ACOUTPUT_TIME" 
		"QLDT\r": _("9")
		}
		
del _

def lisProt(protocol):
    return forecast_text[protocol]

