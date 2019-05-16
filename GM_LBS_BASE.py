#!/usr/bin/env python
# -*- coding: cp949 -*-

# Author : HADES 171113 modify
# History
# YW_ML : mold modify for yonwoo
# HA171113 : get data base change / get ble_scanner_new data / update mold_loc_new that tag name check db table 
# HA171117 : Two database / YWIC_MMS -> ble_device / YWIC_MMS_NEW -> ble_scanner, mold_loc
# HA180115 : YWIC_MMS_NEW dB process

from LBS_BASE import *

#from pandas import Series, DataFrame
#import pandas as pd

#====================================================================================
# Location Definer Function
#------------------------------------------------------------------------------------

def GM_LD_Code(time_delay) :
        try :
                d = BASEClass()
		print("GM_Calc_Distance Start")

		f_data1 = d.PATH + 'anybin_gm_env'
		#f_data2 = d.PATH + 'yw_ml_lbs_env'
                d.list_sql = d.Read_File(f_data1)
                #d.list_lbs = d.LBSENV_Read_File(f_data2)
                print(d.list_sql)
                #print(d.list_lbs)
                d.SQL_OPEN()
                print('*****************************************************************************')
                print('list_sql : ', d.list_sql)
                #print('list_lbs : ', d.list_lbs)
                print('file_list : ', d.file_list)
                print('list_codination : ', d.list_codination)
                print('*****************************************************************************')

		#del d.list_ld[:]	#HA171113 Location Definer List Clear

                #num = int(d.list_lbs[5]) # location definer number
                #print('LD_num = ', num)
                cdate = datetime.datetime.now()
                timegap = datetime.timedelta(minutes=time_delay)
                ddate = cdate - timegap

                sdate = ("%04d-%02d-%02d %02d:%02d:00") % (int(ddate.year), int(ddate.month), int(ddate.day), int(ddate.hour), int(ddate.minute))
                edate = ("%04d-%02d-%02d %02d:%02d:00") % (int(cdate.year), int(cdate.month), int(cdate.day), int(cdate.hour), int(cdate.minute))
                #location definer program get db data
                # Location Definer get Beacon id
                location_definer = []

#		df = YW_ML_LD_MAT(60)
#================================================================
		LD_MAT = []	#HA180130 imsi


                a = []
                tt = d.SQL_getGMLD_bledata(sdate, edate)
                print(tt)


                ''' 
		for k in range(num) : 
                        try :
				a = []
                                tt = d.getLDSqlBleDevice('Anybi:n0%', d.list_lbs[6+k], sdate, edate)
                                a.append(tt)

				LD_MAT.append(a)	#HA180130 imsi

			except : 

				print('LD_MAT Error')

                '''           


        except :
                print('LD_Code Error')
#====================================================================================

# main Function ------------------------------------------------------------------------------------
def main() :
        try :
                print("==========================================================")
                print(" [ LBS Engine ] Ver 3.0 - BLE Scanner ")
                print("==========================================================")
                loop_delay_time = 60 # 5 minute data gather
                #while(1) :
		if(1):
                        print('***************** 10 min delay **********************')
                        GM_LD_Code(loop_delay_time)


        except :
                print("!!!!!!!!!!!!!!!LBS Engine Error!!!!!!!!!!!!!")
#======================================
if __name__ == '__main__' :
        try :
                main()
        except KeyboardInterrupt :
                print("LBS Engine END")

