#!/usr/bin/env python
# -*- coding: cp949 -*-

# Author : HADES 171113 modify
# History
# YW_CL : mold 2 part for yonwoo
# HA171113 : get data base change / get ble_scanner_new data / update mold_loc_new that tag name check db table 
# HA171117 : Two database / YWIC_MMS -> ble_device / YWIC_MMS_NEW -> ble_scanner, mold_loc
# HA180115 : YWIC_MMS_NEW dB process - LBS_BASE.py

import os
import time, threading
import datetime
import MySQLdb
import pymssql
import math
import CircleIntersection
import random
import pdb

from subprocess import *

from pandas import Series, DataFrame
import pandas as pd
#====================================================================================
# LBS Engin Base Class declare
#------------------------------------------------------------------------------------
class BASEClass :

        file_list = []
        list_sql = []
        list_lbs = []
        list_codination = []
	list_ld = []
	LD_MAT = []

        db = ' '
        curs = ' '
	
        gServerIP = ' '
        gLoginID = ' '
        gPassword = ' '
        gDBNAME = ' '

	gtable_name = ' '

	PATH = '/home/pi/Anybin/GM/'
	#PATH = '/home/solubiz/study/anybin_src/YW_NEW/'

        def __init__(self) :
                print('======= LBS Engine Initial ======')
		self.gtable_name = ("ble_device_" + str(datetime.date.today()).split()[0].replace('-', ''))

        def set(self, v) :
                self.value = v

        def get(self) :
                self.file_list = self.value
                #print self.value
                return self.value

        #====================================================================================
        # file read Function
        #------------------------------------------------------------------------------------
        def Read_File(self, fdata) :

                anybin_data = []

                parsor_t = ['serverIP:', 'loginID:','password','dbname', 'ipaddress:', 'scannerid:', 'constrain:', 'productco:', 'lcation:', 'locx:', 'locy:', 'locz:']

                try :

                        f = open(fdata, 'rb')

                        k = 0
                        for i in parsor_t :
                                line = f.readline()
                                l = line.split()

                                if(i == parsor_t[k]) :
                                        mat = l[1]
                                        anybin_data.append(mat)
                                        k = k+1

                        return anybin_data

                except IndexError as e:
                        print(e)
                finally :
                        f.close()

        #====================================================================================
        # file lbs_env Function
        #------------------------------------------------------------------------------------
        def LBSENV_Read_File(self, fdata) :

		anybin_data = []

		pp = ['S_NUM', 'LD_NUM']

		try :

		        f = open(fdata, 'rb')

		        k = 0
		        s_num = 0
		        l_num = 0
		        for i in range(100) :
		                line = f.readline()
				line = line.replace("\n", "")
		                l = line.split(': ')
			
				if(l[0] == pp[0]) : 				
					s_num = l[1]

				if(l[0] == pp[1]) : 
					l_num = l[1]

				anybin_data.append(l[1])

				k = k+1
		                print(k, l, s_num, l_num)

			print(anybin_data)
		        return anybin_data

		except IndexError as e:
		        print(e)
			print(anybin_data)
		        return anybin_data
		finally :
		        f.close()


        #====================================================================================
        # SQL_MSSQL_OPEN Function
        #------------------------------------------------------------------------------------
        def SQL_MSSQL_OPEN(self) :

		ret = 0

		for i in range(1) : 

			try : 
			        self.db = pymssql.connect(host = self.gServerIP, user = self.gLoginID, password = self.gPassword, database = self.gDBNAME)
			        #print('sql ---2 ')
			        self.curs = self.db.cursor()
			        #print('sql ---3 ')
				ret = 0;
				print(self.db, self.curs)
				return (ret)
				break;

			except pymssql.DatabaseError, e : 
				print('SQL_MSSQL_OPEN Error : ',i, e)
				ret = -1	
				#self.gServerIP = '222.100.204.221'       # Server IP
				time.sleep(0.2)

			except : 
				print "Another Exception occured, most likely User or signon incorrect"
				time.sleep(0.2)

        #====================================================================================
        # SQL_OPEN Function
        #------------------------------------------------------------------------------------
        def SQL_OPEN(self) :

                self.gServerIP = self.list_sql[0]       # Server IP
                self.gLoginID = self.list_sql[1]        # ID
                self.gPassword = self.list_sql[2]       # Password
                self.gDBNAME = self.list_sql[3]         # DB Name
                print(self.gServerIP, self.gLoginID, self.gPassword, self.gDBNAME)

                # SQL Open
                ret = self.SQL_MSSQL_OPEN()
                print(self.db)
		return (ret)

        #====================================================================================
        # SQL_DELETE Function
        #------------------------------------------------------------------------------------
	def SQL_DELETE(self) : 
		print("dB Close!")
		self.curs.close()
		self.db.close()

        #====================================================================================
        # getSqlBatteryLevel Function
        #------------------------------------------------------------------------------------
        def getSqlBatteryLevel(self, MoldID) :
                ret = []

                query = "select top 1 blackbin_batterylevel from " + self.gtable_name + " where (blackbin_name = %s) order by blackbin_index DESC"
                #print(query)
                self.curs.execute(query, (MoldID))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        print(r)
		a = int(r[0], 16)
		print(a)
                return(str(a))

        #====================================================================================
        # getSqlBleScanner Function
        #------------------------------------------------------------------------------------
        def getSqlBleScanner(self, ID) :
                #print(self.list_lbs[1])
                query = "select * from ble_scanner where bs_name = %s"
                #query = "select * from ble_scanner_new where bs_name = %s"
                
		self.curs.execute(query, ID)
                for r in self.curs.fetchall() :
                        print(r)
                #a = r[0]

                return(r)

        #====================================================================================
        # getSqlBleDevice Function
        #------------------------------------------------------------------------------------
        def getSqlBleDevice(self, ScannerID, sDate, eDate) :

                ret = []

                query = "select blackbin_name, AVG(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where blackbin_bs_name = %s and blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s group by blackbin_name order by blackbin_name ASC"
                self.curs.execute(query, (ScannerID, sDate, eDate))

                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)
                return(ret)

        #====================================================================================
        # getSqlBleDevice_MAX Function
        #------------------------------------------------------------------------------------
        def getSqlBleDevice_MAX(self, ScannerID, sDate, eDate) :
                ret = []

                query = "select blackbin_name, MAX(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where blackbin_bs_name = %s and blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s group by blackbin_name order by blackbin_name ASC"


                self.curs.execute(query, (ScannerID, sDate, eDate))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)
                return(ret)

        #====================================================================================
        # getSqlBleDevice_MIN Function
        #------------------------------------------------------------------------------------
        def getSqlBleDevice_MIN(self, ScannerID, sDate, eDate) :

                ret = []

                query = "select blackbin_name, MIN(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where blackbin_bs_name = %s and blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s group by blackbin_name order by blackbin_name ASC"
                self.curs.execute(query, (ScannerID, sDate, eDate))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)
                return(ret)

        #====================================================================================
        # getTotal_SqlBleDevice Function
        #------------------------------------------------------------------------------------
        def getTotal_SqlBleDevice(self, ScannerID, sDate, eDate) :

                ret = []

                query = "select blackbin_name from " + self.gtable_name + " where (blackbin_bs_name = %s or blackbin_bs_name = %s or blackbin_bs_name = %s or blackbin_bs_name = %s) and blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s group by blackbin_name order by blackbin_name ASC"

                self.curs.execute(query, (ScannerID[0],ScannerID[1],ScannerID[2],ScannerID[3], sDate, eDate))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)


                return(ret)

        #====================================================================================
        # getLDSqlBleDevice Function
        #------------------------------------------------------------------------------------
        def getLDSqlBleDevice(self, ScannerID, LDID, sDate, eDate) :
                ret = []
		try : 

		        #query = "select blackbin_name, blackbin_macaddress, count(blackbin_macaddress) as CNT from " + self.gtable_name + " where (blackbin_bs_name = %s and blackbin_name = %s) and (blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s) group by blackbin_name, blackbin_macaddress order by CNT ASC"
			query = "select blackbin_name, blackbin_macaddress, count(blackbin_macaddress) as CNT from " + self.gtable_name + " where (blackbin_bs_name like %s and blackbin_name like %s) and (blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s) group by blackbin_name, blackbin_macaddress order by CNT DESC"

			#print(query, (self.gtable_name, ScannerID, LDID, sDate, eDate))
			self.curs.execute(query, (ScannerID, LDID, sDate, eDate))
		        for r in self.curs.fetchall() :
		                ret.append(r)
		                print(r)

		        return(ret)

		except pymssql.DatabaseError, e : 
			print('getLDSqlBleDevice Error : ', e)
			ret = -1	
			time.sleep(0.2)

		except : 
			print "Another Exception occured, most likely User or signon incorrect"
			time.sleep(0.2)

        #====================================================================================
        # SQL_getGMLD_bledata Function for GM with gunsolution
        #------------------------------------------------------------------------------------
        def SQL_getGMLD_bledata(self, sDate, eDate) :

                try : 
                        ret = []

                        query = "select top 10 * from " + self.gtable_name + " where (blackbin_name like 'LD%') and ( len(blackbin_macaddress) > 5 ) and ( len(blackbin_macaddress) < 8 ) and ( blackbin_macaddress >= '0'  and blackbin_macaddress <= 'z') and (blackbin_receivedatetime > %s ) and (blackbin_receivedatetime < %s )order by blackbin_name, blackbin_index asc;"


                        self.curs.execute(query, (sDate, eDate))
                        for r in self.curs.fetchall() :
                                ret.append(r)
                                print(r)
                        return(ret)
                except :
                        print('SQL_getGMLD_bledata Error')


        #====================================================================================
        # SQL_InsertMoldLoc Function
        #------------------------------------------------------------------------------------
        def SQL_InsertMoldLoc(self, data) :
                #global gSCANNER_ID, gBLENAME, gBLEMAC, gBLERSSI, gBatteryLevel, gBLETime, gTemperature, gTXPower

                #print('************************************SQL_InsertBLE()******************************')

                #print(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

                query = "INSERT INTO mold_loc (mold_blackbin_name, mold_locX, mold_locY, mold_locZ, mold_productco, mold_managelocation, mold_event, mold_loc_datetime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"

                #print(query)

                self.curs.execute(query, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))

                #for r in self.curs.fetchall() :
                #        print(r)

                self.db.commit()

        #====================================================================================
        # getSqlMoldLoc Function
        #------------------------------------------------------------------------------------
        def getSqlMoldLoc(self, ID) :
                #print(self.list_lbs[1])
                query = "select * from mold_loc where mold_blackbin_name = %s"
                self.curs.execute(query, ID)
                for r in self.curs.fetchall() :
                        print(r)
                #a = r[0]
                return(r)

        #====================================================================================
        # SQL_UpdateMoldLocNew Function
        #------------------------------------------------------------------------------------
        def SQL_UpdateMoldLocNew(self, data) :

		try : 

			ret = self.getSqlMoldLoc(data[0])	#if equal YW_MS, break;

			if(data[5] == 'YW_MS' or data[5] == 'YW_MSH') : 
				if(ret[7] == 'YW_DT') :
					return

			if(data[5] == 'YW_DT' or data[5] == 'YW_DTH') : 
				if(ret[7] == 'YW_MS') :
					return
			

			batteryLevel = self.getSqlBatteryLevel(data[0])		#battery level Check

			aa = int(batteryLevel)
			print("Battery Level : %d" % aa)

			if(aa <= 40) : 
				data[6] = 'lowbat'
				print(data[6])

			mold_flag = '1'

		        print('************************************SQL_InsertBLE()******************************')

		        print(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

		        query = "UPDATE mold_loc SET mold_locX=%s, mold_locY=%s, mold_locZ=%s, mold_productco=%s, mold_managelocation=%s, mold_event=%s, mold_loc_datetime=%s, mold_batterylevel=%s, mold_flag=%s WHERE mold_blackbin_name=%s"

			#print(query)
			self.curs.execute(query, (data[1], data[2], data[3], data[4], data[5], data[6], data[7], batteryLevel, mold_flag, data[0]))

		        #for r in self.curs.fetchall() :
		        #        print(r)

		        self.db.commit()

		except pymssql.DatabaseError, e : 
			print('SQL_MSSQL_OPEN Error : ',i, e)

			self.SQL_MSSQL_OPEN()		#HA171113 New Add

		except : 
			print "Another Exception occured, SQL_UpdateMoldLocNew ERROR !!!"


        #====================================================================================
        # SQL_getCountMoldLocNew Function
        #------------------------------------------------------------------------------------

	def SQL_getCountMoldLocNew(self, data) :
		try :

			ret = 0
			ret = self.SQL_getCountMoldLocNew(data)
			print ret
			if(ret == 1) : 
				print data[0]
				query = "SELECT COUNT(mold_blackbin_name) from mold_loc where mold_blackbin_name = '%s'" % data[0]

				print query

				try : 
					self.curs.execute(query)

				except pymssql.Error, e:
					try : 
						print "pymssql Error [%d]: %s" % (e.args[0], e.args[1])			
					except IndexError:
						print "pymssql Error: %s" % str(e)				
		
				for r in self.curs.fetchall() : 
					print('SQL_getCountMoldLocNew', r)
				a = r[0]
				print(r, a)
				return(int(a))

			else : 
				print('SQL_getCountMoldLocNew No Data')

		except :			
			print('SQL_getCountMoldLocNew Error :: Unknown table')

        #====================================================================================
        # SQL_getMoldLocNewIndex Function
        #------------------------------------------------------------------------------------
	def SQL_getMoldLocNewIndex(self, data) : 
		try : 
			query = "select mold_loc_Index from mold_loc where mold_blackbin_name = %s"
			self.curs.execute(query, (data[0]))


			print query

			for r in self.curs.fetchall() :
				print(r)
			a = r[0]
			return(int(a))
		except :			
			print('SQL_getMoldLocNewIndex Error :: Unknown table')

        #====================================================================================
        # Mold list check Function
        #------------------------------------------------------------------------------------
        def checkMOLDLIST(self, NAME) :
                try :
                        for i, s in enumerate(self.list_ld) :
                                #print (s, i)
                                if NAME in s:
                                        print i, s
                                        return i

                        return -1	#HA180123 0 -> -1 Modify
                except :
                        return -1

        #====================================================================================
        # getMOLDAREASqlBleDevice Function
        #------------------------------------------------------------------------------------
        def getMOLDAREASqlBleDevice(self, ScannerID1, ScannerID2, RSSI, sDate, eDate) :
                ret = []
                query = "select blackbin_name, blackbin_bs_name, MAX(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where (blackbin_bs_name = %s or blackbin_bs_name = %s) and blackbin_rssi < %s and blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s group by blackbin_name, blackbin_bs_name order by blackbin_name ASC"
                self.curs.execute(query, (ScannerID1, ScannerID2, RSSI, sDate, eDate))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)

                return(ret)

        def getMOLDAREA1SqlBleDevice(self, ScannerID1, RSSI, sDate, eDate) :
                ret = []
                query = "select blackbin_name, blackbin_bs_name, MAX(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where (blackbin_bs_name = %s ) and blackbin_rssi < %s and blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s group by blackbin_name, blackbin_bs_name order by blackbin_name ASC"
                self.curs.execute(query, (ScannerID1, RSSI, sDate, eDate))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)

                return(ret)

        #====================================================================================
        # getSqlBleDevice_Mon Function
        #------------------------------------------------------------------------------------
        def getSqlBleDevice_Mon(self, ScannerID, sDate, eDate) :
                ret = []

                query = "select blackbin_name, count(blackbin_name), MAX(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where (blackbin_bs_name = %s or blackbin_bs_name = %s) and (blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s) group by blackbin_name order by blackbin_name ASC"

                print(query, ScannerID)
                self.curs.execute(query, (ScannerID[1], ScannerID[2], sDate, eDate))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        print(r)

                return(ret)

        #====================================================================================
        # getSqlBleDevice_CutRSSI_MAX Function
        #------------------------------------------------------------------------------------
        def getSqlBleDevice_CutRSSI_MAX(self, ScannerID, sDate, eDate, RSSI) :
                ret = []

                query = "select blackbin_name, MAX(convert(INT, blackbin_rssi)) from " + self.gtable_name + " where (blackbin_bs_name = %s) and (blackbin_receivedatetime >= %s and blackbin_receivedatetime < %s) and (blackbin_rssi <= %s) group by blackbin_name order by blackbin_name ASC"

                self.curs.execute(query, (ScannerID, sDate, eDate, RSSI))
                for r in self.curs.fetchall() :
                        ret.append(r)
                        #print(r)
                return(ret)

	#================================================================================================================================
        def RSSI_Calc(self, RSSI) :
                # d = 10^((tx_power - rssi)/(10*n))
                # n = 2 or 5 (variable
                # tx_power = -28 for 1m
                #tx_power = -34 #org
                #tx_power = -28
		tx_power = -21	#HA171113 New

                #rssi = int(RSSI, 10)
                #num = 3.2      #org
                #num = 2.6
                #num = 2.77
		num = 2.7	#HA171113 New
                #val = ( (tx_power - rssi) / (10 * num) )

                #print('RSSI = %d') % (RSSI)
                val = ( (tx_power - RSSI) / (10 * num) )


                d = math.pow(10, val)

                #print('val = %f, rssi = %d, distance = %f')%(val, RSSI, d)

                # return cm unit send
                return(d*100)

	#================================================================================================================================
	def getRSSItoDistance_Linear(self, rssi_data) :

        	if(rssi_data > -5) :
                	R = 1.0
	        elif(rssi_data > -36) :
        	        A = -5.53
                	B = -16.2
	                R = A*rssi_data + B

        	else :
                	A = -130.375
	                B = -4509.875
        	        R = A*rssi_data + B
        	return (R)

	#================================================================================================================================
        def RSSI_Calc_Mod(self, RSSI) :
                # d = 10^((tx_power - rssi)/(10*n))
                # n = 2 or 5 (variable
                # tx_power = -28 for 1m
                #tx_power = -34 #org
                #tx_power = -28
		tx_power = -21	#HA171113 New

                #rssi = int(RSSI, 10)
                #num = 3.2      #org
                #num = 2.6
                #num = 2.77
		num = 2.7	#HA171113 New
                #val = ( (tx_power - rssi) / (10 * num) )

		if 0 : 
                	val = ( (tx_power - RSSI) / (10 * num) )
                	d = math.pow(10, val)
			d = d * 100

		else : 
			if(RSSI >= -40) : 

                		val = ( (tx_power - RSSI) / (10 * num) )
	                	d = math.pow(10, val)
				d = d * 100
				 
			else : 
				A = -130375.
				B = -4509.875
				d = A*RSSI + B

                #print('val = %f, rssi = %d, distance = %f')%(val, RSSI, d)

                # return cm unit send
                return(d)
#================================================================================================================================


