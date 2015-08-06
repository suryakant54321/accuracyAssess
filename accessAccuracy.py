#!/usr/bin/env python
import re, os, shutil, sys
import numpy as np
#
errStatus0 = "enter complete file path"
#
if len(sys.argv)==2:
	filePath = sys.argv[1] #os.chdir("../accuracyAccess/errorMat.txt")
else:
	print errStatus0
# Check errors in input file
errStatus = "Problem with input text file \n recheck the input again \n Suggested format comma seperated values : \n First line number of pixels for each class \n Next lines error matrix. "
def checkErrors(areaArray, errorMat):
	status = "TRUE"	
	if(len(areaArray)==len(errorMat)):
		status = "TRUE"
	else:
		status = errStatus 
	return status
# main
def analyzeAccuracy(filePath):
	areaArray = []
	errorMat = []
	count = 0
	for i in open(filePath):
		row = re.split(',',i)
		row[-1] = row[-1].rstrip('\n')
		if (count == 0):
			areaArray = row
		else:
			errorMat.append(row)
		count = count + 1
	try:	
		areaArray = np.asarray(areaArray, dtype=np.float32)
		#print "area array"
		#print areaArray
		totalArea = areaArray.sum()
		#print "error array"
		errorMat = np.asarray(errorMat, dtype=np.float32)
		#print errorMat
	except:
		print errStatus
	# Check the errors in user input
	check = checkErrors(areaArray, errorMat)
	if (check=="TRUE"):
		# 
		rowSum = []
		colSum = []
		for i in range (0,(len(errorMat))):
			rowSum.append(errorMat[i,:].sum())
			colSum.append(errorMat[:,i].sum())
		#
		rowSum = np.asarray(rowSum, dtype=np.float32)
		colSum = np.asarray(colSum, dtype=np.float32)
		#print ("Total Area [in px] = %s")%(totalArea) 
		#print ("Sum of each Row = %s")%(rowSum)
		#print ("Sum of each Column = %s")%(colSum)
		# -- fun begins
		wi = areaArray/totalArea
		wiPerCent = wi*100
		#print ("Wi = %s")%(wi)
		#print ("Wi (in percent)= %s")%(wiPerCent)
		#-------------------------------------------------
		# To do 
		# estimate sample size for each class
		#-------------------------------------------------
		# Error Matrix estiamted area proportions
		erMatEAP = []
		for i in range (0,(len(errorMat))):
			erMatEAP.append((errorMat[i,]*wi[i])/rowSum[i])
		erMatEAP = np.asarray(erMatEAP, dtype=np.float32)
		#print ("Error Matrix estiamted area proportions")
		#print (erMatEAP)
		# 
		erroRowSum = []
		errorColSum = []
		for i in range (0,(len(erMatEAP))):
			errorColSum.append(erMatEAP[i,:].sum())
			erroRowSum.append(erMatEAP[:,i].sum())
		# 
		#print ("error Column \n %s")%(errorColSum)
		#print ("error Row Area ^ \n %s ")%(erroRowSum)

		areaPix = (erroRowSum * np.asarray(totalArea, dtype=np.float32))
		#print ("Area pix %s")%(areaPix)
		haConv = (100*100)
		pixConv = (30*30)
		areaHa = ((areaPix * np.asarray(pixConv, dtype=np.float32))/np.asarray(haConv, dtype=np.float32))
		#print ("Area in ha %s")%(areaHa)
		# 
		pij = erMatEAP
		ni = rowSum
		# pij	
		# ni	
		# wi	
		print ("pij \n %s")%(pij)
		print ("ni \n %s")%(ni)
		print ("wi \n %s")%(wi)
		SD = []
		for i in range (0,(len(pij))):
			#print (pij[:,i])
			#print (wi)
			#print (ni)
			ss = ((pij[:,i]*wi-(pij[:,i]*pij[:,i]))/(ni))
			ss = np.sqrt(ss.sum())
			SD.append(ss)
		#
		#some = np.asarray(some, dtype=np.float32))
		print ("Standard Error = %s")%(SD)
		SdPix = SD* np.asarray(totalArea, dtype=np.float32)
		print ("Standard Error in [ px ] = %s")%(SdPix)
		SdInHa = ((SdPix * np.asarray(pixConv, dtype=np.float32))/np.asarray(haConv, dtype=np.float32))
		print ("Standard Error in [ ha ] = %s")%(SdInHa)
		# for 95 % confidence interval 1.98
		CiVal = 1.98
		ConfInt = SdInHa * np.asarray(CiVal, dtype=np.float32)
		print ("95 CI in [ ha ] = %s")%(ConfInt)
		#-------------------------------------------------
		# Margin of error
		MoE = (ConfInt / areaHa)
		print ("Margin of Error = %s")%(MoE)
		MoEPerCent = MoE* np.asarray(100, dtype=np.float32)
		print ("Margin of Error in Percent = %s")%(MoEPerCent)

		#-------------------------------------------------
		# Overall Accuracy
		OverallA = np.diag(pij)
		OverallA = OverallA.sum()
		print ("Overal accuracy = %s")%(OverallA)
		#-------------------------------------------------
		# User's accuracy
		UAccuracy = (np.diag(pij)/wi)
		print ("User's accuracy = %s")%(UAccuracy)
		#-------------------------------------------------
		# Producers's accuracy
		ProdAccuracy = (np.diag(pij)/erroRowSum)
		print("Producers Accuracy = \n %s")%(ProdAccuracy)
		#-------------------------------------------------
		# to do Write result to the file 
		#
	else:
		print (check)
# Implementation
analyzeAccuracy(filePath)

