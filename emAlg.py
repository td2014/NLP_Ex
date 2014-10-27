#!/usr/bin/python
#
# Routine to implement the EM algorithm for the
# NLP assignment #3.
#
# 

import pickle

def emAlg(model, trainingCorpusEnglish, trainingCorpusForeign, numIter, outputFileForT, fileAlignEnglish, fileAlignForeign, fileAlign):

#
# Echo back params
#

   print "emAlg:"
   print "model = ", model
   print "trainingCorpusEnglish = ", trainingCorpusEnglish
   print "trainingCorpusForeign = ", trainingCorpusForeign
   print "numIter = ", numIter
   print "outputFileForT = ", outputFileForT
   print "fileAlignEnglish = ", fileAlignEnglish
   print "fileAlignForeign = ", fileAlignForeign
   print "fileAlign = ", fileAlign
   print ""

#
# open the training files
#

   fileEnglish = open(trainingCorpusEnglish, "r")
   fileForeign = open(trainingCorpusForeign, "r")

   if (model==1):
      fileOutputT = open(outputFileForT, "w")
   elif (model==2 or model==3):
      print "need to read in t values for model 2"
      tempDict = {}
      tempDict = pickle.load(open(outputFileForT,"r"))
   else:
      print "emAlg:  Error - model can only be integers 1 or 2"
      return

#
# Preread one of the files to get a line count
#

   tempEnglish = fileEnglish.readlines()
   tempForeign = fileForeign.readlines()
   numSent = len(tempEnglish)

   print "emAlg: numSentences = ", numSent  

#
# Initialize the parameters
#
   
   englishWordList = []

#
# Sparse map
#

   sparseTMap = {}
   qVal = {}
   countsJILM = {}
   countsILM = {}


   for k in range(1, numSent+1):

#
# read in a sentence from each corpus:
#
# insert a NULL in the first position.
#
      tempEnglish[k-1] = "*NULL* " + tempEnglish[k-1]      
      currEnglishString = tempEnglish[k-1] 
      currForeignString = tempForeign[k-1] 
      currEnglishStringSplit = currEnglishString.split()
      currForeignStringSplit = currForeignString.split() 

#
# Insert *NULL* as the first symbol in each english sentence.
#

      l = len(currEnglishStringSplit)-1
      m = len(currForeignStringSplit)

      print "k = ", k
      print "len(qVal) = ", len(qVal)
      print "len(countsJILM) = ", len(countsJILM)
#      print "currEnglishString = ", currEnglishString
#      print "currForeignString = ", currForeignString
#      print "numEnglishWords = ", l
#      print "numForeignWords = ", m

#
# By doing this way, we keep track of the english words we have already encountered
# so we don't double add
#
      for j in range(0, l+1):
         if (model==1):
            try:
               englishWordList.index(currEnglishStringSplit[j])
            except:
               sparseTMap[currEnglishStringSplit[j]] = {}
               englishWordList.append(currEnglishStringSplit[j])

#
# Now scan in the current foreign word list
#
 
         fDict = {}
         foreignWordList = []

         for i in range(1, m+1):
            if (model == 1):
               fDict[currForeignStringSplit[i-1]] = 0.0
            qEncode = str(j) + "_"  + str(i) + "_" + str(l) + "_"  + str(m)
            cEncode = str(i) + "_" + str(l) + "_" + str(m)
            qVal[qEncode] = 1.0/float(l+1)
            countsJILM[qEncode] = 0
            countsILM[cEncode] = 0
###            print "emAlg: qEncode = ", qEncode
###            print "emAlg: len(qVal) = ", len(qVal)
###            print "emAlg: len(countsJILM) = ", len(countsJILM)
###            print "emAlg: len(countsILM) = ", len(countsILM)
###            print "emAlg: cEncode = ", cEncode

#
# Assign the last j indexed qVal.  j won't reach it.
#

###            if (j==l-1):
###               qEncode = str(j+1) + "_"  + str(i) + "_" + str(l) + "_"  + str(m)
###               qVal[qEncode] = 1.0/float(l+1)
###               countsJILM[qEncode] = 0

###               print "emAlg: final j assignment:"
###               print "emAlg: qEncode = ", qEncode
###               print "emAlg: len(qVal) = ", len(qVal) 

         if (model==1):
            sparseTMap[currEnglishStringSplit[j]].update(fDict) 

#
# Now scan in the corresponding foreign word list (watch out for duplicates
#


###      print "EnglishWords: ", englishWordList
###      print "ForeignWords: ", foreignWordList
 

###   print "sparseTMap[this] = ", sparseTMap['this']


#
# Now initialize t(f|e) = 1/n(e)
#

###   print "sparseTMap[this][asees]", sparseTMap['this']['asees']   

###   print "pre T initialization:"
   if (model==1): 
      for eWord, fWordList in sparseTMap.iteritems():
###      print sparseTMap[eWord], len(fWordList) 
         for fWord, fVal in sparseTMap[eWord].iteritems():
###         print "fWord, fVal: ", fWord, fVal
###         print "sparseTMap eWord fWord = ", sparseTMap[eWord][fWord]
            sparseTMap[eWord][fWord] = 1.0/len(fWordList)

#
# If doing model 2, then use pre-computed/loaded t
#

   if (model==2 or model==3):
      sparseTMap = {}
      sparseTMap = tempDict 

###
### Post initialization test dump:
###
###   for eWord, fWordList in sparseTMap.iteritems():
###      print eWord, fWordList 
###

# Now do the main EM processing
#

   for s in range(1,numIter+1):

      print "iter = ", s

#
# Set the counters to zero
# May as well sparse maps for these as well
#
#
      countsEF = {}
      countsE  = {}

      for eWord, fWordList in sparseTMap.iteritems():
         countsEF[eWord]= {}
         for fWord, fVal in sparseTMap[eWord].iteritems():
            countsEF[eWord][fWord] = 0
            countsE[eWord] = 0

###      print "countsE:", countsE
###      print "countsEF:", countsEF

###
### Post initialization test dump:
###
###   for eWord, fWordList in sparseTMap.iteritems():
###      print eWord, fWordList 
###

      for k in range(1, numSent+1):

         print "EMLoop: iter, sentence = ", s, k
#
# read in a sentence from each corpus:
#
# m is associated with foreign sentences
# l is associated with english sentences 
#

         currEnglishString = tempEnglish[k-1] 
         currForeignString = tempForeign[k-1] 
         currEnglishStringSplit = currEnglishString.split()
         currForeignStringSplit = currForeignString.split() 
         l = len(currEnglishStringSplit)-1
         m = len(currForeignStringSplit)

###         print "k = ", k
###         print "currEnglishString = ", currEnglishString
###         print "currForeignString = ", currForeignString
###         print "numEnglishWords = ", l
###         print "numForeignWords = ", m

#
# Now the inner most loop
#

         for i in range(1, m+1):
            currFWord = currForeignStringSplit[i-1]

            for j in range(0, l+1):
               currEWord = currEnglishStringSplit[j]
              
               qTemp = 1.0 
               
               if (model==2): 
                  qEncode = str(j) + "_"  + str(i) + "_" + str(l) + "_"  + str(m)
                  cEncode = str(i) + "_" + str(l) + "_" + str(m)
                  qTemp = qVal[qEncode]

               deltaNum = sparseTMap[currEWord][currFWord]*qTemp
               deltaDen = 0.0 
               
               for jj in range(0,l+1):
                  tempEWord = currEnglishStringSplit[jj]

                  qTemp = 1.0

                  if (model==2):
                     qEncodeInner = str(jj) + "_"  + str(i) + "_" + str(l) + "_"  + str(m)
                     qTemp = qVal[qEncodeInner] 

                  deltaDen = deltaDen + sparseTMap[tempEWord][currFWord]*qTemp 

               delta = float(deltaNum)/float(deltaDen)  

               countsEF[currEWord][currFWord] = countsEF[currEWord][currFWord] + delta
               countsE[currEWord] = countsE[currEWord] + delta
               if (model==2):
                  countsJILM[qEncode] = countsJILM[qEncode] + delta
                  countsILM[cEncode] = countsILM[cEncode] + delta

#
# Compute the update t(f|e)
#         t(f|e) = counts(e,f)/counts(e)
#         qVal = countsJILM(j|i,l,m)/countsILM(i,l,m)
#    

      for eWord, fWordList in sparseTMap.iteritems():
###      print sparseTMap[eWord], len(fWordList) 
         for fWord, fVal in sparseTMap[eWord].iteritems():
###         print "fWord, fVal: ", fWord, fVal
###         print "sparseTMap eWord fWord = ", sparseTMap[eWord][fWord]
            stmNum = countsEF[eWord][fWord]
            stmDen = countsE[eWord]
            sparseTMap[eWord][fWord] = float(stmNum)/float(stmDen)

      if (model==2):
###         print "emAlg: qVal update"
         for qEncode,qValTemp in qVal.iteritems():
###            print "emAlg: qEncode update = ", qEncode
            qValNum = countsJILM[qEncode]
            cEncodeSplit = str(qEncode).split("_")
            cEncode = cEncodeSplit[1] + "_" + cEncodeSplit[2] + "_" + cEncodeSplit[3]
###            print "emAlg: cEncode after split = ", cEncode
            qValDen = countsILM[cEncode]

            qVal[qEncode] = float(qValNum)/float(qValDen)        

#
# Output t(f|e) and q(jilm)
#
# We can output t(f|e) as a dictionary
# key, value
#
# key = foreign word, value = tValue
#

   if (model==1):
      pickle.dump(sparseTMap, fileOutputT)
      fileOutputT.close()

   fileEnglish.close()
   fileForeign.close()

#
# Now find the best alignment for each sentence in the 
# inputCorpus, and dump out in the format described in the homework.
#
# a_i = arg (j) that produces max t(f_i | e_j).
# i.e. loop over each foreign word in the test sentence,
# and then find the english word that produces the highest t(f_i, e_j)
# and dump out it position.
#

   inFileAlignEnglish = open(fileAlignEnglish, 'r')
   inFileAlignForeign = open(fileAlignForeign, 'r')
   outFileAlign = open(fileAlign,'w')

   tempAlignEnglish = inFileAlignEnglish.readlines()
   tempAlignForeign = inFileAlignForeign.readlines()
   numSent = len(tempAlignEnglish)

   for k in range(1,numSent+1):

      print "k: in test corpus = ", k

      tempAlignEnglish[k-1] = "*NULL* " + tempAlignEnglish[k-1]
      currAlignEnglishString = tempAlignEnglish[k-1]
      currAlignForeignString = tempAlignForeign[k-1]
      currAlignEnglishStringSplit = currAlignEnglishString.split()
      currAlignForeignStringSplit = currAlignForeignString.split()

      l = len(currAlignEnglishStringSplit)-1
      m = len(currAlignForeignStringSplit)

      for i in range (1, m+1):
         maxT = 0.0
         maxA = 0
         currFWord = currAlignForeignStringSplit[i-1]
         for j in range (0, l+1):
            currEWord = currAlignEnglishStringSplit[j]

            qTemp = 1.0
            if (model==2):
               print "emAlg: Alignment Max:"
               qEncode = str(j) + "_"  + str(i) + "_" + str(l) + "_"  + str(m)
               qTemp = qVal[qEncode]

            currT = sparseTMap[currEWord][currFWord]*qTemp

            if (currT >= maxT):
               maxT = currT
               maxA = j

         outFileAlign.write(str(k) + " " + str(maxA) + " " + str(i) + "\n")


#
# Clean up and return
#

   inFileAlignEnglish.close() 
   inFileAlignForeign.close()
   outFileAlign.close()
  

#
# End of program
#
