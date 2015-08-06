#!/usr/bin/env python
import re, os, shutil, sys
import numpy as np
#
errStatus0 = "enter complete file path"
#
if len(sys.argv)==2:
	filePath = sys.argv[1] #os.chdir("../accuracyAccess/errorMat.txt")
	print filePath
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
	fName = "output.txt"
	curPath = os.getcwd()
	print ("writing output to \n %s/%s")%(curPath,fName)	
	fName = open(fName, 'w')
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
		fName.write("User Inputs \n 1) Area Distribution \n")
		np.savetxt(fName, areaArray, delimiter=',', fmt='%1.4f')
		#fName.write(areaArray)
		print (areaArray)
		totalArea = areaArray.sum()
		errorMat = np.asarray(errorMat, dtype=np.float32)
		fName.write("\n 2) Confustion matrix \n")		
		np.savetxt(fName, errorMat, delimiter=',', fmt='%1.4f')
		print(errorMat)
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
		#print ("pij \n %s")%(pij)
		fName.write("\n Analysis Output \n 1) Matrix p(ij) \n")
		np.savetxt(fName, pij, delimiter=',', fmt='%1.4f')		
		#print ("ni \n %s")%(ni)
		fName.write("\n 2) Number of samples / observations n(i) \n")
		np.savetxt(fName, ni, delimiter=',', fmt='%1.4f')		
		#print ("wi \n %s")%(wi)
		fName.write("\n 3) Weight values Wi \n")
		np.savetxt(fName, wi, delimiter=',', fmt='%1.4f')
		SD = []
		for i in range (0,(len(pij))):
			ss = ((pij[:,i]*wi-(pij[:,i]*pij[:,i]))/(ni))
			ss = np.sqrt(ss.sum())
			SD.append(ss)
		#
		SD = np.asarray(SD, dtype=np.float32)
		fName.write("\n 4) Standard Error (SE) \n")
		np.savetxt(fName, SD, delimiter=',', fmt='%1.4f')
		#print ("Standard Error = %s")%(SD)
		SdPix = SD* np.asarray(totalArea, dtype=np.float32)
		fName.write("\n 5) Standard Error in [ px ] \n")
		np.savetxt(fName, SdPix, delimiter=',', fmt='%1.4f')
		#print ("Standard Error in [ px ] = %s")%(SdPix)
		SdInHa = ((SdPix * np.asarray(pixConv, dtype=np.float32))/np.asarray(haConv, dtype=np.float32))
		#print ("Standard Error in [ ha ] = %s")%(SdInHa)
		fName.write("\n 6) Standard Error in [ ha ] \n")
		np.savetxt(fName, SdInHa, delimiter=',', fmt='%1.4f')
		# for 95 % confidence interval 1.98
		CiVal = 1.98
		ConfInt = SdInHa * np.asarray(CiVal, dtype=np.float32)
		#print ("95 CI in [ ha ] = %s")%(ConfInt)
		fName.write("\n 7) Constant for 95 percent Confidence Interval (CI) = ")
		valC = ("%s")%(CiVal)
		fName.write(valC)
		fName.write("\n \n 8) CI in [ ha ] \n")
		np.savetxt(fName, ConfInt, delimiter=',', fmt='%1.4f')
		#-------------------------------------------------
		# Margin of error
		MoE = (ConfInt / areaHa)
		#print ("Margin of Error = %s")%(MoE)
		fName.write("\n 9) Margin of Error (MoE) \n  \n")
		np.savetxt(fName, MoE, delimiter=',', fmt='%1.4f')
		MoEPerCent = MoE* np.asarray(100, dtype=np.float32)
		#print ("Margin of Error in Percent = %s")%(MoEPerCent)
		fName.write("\n 10) MoE in [ percent ] \n  \n")
		np.savetxt(fName, MoEPerCent, delimiter=',', fmt='%1.4f')
		#-------------------------------------------------
		# Overall Accuracy
		OverallA = np.diag(pij)
		OverallA = OverallA.sum()
		#print ("Overal accuracy = %s")%(OverallA)
		fName.write("\n 11) Overall accuracy \n  \n")
		ov = ("%s")%(OverallA)		
		fName.write(ov)
		#-------------------------------------------------
		# User's accuracy
		UAccuracy = (np.diag(pij)/wi)
		#print ("User's accuracy = %s")%(UAccuracy)
		fName.write("\n 12) User's accuracy \n  \n")
		np.savetxt(fName, UAccuracy, delimiter=',', fmt='%1.4f')
		#-------------------------------------------------
		# Producers's accuracy
		ProdAccuracy = (np.diag(pij)/erroRowSum)
		#print("Producers Accuracy = \n %s")%(ProdAccuracy)
		fName.write("\n 13) Producers Accuracy \n  \n")
		np.savetxt(fName, ProdAccuracy, delimiter=',', fmt='%1.4f')
		#-------------------------------------------------
		fName.close()
		#
	else:
		print (check)
# Implementation
analyzeAccuracy(filePath)

