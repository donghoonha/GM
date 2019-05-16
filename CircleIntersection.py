#!/usr/bin/env python
# -*- coding: cp949 -*-

import os
import time, threading
import datetime
import MySQLdb
import pymssql
import math

from subprocess import *

class CircleIntersectClass :

    PHI =               3.14159265358979323844
    PHI_2 =             6.28318530717958647692
    PHI_INV =           0.31830988618379067154
    PHI_DIV_2 =         1.57079632679489661923          #/* pi / 2.0 */
    PHI_DIV_4 =         0.785398163339744830962         #/* pi / 4.0 */
    RAD_TO_DEG =        57.29577951408240087684         #/* (1.0/pi) * 180.0 */
    DEG_TO_RAD =        0.01745329251994329577          #/* (1.0/180.0) * pi */
    LN_2 =              0.693147180559945309417         #/* ln(2.0) */
    SQRT2 =             1.41421356237309504880          #/* sqrt(2.0) */
    SQRT2_2 =           0.70710678118654752440          #/* sqrt(2.0) / 2.0 */
    FV_ZERO =           1.0e-12
    INIT_TOL =          0.01

    def __init__(self) :
        print('CircleIntersection Init')
    #function define
    #VtMax(a,b) (((a) > (b)) ? (a) : (b))
    def VtMax(self, a, b) :
        #print('VtMax')
        if(a>b) :
            return a
        else :
            return b

    def VtMin(self, a, b) :
        #print('VtMin')
        if(a<b) :
            return a
        else :
            return b

    def VtA3Add(self, a, b) :
        rslt = []
        for count in range(len(a)) :
            rslt.append(a[count]+b[count])
        #rslt[0] = a[0] + b[0]
        #rslt[1] = a[1] + b[1]
        #rslt[2] = a[2] + b[2]
        return rslt

    def VtA3Sub(self, a, b) :
        rslt = []
        for count in range(len(a)) :
            rslt.append(a[count]-b[count])
        return rslt

    def VtA3Scale(self, k, b) :
        rslt = []
        for count in range(len(b)) :
            rslt.append(k*b[count])
        return rslt

    def VtA3Reverse(self, a) :
        rslt = []
        for count in range(len(a)) :
            rslt.append((-1)*a[count])
        return rslt

    def VtA3Dot(self, a, b) :
        rslt = (a[0]*b[0] + a[1]*b[1] + a[2]*b[2])
        return rslt

    def VtA3Len(self, a) :
        rslt = math.sqrt(self.VtA3Dot(a,a))
        return rslt

    def VtA3Unit(self, a) :
        rslt = []
        lenInv = 1.0 / self.VtA3Len(a)
        for count in range(len(a)) :
            rslt.append(a[count] * lenInv)
        return rslt
    def VtA3Cross(self, a, b) :
        rslt = []
        rslt.append(a[1]*b[2] - a[2]*b[1])
        rslt.append(a[2]*b[0] - a[0]*b[2])
        rslt.append(a[0]*b[1] - a[1]*b[0])
        return rslt

    def VtA3Copy(self, a) :
        rslt = []
        for count in range(len(a)) :
            rslt.append(a[count])
        return rslt

    def VmMatGetInvXform(self, m) :
        w, h = 4, 4
        inv = [[0 for x in range(w)] for y in range(h)]     #inv matrix 4x4 create

        inv[0][0] = m[0][0]
        inv[0][1] = m[1][0]
        inv[0][2] = m[2][0]

        inv[1][0] = m[0][1]
        inv[1][1] = m[1][1]
        inv[1][2] = m[2][1]

        inv[2][0] = m[0][2]
        inv[2][1] = m[1][2]
        inv[2][2] = m[2][2]
        inv[0][3] = -1*(m[0][3] * m[0][0] + m[1][3] * m[1][0] + m[2][3] * m[2][0])
        inv[1][3] = -1*(m[0][3] * m[0][1] + m[1][3] * m[1][1] + m[2][3] * m[2][1])
        inv[2][3] = -1*(m[0][3] * m[0][2] + m[1][3] * m[1][2] + m[2][3] * m[2][2])

        inv[3][0] = 0.0
        inv[3][1] = 0.0
        inv[3][2] = 0.0
        inv[3][3] = 1.0

        return (inv)

    #=============== Function ================
    def TriArea(self, p1, p2, p3) :
        # Calculation Area for Triangle
        cross = []
        cross.append( (p2[1] - p1[1])*(p3[2] - p1[2]) - (p3[1] - p1[1])*(p2[2] - p1[2]) )
        cross.append( (p2[2] - p1[2])*(p3[0] - p1[0]) - (p3[2] - p1[2])*(p2[0] - p1[0]) )
        cross.append( (p2[0] - p1[0])*(p3[1] - p1[1]) - (p3[0] - p1[0])*(p2[1] - p1[1]) )

        ss = (cross[0]*cross[0] + cross[1]*cross[1] + cross[2]*cross[2])

        if( ss < self.FV_ZERO ) :
            return 0.0
        return ( math.sqrt(ss)/2.0 )

    def check_pnt_in_tri(self, pnt, p1, p2, p3, fv_tri_area, fv_tol) :

        try :
            # check internal or external for triangle area
            #print('check_pnt_in_tri start')
            if( fv_tri_area <= self.FV_ZERO ) :
                fv_tri_area = self.TriArea( p1, p2, p3 )
                if( fv_tri_area <= self.FV_ZERO ) :
                    return -1

            area_sum = self.TriArea( p1, p2, pnt )
            area_sum += self.TriArea( p1, p3, pnt )
            area_sum += self.TriArea( p2, p3, pnt )

            #print('area_sum : ',area_sum)
            #print('fv_tri_area : ',fv_tri_area)
            if( math.fabs(area_sum-fv_tri_area) <= fv_tol ) :
                return 0  #//pnt exists in/on triangualr
            return 1
        except :
            print('check_pnt_in_tri Error')

    def check_pnt_in_quad(self, pnt, p1, p2, p3, p4, fv_tri_area1, fv_tri_area2, fv_tol) :

        try :
            # check internal or external for quad area
            #print('check_pnt_in_quad start')
            if( fv_tri_area1 <= self.FV_ZERO ) :
                fv_tri_area1 = self.TriArea( p1, p2, p3 )
                if( fv_tri_area1 <= self.FV_ZERO ) :
                    return -1

            area_sum = self.TriArea( p1, p2, pnt )
            area_sum += self.TriArea( p1, p3, pnt )
            area_sum += self.TriArea( p2, p3, pnt )

            #print('area_sum : ',area_sum)
            #print('fv_tri_area1 : ',fv_tri_area1)

            if( math.fabs(area_sum-fv_tri_area1) <= fv_tol ) :
                return 0  #//pnt exists in/on triangualr

            if( fv_tri_area2 <= self.FV_ZERO ) :
                fv_tri_area2 = self.TriArea( p1, p3, p4 )
                if( fv_tri_area2 <= self.FV_ZERO ) :
                    return -1

            area_sum = self.TriArea( p1, p3, pnt )
            area_sum += self.TriArea( p3, p4, pnt )
            area_sum += self.TriArea( p4, p1, pnt )

            #print('area_sum : ',area_sum)
            #print('fv_tri_area2 : ',fv_tri_area2)

            if( math.fabs(area_sum-fv_tri_area2) <= fv_tol ) :
                return 0  #//pnt exists in/on triangualr

            return 1
        except :
            print('check_pnt_in_quad Error')

    def get_2circle_intersection_coord(self,fv_xyz_center_c1,fv_xyz_center_c2,fv_D1_c1,fv_D2_c2,fv_tol) :
        # how-to : (iv_num_pnt, fv_xyz_out) = get_2circle_intersection_coord(...)

        try :
            w, h = 4, 4
            xform = [[0 for x in range(w)] for y in range(h)]     #inv matrix 4x4 create
            fv_xyz_out = []

            center = []
            maxaxis = []
            minaxis = []
            normal = []
            fv_xyz_center_c1_new = [0,0,0]
            fv_xyz_center_c2_new = [0,0,0]

            iv_num_pnt = 0
            f1, f2, f3, f4 = 0,0,0,0
            fv_tol = 0
            x1, x2, y1, y2 = 0,0,0,0

            ret0 = 0        # return value

            if( fv_tol <= self.FV_ZERO ) :   #tolerance define
                f1 = self.VtMin( fv_D1_c1, fv_D2_c2 )
                if( f1 <= self.FV_ZERO ) :
                    fv_tol = self.INIT_TOL
                else :
                    fv_tol = f1 / 100.0

            print('get_2circle_intersection_coord start')
            #print('f1 : ', f1)
            #print('fv_tol : ', fv_tol)

            fv_tol2 = fv_tol * fv_tol

            if( (fv_D1_c1 <= fv_tol) or (fv_D2_c2 <= fv_tol) ) :
                print('(Error :: fv_D1_c1 <= fv_tol)')
                ret0 += -1
                #return -1  #error : radius is too small

            fv1 = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_center_c2)
            f1 = self.VtA3Dot( fv1, fv1 )
            #print('f1-1 : ', f1, fv_tol2)
            if( f1 <= fv_tol2 ) :
                print('(Error :: f1 <= fv_tol2)')
                ret0 += -1
                #return -1  #error : duplicated coordinates of 2 circles

            fv_T = math.sqrt( f1 )

            f1 = fv_T - fv_D1_c1 - fv_D2_c2
            #print('f1-2 : ', f1, fv_T)
            if( f1 >= -fv_tol ) : #no intersection between 2 circles, use formula internal
                iv_num_pnt = 1
                fv_xyz_out.append( (fv_xyz_center_c1[0]*fv_D2_c2 + fv_xyz_center_c2[0]*fv_D1_c1) / (fv_D1_c1+fv_D2_c2) )
                fv_xyz_out.append( (fv_xyz_center_c1[1]*fv_D2_c2 + fv_xyz_center_c2[1]*fv_D1_c1) / (fv_D1_c1+fv_D2_c2) )
                fv_xyz_out.append( 0.0 )
                print('2', ret0, iv_num_pnt, fv_xyz_out)
                #return (2, iv_num_pnt, fv_xyz_out)
                return (ret0, iv_num_pnt, fv_xyz_out)   #HA170306 ADD

            f2 = (fv_xyz_center_c2[0] - fv_xyz_center_c1[0])      #X2 == X1
            #print('f2 :', f2)

            if( math.fabs(f2) > fv_tol ) :
                #print('f2 > fv_tol : ', f2, fv_tol, ' start')
                f3 = ( (fv_xyz_center_c2[1] - fv_xyz_center_c1[1]) / f2 )
                #print('f3 : ',f3)
                f1 = math.atan(f3)
                #print('f1 :', f1)

                f4 = ( (fv_D1_c1*fv_D1_c1 - fv_D2_c2*fv_D2_c2 + fv_T*fv_T) / (2*fv_D1_c1*fv_T) )
                #print('f4', f4)
                if( (f4 > -1.0) and (f4 < 1.0) ) :
                    f2 = math.acos(f4)
                else :
                    # futher modify
                    f2 = 1.0
                    #print('atan > +- 1.0', f4)

                f_cos1 = math.cos( f1 + f2 )
                f_cos2 = math.cos( f1 - f2 )
                f_sin1 = math.sin( f1 + f2 )
                f_sin2 = math.sin( f1 - f2 )
                x1 = (fv_xyz_center_c1[0] + fv_D1_c1 * f_cos1)
                x2 = (fv_xyz_center_c1[0] + fv_D1_c1 * f_cos2)
                y1 = (fv_xyz_center_c1[1] + fv_D1_c1 * f_sin1)
                y2 = (fv_xyz_center_c1[1] + fv_D1_c1 * f_sin2)
                #print('f2 > fv_tol end')
                print(x1, x2, y1, y2)

            else :          #//Transform Coordination  //2017/02/26 -> Add Exception Process
                print('Transform Coordination start')
                center.append(0.0)      #center[0]
                center.append(0.0)      #center[1]
                center.append(0.0)      #center[2]
                maxaxis.append(0.0)     #maxaxis[0]
                maxaxis.append(1.0)     #maxaxis[1]
                maxaxis.append(0.0)     #maxaxis[2]
                minaxis.append(-1.0)    #minaxis[0]
                minaxis.append(0.0)     #minaxis[1]
                minaxis.append(0.0)     #minaxis[2]
                normal.append(0.0)      #normal[0]
                normal.append(0.0)      #normal[1]
                normal.append(1.0)      #normal[2]

                xform[0][0] = maxaxis[0]
                xform[1][0] = maxaxis[1]
                xform[2][0] = maxaxis[2]
                xform[3][0] = 1.0
                xform[0][1] = minaxis[0]
                xform[1][1] = minaxis[1]

                xform[2][1] = minaxis[2]
                xform[3][1] = 1.0
                xform[0][2] = normal[0]
                xform[1][2] = normal[1]
                xform[2][2] = normal[2]
                xform[3][2] = 1.0
                xform[0][3] = center[0]
                xform[1][3] = center[1]
                xform[2][3] = center[2]
                xform[3][3] = 1.0
                Invxform = self.VmMatGetInvXform(xform)

                xx = fv_xyz_center_c1[0]
                yy = fv_xyz_center_c1[1]
                zz = 0.0
                fv_xyz_center_c1_new[0] = ((xx-center[0]) * xform[0][0] + (yy-center[1]) * xform[1][0] + (zz-center[2]) * xform[2][0])
                fv_xyz_center_c1_new[1] = ((xx-center[0]) * xform[0][1] + (yy-center[1]) * xform[1][1] + (zz-center[2]) * xform[2][1])
                fv_xyz_center_c1_new[2] = 0.0

                xx = fv_xyz_center_c2[0]
                yy = fv_xyz_center_c2[1]
                fv_xyz_center_c2_new[0] = ((xx-center[0]) * xform[0][0] + (yy-center[1]) * xform[1][0] + (zz-center[2]) * xform[2][0])
                fv_xyz_center_c2_new[1] = ((xx-center[0]) * xform[0][1] + (yy-center[1]) * xform[1][1] + (zz-center[2]) * xform[2][1])
                fv_xyz_center_c2_new[2] = 0.0

                fv_D1_c1_new, fv_D2_c2_new = 0, 0

                if( fv_xyz_center_c1_new[0] > fv_xyz_center_c2_new[0]) :
                    fv_D1_c1_new = fv_D2_c2
                    fv_D2_c2_new = fv_D1_c1

                    f2 = fv_xyz_center_c1_new[0]
                    fv_xyz_center_c1_new[0] = fv_xyz_center_c2_new[0]
                    fv_xyz_center_c2_new[0] = f2

                    f2 = fv_xyz_center_c1_new[1]
                    fv_xyz_center_c1_new[1] = fv_xyz_center_c2_new[1]
                    fv_xyz_center_c2_new[1] = f2

                else :
                    fv_D1_c1_new = fv_D1_c1
                    fv_D2_c2_new = fv_D2_c2


                f2 = fv_xyz_center_c2_new[0] - fv_xyz_center_c1_new[0]      #X2 == X1
                f3 = (fv_xyz_center_c2_new[1] - fv_xyz_center_c1_new[1]) / f2
                f1 = math.atan( f3 )

                f4 = (fv_D1_c1_new*fv_D1_c1_new - fv_D2_c2_new*fv_D2_c2_new + fv_T*fv_T) / (2*fv_D1_c1_new*fv_T)

                #f2 = math.acos(f4)

                #print('f4 :', f4)
                if( (f4 > -1.0) and (f4 < 1.0) ) :
                    f2 = math.acos(f4)
                else :
                    # futher modify
                    f2 = 1.0
                    #print('atan > +- 1.0', f4)

                f_cos1 = math.cos( f1 + f2 )
                f_cos2 = math.cos( f1 - f2 )
                f_sin1 = math.sin( f1 + f2 )
                f_sin2 = math.sin( f1 - f2 )
                xx = fv_xyz_center_c1_new[0] + fv_D1_c1_new * f_cos1
                yy = fv_xyz_center_c1_new[1] + fv_D1_c1_new * f_sin1
                x1 = xx*Invxform[0][0] + yy*Invxform[1][0];  #// + zz*Invxform[2][0]
                y1 = xx*Invxform[0][1] + yy*Invxform[1][1];  #// + zz*Invxform[2][1]
                #z1 = xx*Invxform[0][2] + yy*Invxform[1][2];  #// + zz*Invxform[2][2]

                xx = fv_xyz_center_c1_new[0] + fv_D1_c1_new * f_cos2
                yy = fv_xyz_center_c1_new[1] + fv_D1_c1_new * f_sin2
                x2 = xx*Invxform[0][0] + yy*Invxform[1][0];  #// + zz*Invxform[2][0]
                y2 = xx*Invxform[0][1] + yy*Invxform[1][1];  #// + zz*Invxform[2][1]

            #print('iv_num_pnt', iv_num_pnt)
            iv_num_pnt = 2
            fv_xyz_out.append(x1)
            fv_xyz_out.append(y1)
            fv_xyz_out.append(0.0)
            fv_xyz_out.append(x2)
            fv_xyz_out.append(y2)
            fv_xyz_out.append(0.0)

            print(ret0, iv_num_pnt, fv_xyz_out)

            return (ret0, iv_num_pnt, fv_xyz_out)

        except :
            print("get_2circle_intersection_coord Error!!!")

    def get_3circle_intersection_coord(self,fv_xyz_center_c1,fv_xyz_center_c2,fv_xyz_center_c3,fv_D1_c1,fv_D2_c2,fv_D3_c3,fv_tol) :
        # how-to : (iv_num_pnt, fv_xyz_out) = get_3circle_intersection_coord(...)
        try :

            w, h = 3, 2
            fv_xyz_c12 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c13 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c23 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create

            iv_pnt_num = 0

            ret0 = 0   #return value addition, proof the error

            #print('get_3circle_intersection_coord start')

            #print('fv_xyz_c12',fv_xyz_c12)
            #print('fv_xyz_c13',fv_xyz_c13)
            #print('fv_xyz_c23',fv_xyz_c23)

            fv_area_total = self.TriArea( fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3 );

            #print('fv_area_total :', fv_area_total)

            if( fv_area_total <= self.FV_ZERO ) :
                ret0 += -1
                #return -1

            #================================================
            #c1 - c2
            #iv_num = 0
            fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            (ret1, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c2, fv_D1_c1, fv_D2_c2, fv_tol );

            #print('ret1 :', ret1)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret1 < 0 ) :
                #print('Error :: (3circle : ret1 ) ', ret1)
                ret0 += ret1;
                #print('Error :: (3circle : ret0 ) ', ret0)
                return (ret0, fv_xyz)       #HA170302

            for i in range(iv_num) :
                for j in range(3) :
                    fv_xyz_c12[i][j] = fv_xyz[i*3+j]
                iv_pnt_num = iv_pnt_num + 1

            #print('fv_xyz_c12 : ', fv_xyz_c12)
            #================================================
            #c1 - c3
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            (ret2, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c3, fv_D1_c1, fv_D3_c3, fv_tol );

            #print('ret2 :', ret2)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret2 < 0 ) :
                #print('Error :: (3circle : ret2 ) ', ret1)
                ret0 += ret2;
                #print('Error :: (3circle : ret0 ) ', ret0)
                return (ret0, fv_xyz)       #HA170302

            for i in range(iv_num) :
                for j in range(3) :
                    fv_xyz_c13[i][j] = fv_xyz[i*3+j]
                iv_pnt_num = iv_pnt_num + 1

            #print('fv_xyz_c13 : ',fv_xyz_c13)
            #================================================
            #c2 - c3
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            (ret3, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c2, fv_xyz_center_c3, fv_D2_c2, fv_D3_c3, fv_tol );

            #print('ret3 :', ret3)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret3 < 0 ) :
                #print('Error :: (3circle : ret3 ) ', ret3)
                ret0 += ret3;
                #print('Error :: (3circle : ret0 ) ', ret0)
                return (ret0, fv_xyz)       #HA170302

            for i in range(iv_num) :
                for j in range(3) :
                    fv_xyz_c23[i][j] = fv_xyz[i*3+j]
                iv_pnt_num = iv_pnt_num + 1

            #print('fv_xyz_c23 : ',fv_xyz_c23, iv_pnt_num)
            #================================================
            fv_xyz_out = [0.0,0.0,0.0]

            if( iv_pnt_num == 3 ) :
                # cross intersection : 0
                for i in range(3) :
                    fv_xyz_out[i] = (fv_xyz_c12[0][i] + fv_xyz_c13[0][i] + fv_xyz_c23[0][i] ) / 3.0

                #print('11:', fv_xyz_out)
                ch = self.check_pnt_in_tri( fv_xyz_out, fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                #print('iv_pnt_num = 3 : ', ch, fv_xyz_out)
                if(ch == 0) :
                    return (ret0, fv_xyz_out)

            #elif(iv_pnt_num == 5) :
                # future excpetion process
                #print('iv_pnt_num == 5')
                #return (iv_pnt_num, fv_xyz)

            elif(iv_pnt_num == 4) :
                if(ret1 == 0) :
                    #c1 - c2
                    ch = self.check_pnt_in_tri( fv_xyz_c12[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c12[0][i]
                    else :
                        ch = self.check_pnt_in_tri( fv_xyz_c12[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c12[1][i]
                        else :
                            #C1 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                    if(iv_pnt_num == 4) :
                        for i in range(3) :
                            fv_xyz_out[i] += (fv_xyz_c13[0][i] + fv_xyz_c23[0][i])

                elif(ret2 == 0) :
                    #c1 - c3
                    ch = self.check_pnt_in_tri( fv_xyz_c13[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c13[0][i]

                    else :
                        ch = self.check_pnt_in_tri( fv_xyz_c13[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c13[1][i]
                        else :
                            #C1 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c13[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c13[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c13[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c13[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                    if(iv_pnt_num == 4) :
                        for i in range(3) :
                            fv_xyz_out[i] += (fv_xyz_c12[0][i] + fv_xyz_c23[0][i])

                elif(ret3 == 0) :
                    #c2 - c3
                    ch = self.check_pnt_in_tri( fv_xyz_c23[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c23[0][i]

                    else :
                        ch = self.check_pnt_in_tri( fv_xyz_c23[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c23[1][i]
                        else :
                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]

                    if(iv_pnt_num == 4) :
                        for i in range(3) :
                            fv_xyz_out[i] += (fv_xyz_c12[0][i] + fv_xyz_c13[0][i])
                else :
                    return (iv_pnt_num, fv_xyz_out)

            elif( iv_pnt_num >= 5 ) :   # if : 5(4point, 1point mismatch), 6(normal)
                if(ret1 == 0) :
                    #c1 - c2
                    ch = self.check_pnt_in_tri( fv_xyz_c12[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c12[0][i]

                    else :
                        ch = self.check_pnt_in_tri( fv_xyz_c12[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c12[1][i]
                        else :
                            #C1 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                else :
                    for i in range(3) :
                        fv_xyz_out[i] += fv_xyz_c12[0][i]

                if(ret2 == 0) :
                    #c1 - c3
                    ch = self.check_pnt_in_tri( fv_xyz_c13[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c13[0][i]

                    else :
                        ch = self.check_pnt_in_tri( fv_xyz_c13[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c13[1][i]
                        else :
                            #C1 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c13[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c13[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c13[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c13[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                else :
                    for i in range(3) :
                        fv_xyz_out[i] += fv_xyz_c13[0][i]

                if(ret3 == 0) :
                    #c2 - c3
                    ch = self.check_pnt_in_tri( fv_xyz_c23[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c23[0][i]

                    else :
                        ch = self.check_pnt_in_tri( fv_xyz_c23[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c23[1][i]
                        else :
                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]

                else :
                    for i in range(3) :
                        fv_xyz_out[i] += fv_xyz_c23[0][i]


            #print(fv_xyz_out)
            #final x,y,x transfer
            for i in range(3) :
                fv_xyz_out[i] /= 3.0

            #print(fv_xyz_out)
            ch = self.check_pnt_in_tri( fv_xyz_out, fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_area_total, fv_tol );
            if(ch == 0) :
                return (ret0, fv_xyz_out)
            #================================================

            return (ret0, fv_xyz)

        except :
            print("get_3circle_intersection_coord Error!!!")

    def get_4circle_intersection_coord(self,fv_xyz_center_c1,fv_xyz_center_c2,fv_xyz_center_c3,fv_xyz_center_c4,fv_D1_c1,fv_D2_c2,fv_D3_c3,fv_D4_c4,fv_tol) :
        # how-to : (iv_num_pnt, fv_xyz_out) = get_4circle_intersection_coord(...)
        try :

            w, h = 3, 2
            fv_xyz_c12 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c23 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c34 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c41 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create

            fv_xyz_c13 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c24 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create

            iv_pnt_num = 0
            ret0 = 0    # return value
            count_xyz = 0

            #print('get_4circle_intersection_coord start')

            #print('fv_xyz_c12',fv_xyz_c12)
            #print('fv_xyz_c23',fv_xyz_c23)
            #print('fv_xyz_c34',fv_xyz_c34)
            #print('fv_xyz_c41',fv_xyz_c41)

            area_tri_123 = self.TriArea( fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3 );
            if( area_tri_123 <= self.FV_ZERO ) :
                return -1

            area_tri_134 = self.TriArea( fv_xyz_center_c1, fv_xyz_center_c3, fv_xyz_center_c4 );
            if( area_tri_134 <= self.FV_ZERO ) :
                return -1

            #print('area_tri_123 :', area_tri_123)
            #print('area_tri_134 :', area_tri_134)

            #================================================
            #c1 - c2
            #iv_num = 0
            fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            ret12 = 0
            ret23 = 0
            ret34 = 0
            ret41 = 0
            ret13 = 0
            ret24 = 0

            if(fv_xyz_center_c1[0] > fv_xyz_center_c2[0] ) :
                (ret12, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c2, fv_xyz_center_c1, fv_D2_c2, fv_D1_c1, fv_tol );
            else :
                (ret12, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c2, fv_D1_c1, fv_D2_c2, fv_tol );

            #print('ret12 :', ret12)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret12 < 0 ) :
                ret0 += ret12
                #return (ret12, fv_xyz)
            elif( ret12 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c12[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c12 : ', fv_xyz_c12)
            else :
                print('Further Error!!! count_xyz = ', count_xyz)
            #================================================
            #c2 - c3
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            if(fv_xyz_center_c2[0] > fv_xyz_center_c3[0] ) :
                (ret23, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c3, fv_xyz_center_c2, fv_D3_c3, fv_D2_c2, fv_tol );
            else :
                (ret23, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c2, fv_xyz_center_c3, fv_D2_c2, fv_D3_c3, fv_tol );

            #print('ret23 :', ret23)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret23 < 0 ) :
                ret0 += ret23
                #return (ret23, fv_xyz)

            elif( ret23 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c23[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c23 : ', fv_xyz_c23)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)
            #================================================
            #c3 - c4
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            if(fv_xyz_center_c3[0] > fv_xyz_center_c4[0] ) :
                (ret34, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c4, fv_xyz_center_c3, fv_D4_c4, fv_D3_c3, fv_tol );
            else :
                (ret34, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c3, fv_xyz_center_c4, fv_D3_c3, fv_D4_c4, fv_tol );

            #print('ret34 :', ret34)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret34 < 0 ) :
                ret0 += ret34
                #return (ret34, fv_xyz)

            elif( ret34 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c34[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c34 : ', fv_xyz_c34)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)
            #================================================
            #c4 - c1
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            print(fv_xyz_center_c1[0], fv_xyz_center_c2[0], fv_xyz_center_c3[0], fv_xyz_center_c4[0])
            if(fv_xyz_center_c4[0] > fv_xyz_center_c1[0] ) :
                #print('fv_xyz_center_c4[0] >= fv_xyz_center_c1[0]')
                (ret41, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c4, fv_D1_c1, fv_D4_c4, fv_tol );
            else :
                #print('fv_xyz_center_c4[0] < fv_xyz_center_c1[0]')
                (ret41, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c4, fv_xyz_center_c1, fv_D4_c4, fv_D1_c1, fv_tol );

            #print('ret41 :', ret41)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret41 < 0 ) :
                ret0 += ret41
                #return (ret41, fv_xyz)

            elif( ret41 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c41[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c41, ret0 : ', fv_xyz_c41, ret0)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)

            #================================================

            #c1 - c3
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            if(fv_xyz_center_c1[0] > fv_xyz_center_c3[0] ) :
                (ret13, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c3, fv_xyz_center_c1, fv_D3_c3, fv_D1_c1, fv_tol );
            else :
                (ret13, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c3, fv_D1_c1, fv_D3_c3, fv_tol );

            #print('ret13 :', ret13)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret13 < 0 ) :
                ret0 += ret13
                #return (ret13, fv_xyz)

            elif( ret13 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c13[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c13, ret0 : ', fv_xyz_c13, ret0)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)

            #================================================
            #c2 - c4
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            if(fv_xyz_center_c2[0] > fv_xyz_center_c4[0] ) :
                (ret24, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c4, fv_xyz_center_c2, fv_D4_c4, fv_D2_c2, fv_tol );
            else :
                (ret24, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c2, fv_xyz_center_c4, fv_D2_c2, fv_D4_c4, fv_tol );

            #print('ret24 :', ret24)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret24 < 0 ) :
                ret0 += ret24
                #return (ret13, fv_xyz)

            elif( ret24 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c24[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c24, ret0 : ', fv_xyz_c24, ret0)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)

            #================================================

            # switch
            fv_xyz_out = [0.0,0.0,0.0]


            print('iv_pnt_num',iv_pnt_num)

            '''
            #if( iv_pnt_num == 4 ) :
            if( iv_pnt_num == 3 ) :
                # cross intersection : 0
                for i in range(3) :
                    fv_xyz_out[i] = (fv_xyz_c12[0][i] + fv_xyz_c23[0][i] + fv_xyz_c34[0][i] + fv_xyz_c41[0][i] ) / 4.0
                    #fv_xyz_out[i] = (fv_xyz_c12[0][i] + fv_xyz_c23[0][i] + fv_xyz_c34[0][i] + fv_xyz_c41[1][i] ) / count_xyz    #HA170306 New

                #print('11:', fv_xyz_out)
                ch = self.check_pnt_in_quad( fv_xyz_out, fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                #print('iv_pnt_num = 4 : ', ch, fv_xyz_out)
                if(ch == 0) :
                    return (0, fv_xyz_out)
            '''

            #if( (iv_pnt_num >= 2) and (iv_pnt_num <= 8) ) :   # if : 5(4point, 1point mismatch), 6(normal)
            if( iv_pnt_num >= 0) :
                if(ret12 == 0) :
                    #c1 - c2
                    ch = self.check_pnt_in_quad( fv_xyz_c12[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c12[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c12[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c12[1][i]
                        else :
                            #C1 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                else :
                    for i in range(3) :
                    #    fv_xyz_out[i] += fv_xyz_c12[0][i]
                          fv_xyz_out[i] += 0
                if(ret23 == 0) :
                    #c2 - c3
                    ch = self.check_pnt_in_quad( fv_xyz_c23[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c23[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c23[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c23[1][i]
                        else :
                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]

                else :
                    for i in range(3) :
                    #    fv_xyz_out[i] += fv_xyz_c23[0][i]
                        fv_xyz_out[i] += 0

                if(ret34 == 0) :
                    #c3 - c4
                    ch = self.check_pnt_in_quad( fv_xyz_c34[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c34[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c34[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )

                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c34[1][i]
                        else :
                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c34[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c34[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C4 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c34[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c34[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c4[0]
                                fv_xyz_out[1] += fv_xyz_center_c4[1]
                                fv_xyz_out[2] += fv_xyz_center_c4[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]

                else :
                    for i in range(3) :
                    #    fv_xyz_out[i] += fv_xyz_c34[0][i]
                        fv_xyz_out[i] += 0

                if(ret41 == 0) :
                    #c4 - c1
                    ch = self.check_pnt_in_quad( fv_xyz_c41[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c41[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c41[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c41[1][i]
                        else :
                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c41[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c41[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C4 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c41[0])

                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c41[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c4[0]
                                fv_xyz_out[1] += fv_xyz_center_c4[1]
                                fv_xyz_out[2] += fv_xyz_center_c4[2]

                else :
                    for i in range(3) :
                        #fv_xyz_out[i] += fv_xyz_c41[0][i]
                        fv_xyz_out[i] += 0

                if(ret13 == 0) :
                    #c1 - c3
                    ch = self.check_pnt_in_quad( fv_xyz_c13[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c13[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c13[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c13[1][i]
                        else :
                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c13[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c13[1])
                            fv1 += self.VtA3Dot( fv, fv )
                            #C4 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c13[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c13[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                else :
                    for i in range(3) :
                        #fv_xyz_out[i] += fv_xyz_c41[0][i]
                        fv_xyz_out[i] += 0

                if(ret24 == 0) :
                    #c1 - c3
                    ch = self.check_pnt_in_quad( fv_xyz_c24[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c24[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c24[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c24[1][i]
                        else :
                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c24[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c24[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C4 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c24[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c24[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c4[0]
                                fv_xyz_out[1] += fv_xyz_center_c4[1]
                                fv_xyz_out[2] += fv_xyz_center_c4[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]

                else :
                    for i in range(3) :
                        #fv_xyz_out[i] += fv_xyz_c41[0][i]
                        fv_xyz_out[i] += 0

            #=============================================================
            print(fv_xyz_out, count_xyz)
            #final x,y,x transfer

            if(count_xyz > 0) :
                for i in range(3) :
                    fv_xyz_out[i] /= count_xyz  #4.0

                ch = self.check_pnt_in_quad( fv_xyz_out, fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                #print(fv_xyz_out, ch, ret0)
                if(ch == 0) :
                    return (ret0, fv_xyz_out)
            else :
                fv_xyz_out[0] = 0
                fv_xyz_out[1] = 0
                fv_xyz_out[2] = 0
                return (ret0, fv_xyz_out)

            #================================================

        except :
            print("get_4circle_intersection_coord Error!!!")


    def get_4circle_intersection_coord_4(self,fv_xyz_center_c1,fv_xyz_center_c2,fv_xyz_center_c3,fv_xyz_center_c4,fv_D1_c1,fv_D2_c2,fv_D3_c3,fv_D4_c4,fv_tol) :
        # how-to : (iv_num_pnt, fv_xyz_out) = get_4circle_intersection_coord(...)
        try :

            w, h = 3, 2
            fv_xyz_c12 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c23 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c34 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            fv_xyz_c41 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create

            #fv_xyz_c13 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create
            #fv_xyz_c24 = [[0 for x in range(w)] for y in range(h)]     # matrix 2x3 create

            iv_pnt_num = 0
            ret0 = 0    # return value
            count_xyz = 0

            #print('get_4circle_intersection_coord start')

            #print('fv_xyz_c12',fv_xyz_c12)
            #print('fv_xyz_c23',fv_xyz_c23)
            #print('fv_xyz_c34',fv_xyz_c34)
            #print('fv_xyz_c41',fv_xyz_c41)

            area_tri_123 = self.TriArea( fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3 );
            if( area_tri_123 <= self.FV_ZERO ) :
                return -1

            area_tri_134 = self.TriArea( fv_xyz_center_c1, fv_xyz_center_c3, fv_xyz_center_c4 );
            if( area_tri_134 <= self.FV_ZERO ) :
                return -1

            #print('area_tri_123 :', area_tri_123)
            #print('area_tri_134 :', area_tri_134)

            #================================================
            #c1 - c2
            #iv_num = 0
            fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            ret12 = 0
            ret23 = 0
            ret34 = 0
            ret41 = 0
            ret13 = 0
            ret24 = 0

            if(fv_xyz_center_c1[0] > fv_xyz_center_c2[0] ) :
                (ret12, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c2, fv_xyz_center_c1, fv_D2_c2, fv_D1_c1, fv_tol );
            else :
                (ret12, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c2, fv_D1_c1, fv_D2_c2, fv_tol );

            #print('ret12 :', ret12)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret12 < 0 ) :
                ret0 += ret12
                #return (ret12, fv_xyz)
            elif( ret12 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c12[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c12 : ', fv_xyz_c12)
            else :
                print('Further Error!!! count_xyz = ', count_xyz)
            #================================================
            #c2 - c3
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            if(fv_xyz_center_c2[0] > fv_xyz_center_c3[0] ) :
                (ret23, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c3, fv_xyz_center_c2, fv_D3_c3, fv_D2_c2, fv_tol );
            else :
                (ret23, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c2, fv_xyz_center_c3, fv_D2_c2, fv_D3_c3, fv_tol );

            #print('ret23 :', ret23)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret23 < 0 ) :
                ret0 += ret23
                #return (ret23, fv_xyz)

            elif( ret23 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c23[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c23 : ', fv_xyz_c23)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)
            #================================================
            #c3 - c4
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            if(fv_xyz_center_c3[0] > fv_xyz_center_c4[0] ) :
                (ret34, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c4, fv_xyz_center_c3, fv_D4_c4, fv_D3_c3, fv_tol );
            else :
                (ret34, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c3, fv_xyz_center_c4, fv_D3_c3, fv_D4_c4, fv_tol );

            #print('ret34 :', ret34)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret34 < 0 ) :
                ret0 += ret34
                #return (ret34, fv_xyz)

            elif( ret34 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c34[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c34 : ', fv_xyz_c34)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)
            #================================================
            #c4 - c1
            #iv_num = 0
            #fv_xyz = [0.0,0.0,0.0,0.0,0.0,0.0]
            print(fv_xyz_center_c1[0], fv_xyz_center_c2[0], fv_xyz_center_c3[0], fv_xyz_center_c4[0])
            if(fv_xyz_center_c4[0] > fv_xyz_center_c1[0] ) :
                #print('fv_xyz_center_c4[0] >= fv_xyz_center_c1[0]')
                (ret41, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c1, fv_xyz_center_c4, fv_D1_c1, fv_D4_c4, fv_tol );
            else :
                #print('fv_xyz_center_c4[0] < fv_xyz_center_c1[0]')
                (ret41, iv_num, fv_xyz) = self.get_2circle_intersection_coord( fv_xyz_center_c4, fv_xyz_center_c1, fv_D4_c4, fv_D1_c1, fv_tol );

            #print('ret41 :', ret41)
            #print('iv_num :', iv_num)
            #print('fv_xyz :', fv_xyz)

            if( ret41 < 0 ) :
                ret0 += ret41
                #return (ret41, fv_xyz)

            elif( ret41 == 0 ) :
                count_xyz += 1;

                for i in range(iv_num) :
                    for j in range(3) :
                        fv_xyz_c41[i][j] = fv_xyz[i*3+j]
                    iv_pnt_num = iv_pnt_num + 1

                print('fv_xyz_c41, ret0 : ', fv_xyz_c41, ret0)

            else :
                print('Further Error!!! count_xyz = ', count_xyz)

            #================================================


            # switch
            fv_xyz_out = [0.0,0.0,0.0]


            print('iv_pnt_num',iv_pnt_num)

            '''
            #if( iv_pnt_num == 4 ) :
            if( iv_pnt_num == 3 ) :
                # cross intersection : 0
                for i in range(3) :
                    fv_xyz_out[i] = (fv_xyz_c12[0][i] + fv_xyz_c23[0][i] + fv_xyz_c34[0][i] + fv_xyz_c41[0][i] ) / 4.0
                    #fv_xyz_out[i] = (fv_xyz_c12[0][i] + fv_xyz_c23[0][i] + fv_xyz_c34[0][i] + fv_xyz_c41[1][i] ) / count_xyz    #HA170306 New

                #print('11:', fv_xyz_out)
                ch = self.check_pnt_in_quad( fv_xyz_out, fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                #print('iv_pnt_num = 4 : ', ch, fv_xyz_out)
                if(ch == 0) :
                    return (0, fv_xyz_out)
            '''

            #if( (iv_pnt_num >= 2) and (iv_pnt_num <= 8) ) :   # if : 5(4point, 1point mismatch), 6(normal)
            if( iv_pnt_num >= 0) :
                if(ret12 == 0) :
                    #c1 - c2
                    ch = self.check_pnt_in_quad( fv_xyz_c12[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c12[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c12[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c12[1][i]
                        else :
                            #C1 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c12[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c12[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]

                else :
                    for i in range(3) :
                    #    fv_xyz_out[i] += fv_xyz_c12[0][i]
                          fv_xyz_out[i] += 0
                if(ret23 == 0) :
                    #c2 - c3
                    ch = self.check_pnt_in_quad( fv_xyz_c23[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c23[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c23[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c23[1][i]
                        else :
                            #C2 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c2, fv_xyz_c23[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c23[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c2[0]
                                fv_xyz_out[1] += fv_xyz_center_c2[1]
                                fv_xyz_out[2] += fv_xyz_center_c2[2]

                else :
                    for i in range(3) :
                    #    fv_xyz_out[i] += fv_xyz_c23[0][i]
                        fv_xyz_out[i] += 0

                if(ret34 == 0) :
                    #c3 - c4
                    ch = self.check_pnt_in_quad( fv_xyz_c34[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c34[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c34[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )

                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c34[1][i]
                        else :
                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c34[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c3, fv_xyz_c34[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C4 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c34[0])
                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c34[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c4[0]
                                fv_xyz_out[1] += fv_xyz_center_c4[1]
                                fv_xyz_out[2] += fv_xyz_center_c4[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c3[0]
                                fv_xyz_out[1] += fv_xyz_center_c3[1]
                                fv_xyz_out[2] += fv_xyz_center_c3[2]

                else :
                    for i in range(3) :
                    #    fv_xyz_out[i] += fv_xyz_c34[0][i]
                        fv_xyz_out[i] += 0

                if(ret41 == 0) :
                    #c4 - c1
                    ch = self.check_pnt_in_quad( fv_xyz_c41[0], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                    if( ch == 0 ) :
                        for i in range(3) :
                            fv_xyz_out[i] += fv_xyz_c41[0][i]

                    else :
                        ch = self.check_pnt_in_quad( fv_xyz_c41[1], fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                        if(ch == 0) :
                            for i in range(3) :
                                fv_xyz_out[i] += fv_xyz_c41[1][i]
                        else :
                            #C3 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c41[0])
                            fv1 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c4, fv_xyz_c41[1])
                            fv1 += self.VtA3Dot( fv, fv )

                            #C4 point intersection distance sum
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c41[0])

                            fv2 = self.VtA3Dot( fv, fv )
                            fv = self.VtA3Sub( fv_xyz_center_c1, fv_xyz_c41[1])
                            fv2 += self.VtA3Dot( fv, fv )

                            if(fv2 < fv1) :
                                fv_xyz_out[0] += fv_xyz_center_c1[0]
                                fv_xyz_out[1] += fv_xyz_center_c1[1]
                                fv_xyz_out[2] += fv_xyz_center_c1[2]
                            else :
                                fv_xyz_out[0] += fv_xyz_center_c4[0]
                                fv_xyz_out[1] += fv_xyz_center_c4[1]
                                fv_xyz_out[2] += fv_xyz_center_c4[2]

                else :
                    for i in range(3) :
                        #fv_xyz_out[i] += fv_xyz_c41[0][i]
                        fv_xyz_out[i] += 0


            #=============================================================
            print(fv_xyz_out, count_xyz)
            #final x,y,x transfer

            if(count_xyz > 0) :
                for i in range(3) :
                    fv_xyz_out[i] /= count_xyz  #4.0

                ch = self.check_pnt_in_quad( fv_xyz_out, fv_xyz_center_c1, fv_xyz_center_c2, fv_xyz_center_c3, fv_xyz_center_c4, area_tri_123, area_tri_134, fv_tol )
                #print(fv_xyz_out, ch, ret0)
                if(ch == 0) :
                    return (ret0, fv_xyz_out)
            else :
                fv_xyz_out[0] = 0
                fv_xyz_out[1] = 0
                fv_xyz_out[2] = 0
                return (ret0, fv_xyz_out)

            #================================================

        except :
            print("get_4circle_intersection_coord Error!!!")

    def get_circle_intersection_coord(self,iv_num_circle,fv_xyz_center,fv_radius_circle,fv_tol) :
        # how-to : (iv_num_pnt, fv_xyz_out) = get_circle_intersection_coord(...)
        try :

            #print('get_circle_intersection_coord start')
            if( (iv_num_circle < 3) or (iv_num_circle > 4) ) :
                # 3 or 4 date normal
                return -1

            #print('=================1================')
            #print(fv_tol)
            #print(self.FV_ZERO)
            #print(iv_num_circle)

            if( fv_tol <= self.FV_ZERO ) :  #tolerance
                if( iv_num_circle == 3 ) :
                    f1 = self.VtMin( self.VtMin( fv_radius_circle[0], fv_radius_circle[1] ), fv_radius_circle[2] )
                    #print(f1)
                elif( iv_num_circle == 4 ) :
                    f1 = self.VtMin( self.VtMin( self.VtMin( fv_radius_circle[0], fv_radius_circle[1] ), fv_radius_circle[2] ), fv_radius_circle[3] )
                else :
                    return -1

                if( f1 <= self.FV_ZERO ) :
                    fv_tol = self.INIT_TOL
                else :
                    fv_tol = f1 / 100.0

                #print(fv_tol)

            fv_center_c1 = [0,0,0]
            fv_center_c2 = [0,0,0]

            fv_center_c3 = [0,0,0]
            fv_center_c4 = [0,0,0]

            fv_center_c1[0] = fv_xyz_center[0]
            fv_center_c1[1] = fv_xyz_center[1]
            fv_center_c1[2] = fv_xyz_center[2]

            fv_center_c2[0] = fv_xyz_center[3]
            fv_center_c2[1] = fv_xyz_center[4]
            fv_center_c2[2] = fv_xyz_center[5]

            fv_center_c3[0] = fv_xyz_center[6]
            fv_center_c3[1] = fv_xyz_center[7]
            fv_center_c3[2] = fv_xyz_center[8]

            fv_D1 = fv_radius_circle[0]
            fv_D2 = fv_radius_circle[1]
            fv_D3 = fv_radius_circle[2]
            fv_D4 = fv_radius_circle[3]

            fv_xyz_out = [0,0,0]
            fv_xyz = [0,0,0]

            if( iv_num_circle == 3 ) :

                (ret, fv_xyz) = self.get_3circle_intersection_coord( fv_center_c1, fv_center_c2, fv_center_c3, fv_D1, fv_D2, fv_D3, fv_tol );

                if( ret == 0 ) :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 3 circle')
                    return (ret, fv_xyz_out)
                else :
                    if( iv_num_circle == 3 ) :
                        return (ret, fv_xyz_out)

            elif( iv_num_circle == 4 ) :
                fv_xyz_out_1 = [0,0,0]

                fv_center_c4[0] = fv_xyz_center[9];
                fv_center_c4[1] = fv_xyz_center[10];
                fv_center_c4[2] = fv_xyz_center[11];


                (ret, fv_xyz) = self.get_4circle_intersection_coord( fv_center_c1, fv_center_c2, fv_center_c3, fv_center_c4, fv_D1, fv_D2, fv_D3, fv_D4, fv_tol );

                if( ret == 0 ) :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 4 circle')

                    print('4/first:', fv_xyz_out)

                elif( ret < 0) :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 4 circle')
                    print('4/Error:', fv_xyz_out)

                else :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 4 circle')
                    print('4/over:', fv_xyz_out)

                return (ret, fv_xyz_out)

            return -1

        except :
            print("get_circle_intersection_coord Error!!!")

    def get_circle_intersection_coord_4(self,iv_num_circle,fv_xyz_center,fv_radius_circle,fv_tol) :
        # how-to : (iv_num_pnt, fv_xyz_out) = get_circle_intersection_coord(...)
        try :

            #print('get_circle_intersection_coord start')
            if( (iv_num_circle < 3) or (iv_num_circle > 4) ) :
                # 3 or 4 date normal
                return -1

            #print('=================1================')
            #print(fv_tol)
            #print(self.FV_ZERO)
            #print(iv_num_circle)

            if( fv_tol <= self.FV_ZERO ) :  #tolerance
                if( iv_num_circle == 3 ) :
                    f1 = self.VtMin( self.VtMin( fv_radius_circle[0], fv_radius_circle[1] ), fv_radius_circle[2] )
                    #print(f1)
                elif( iv_num_circle == 4 ) :
                    f1 = self.VtMin( self.VtMin( self.VtMin( fv_radius_circle[0], fv_radius_circle[1] ), fv_radius_circle[2] ), fv_radius_circle[3] )
                else :
                    return -1

                if( f1 <= self.FV_ZERO ) :
                    fv_tol = self.INIT_TOL
                else :
                    fv_tol = f1 / 100.0

                #print(fv_tol)

            fv_center_c1 = [0,0,0]
            fv_center_c2 = [0,0,0]

            fv_center_c3 = [0,0,0]
            fv_center_c4 = [0,0,0]

            fv_center_c1[0] = fv_xyz_center[0]
            fv_center_c1[1] = fv_xyz_center[1]
            fv_center_c1[2] = fv_xyz_center[2]

            fv_center_c2[0] = fv_xyz_center[3]
            fv_center_c2[1] = fv_xyz_center[4]
            fv_center_c2[2] = fv_xyz_center[5]

            fv_center_c3[0] = fv_xyz_center[6]
            fv_center_c3[1] = fv_xyz_center[7]
            fv_center_c3[2] = fv_xyz_center[8]

            fv_D1 = fv_radius_circle[0]
            fv_D2 = fv_radius_circle[1]
            fv_D3 = fv_radius_circle[2]
            fv_D4 = fv_radius_circle[3]

            fv_xyz_out = [0,0,0]
            fv_xyz = [0,0,0]

            if( iv_num_circle == 3 ) :

                (ret, fv_xyz) = self.get_3circle_intersection_coord( fv_center_c1, fv_center_c2, fv_center_c3, fv_D1, fv_D2, fv_D3, fv_tol );

                if( ret == 0 ) :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 3 circle')
                    return (ret, fv_xyz_out)
                else :
                    if( iv_num_circle == 3 ) :
                        return (ret, fv_xyz_out)

            elif( iv_num_circle == 4 ) :
                fv_xyz_out_1 = [0,0,0]

                fv_center_c4[0] = fv_xyz_center[9];
                fv_center_c4[1] = fv_xyz_center[10];
                fv_center_c4[2] = fv_xyz_center[11];


                (ret, fv_xyz) = self.get_4circle_intersection_coord_4( fv_center_c1, fv_center_c2, fv_center_c3, fv_center_c4, fv_D1, fv_D2, fv_D3, fv_D4, fv_tol );

                if( ret == 0 ) :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 4 circle')

                    print('4/first:', fv_xyz_out)

                elif( ret < 0) :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 4 circle')
                    print('4/Error:', fv_xyz_out)

                else :
                    fv_xyz_out[0] = fv_xyz[0]
                    fv_xyz_out[1] = fv_xyz[1]
                    fv_xyz_out[2] = fv_xyz[2]
                    #print('get_circle_intersection_coord - 4 circle')
                    print('4/over:', fv_xyz_out)

                return (ret, fv_xyz_out)

            return -1

        except :
            print("get_circle_intersection_coord Error!!!")
#====================================================================================
# main Function
#------------------------------------------------------------------------------------

def main() :

        try :
            print("==========================================================")
            print("       [ Circle intersection ] Ver 1.00 - BLE Scanner                 ")
            print("==========================================================")


            loop_delay_time = 5 # 1 minute delay

            CI = CircleIntersectClass()

            #while(1) :
            if(1) :
                print('***************** Start Circle Intersection **********************')
                #print(CI.PHI)
                a = [1,2,3]
                b = [4,5,6]
                result = []
                k = 2
                result = CI.VtA3Copy(a)
                print(a)
                print(b)
                print(result)

                p1 = [0.0, 0.0, 0.0]
                p2 = [100.0, 0.0, 0.0]
                p3 = [80.0, 50.0, 0.0]

                pnt = [100, 20, 0]

                ret = CI.TriArea(p1, p2, p3)
                print(p1)
                print(p2)
                print(p3)
                print(ret)
                fv_tol = CI.INIT_TOL
                ret = CI.check_pnt_in_tri(pnt, p1, p2, p3, ret, fv_tol)
                if(ret == 0) :
                    print('Internal circle')
                else :
                    print('External circle')
                print(ret)

                w, h = 4, 4
                m = [[2 for x in range(w)] for y in range(h)]     #inv matrix 4x4 create
                m[2][3] = -1

                print(m)
                inv = CI.VmMatGetInvXform(m)
                print(inv)

                # 3 point coordination x, y, z
                fv_xyz_center = []

                fv_xyz_center.append(0.0)
                fv_xyz_center.append(0.0)
                fv_xyz_center.append(0.0)

                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(0.0)
                fv_xyz_center.append(0.0)

                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(0.0)

                fv_xyz_center.append(0.0)
                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(0.0)

                fv_radius_circle = []
                fv_radius_circle.append(2386.0)
                fv_radius_circle.append(774.0)
                fv_radius_circle.append(950.0)
                fv_radius_circle.append(1165.0)

                iv_num_circle = 4
                print(inv)

                # 3 point coordination x, y, z
                fv_xyz_center = []

                fv_xyz_center.append(0.0)
                fv_xyz_center.append(0.0)
                fv_xyz_center.append(0.0)

                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(0.0)
                fv_xyz_center.append(0.0)

                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(0.0)

                fv_xyz_center.append(0.0)
                fv_xyz_center.append(3000.0)
                fv_xyz_center.append(0.0)

                fv_radius_circle = []
                fv_radius_circle.append(2386.0)
                fv_radius_circle.append(774.0)
                fv_radius_circle.append(950.0)
                fv_radius_circle.append(1165.0)

                iv_num_circle = 4

                fv_tol=0.0

                print('3 coord start')
                print(fv_xyz_center)
                print(fv_radius_circle)

                (ret, fv_xyz_out) = CI.get_circle_intersection_coord( iv_num_circle,fv_xyz_center,fv_radius_circle,fv_tol)

                print('ret :',ret)
                print('fv_xyz_out :', fv_xyz_out)


        except :
                print("!!!!!!!!!!!!!!!Circle Intersection Main Error!!!!!!!!!!!!!")

#======================================

if __name__ == '__main__' :

        try :
                main()
        except KeyboardInterrupt :
                print("Circle Intersection END")


