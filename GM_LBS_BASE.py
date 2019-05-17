#!/usr/bin/env python
# -*- coding: cp949 -*-

# Author : HADES 190517 modify
# History
# YW_ML : mold modify for yonwoo
# HA171113 : get data base change / get ble_scanner_new data / update mold_loc_new that tag name check db table 
# HA171117 : Two database / YWIC_MMS -> ble_device / YWIC_MMS_NEW -> ble_scanner, mold_loc
# HA180115 : YWIC_MMS_NEW dB process
# HA190517 : GM update location definer get ble beacon

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
		#f_data1 = d.PATH + 'anybin_yonwoo_env'
                d.list_sql = d.Read_File(f_data1)
                print(d.list_sql)
                d.SQL_OPEN()
                print('*****************************************************************************')
                print('list_sql : ', d.list_sql)
                print('file_list : ', d.file_list)
                print('list_codination : ', d.list_codination)
                print('*****************************************************************************')

                cdate = datetime.datetime.now()
                timegap = datetime.timedelta(minutes=time_delay)
                ddate = cdate - timegap

                sdate = ("%04d-%02d-%02d %02d:%02d:00") % (int(ddate.year), int(ddate.month), int(ddate.day), int(ddate.hour), int(ddate.minute))
                edate = ("%04d-%02d-%02d %02d:%02d:00") % (int(cdate.year), int(cdate.month), int(cdate.day), int(cdate.hour), int(cdate.minute))

                #location definer program get db data
                # Location Definer get Beacon id
                location_definer = []

                df = DataFrame(d.SQL_getGMLD_bledata(sdate, edate), columns = (['name','ldname','rssi']))
                df1 = df.sort_values(by=['name', 'rssi'])
                df2 = df1.drop_duplicates(['name'], keep='last')
                df2 = df2.reset_index(drop=True)
                print(df2)
                num = df2.shape[0]

                for k in range(num) : 
                        try : 
                                #print(df2['name'][k])
                                ble_batterylevel, ble_macaddress = d.getSqlBatteryLevel(df2['name'][k])
                                ld_list = d.getSqlBleScanner(df2['ldname'][k])
                                #print(ble_batterylevel, ld_list)

                                # mold_loc set db
                                data = []
                                data.append(df2['name'][k])     # mold_blackbin_name
                                data.append(ble_macaddress)     # modl_blackbin_mac
                                data.append('0')                # mold_locX
                                data.append('0')                # mold_locY
                                data.append('0')                # mold_locZ
                                data.append('GM')               # mold_productco  
                                data.append('GM')               # mold_orglocation
                                data.append(ld_list[5])         # mold_managelocation
                                data.append(ble_batterylevel)   # mold_batterylevel
                                data.append('1')                # mold_flag
                                if(int(ble_batterylevel) < 40) : 
                                        data.append('lowbat')
                                else  :
                                        data.append('moldlot')             # mold_event
                                data.append(str(datetime.datetime.now()))   #mold_loc_datetime

                                print("==========================================================")
                                print(data)
                                d.SQL_UpdateMoldLocNew(data)    # mold_loc data update       
                                pdb.set_trace()

                        except : 
                                print('LD sql data Error!')

        except :
                print('LD_Code Error')
#====================================================================================

# main Function ------------------------------------------------------------------------------------
def main() :
        try :
                print("==========================================================")
                print(" [ LBS Engine ] Ver 3.0 - BLE Scanner ")
                print("==========================================================")
                loop_delay_time = 30 # 5 minute data gather
                while(1) :
		#if(1):
                        print('***************** 10 min delay **********************')
                        GM_LD_Code(loop_delay_time)
                        time.sleep(60*(28))


        except :
                print("!!!!!!!!!!!!!!!LBS Engine Error!!!!!!!!!!!!!")
#======================================
if __name__ == '__main__' :
        try :
                main()
        except KeyboardInterrupt :
                print("LBS Engine END")

