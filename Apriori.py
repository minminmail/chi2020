  #** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
  # This file is part of KEEL - software, the Data Mining tool
  # for regression, classification, clustering, pattern  mining and so  on.

  # Copyright(C) 2004 - 2010

#     F.Herrera(herrera @ decsai.ugr.es)
#     L.SÃ¡nchez(luciano @ uniovi.es)
#     J.AlcalÃ¡-Fdez(jalcala @ decsai.ugr.es)
#     S.GarcÃ­a(sglopez @ ujaen.es)
#     A.FernÃ¡ndez(alberto.fernandez @ ujaen.es)
#     J.Luengo(julianlm @ decsai.ugr.es)
#
#     This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see http://www.gnu.org/licenses/
#
#
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
from main.Item import Item
from main.RuleBase import RuleBase


import gc

# /**
#  * <p>Title: Apriori</p>
#  * <p>Description: This class mines the frecuent fuzzy itemsets and the fuzzy classification associacion rules</p>
#  * <p>Copyright: Copyright KEEL (c) 2007</p>
#  * <p>Company: KEEL </p>
#  * @author Written by Jesus Alcala (University of Granada) 09/02/2011
#  * @version 1.0
#  * @since JDK1.6
#  */

class Apriori :
    # ArrayList < Itemset > L2;
    L2 = []
    # double
    minsup = None
    minconf = None

    minSupps = None   # double[]
    # int
    nClasses = None
    nVariables = None
    depth = None

    ruleStage1= None #long
    ruleBase = None   #RuleBase
    ruleBaseClase = None #RuleBase
    train = None   # myDataset
    dataBase = None  # DataBase

  #  **
  #  *Default  Constructor.
  #  *


    def __init__(self):
      print("__init__ of Apriori")

    # / **
    # * Builder
    # * @ param ruleBase Rule base
    # * @ param dataBase Data Base
    # * @ param train Training dataset
    # * @ param minsup Minimum support.
    # * @ param minconf Maximum Confidence.
    # * @ param depth Depth of the trees (Depthmax)
    # * /

    def multiple_init(self,ruleBase, dataBase,  train,  minsup,  minconf,  depth):
        self.train = train
        self.dataBase = dataBase
        self.ruleBase = ruleBase
        self.minconf = minconf
        self.depth = depth
        self.nClasses = self.train.getnClasses()
        self.nVariables = self.train.getnInputs()

        self.L2 = []
        minSupps = [None] * self.nClasses
        for i in range (0, self.nClasses):
            minSupps[i] = self.train.frecuentClass(i) * minsup


    # / **
    # * Generate the rule set (Stage 1 and 2)
    # * /

    def generateRB (self) :
        # int
        i= None
        j = None
        uncover =  None
        ruleStage1 = 0

        self.ruleBaseClase = RuleBase(self.dataBase, self.train, self.ruleBase.getK(), self.ruleBase.getTypeInference())

        for i in range (0, self.nClasses) :
            self.minsup = self.minSupps[i]
            self.generateL2(i)
            self.generateLarge (self.L2, i)

            self.ruleBaseClase.reduceRules(i)

            self.ruleBase.add(self.ruleBaseClase)
            self.ruleBaseClase.clear()
            gc.collect()



    def generateL2(self, clas):
        int
        i = None
        j = None
        k = None
        uncover = None
        item = None
        itemset = None

        self.L2.clear()
        itemset = [Itemset for i in range(clas)]

        for i in range(0, i < self.nVariables):
            if self.dataBase.numLabels(i) > 1:
                for j in range(0, j < self.dataBase.numLabels(i)):
                    item = Item(i, j)
                    itemset.add(item)
                    itemset.calculateSupports(self.dataBase, self.train);
                    if itemset.getSupportClass() >= self.minsup :
                        self.L2.add(itemset.clone())
                    itemset.remove(0)
         self.generateRules(self.L2, clas)

        '''
         * Indentifies how many times a class has been uncovered.
         * @param clas Class given to compute the number of times.
         * @return number of times that class has been uncovered.
        '''

    def  hasUncoverClass(self, clas):
        int
        uncover = None
        degree = None
        itemset = None
        stop =None

        uncover = 0
        for j in range(0 ,self.train.size()) :
            if self.train.getOutputAsInteger(j) == clas:
                stop = False
                for i in range (0,self.L2.size()) :
                    if not stop:
                        itemset = self.L2.get(i)
                        degree = itemset.degree(self.dataBase, self.train.getExample(j))
                        if degree > 0.0 :
                            stop = True

                if not stop:
                    uncover = uncover + 1


	return uncover


    def generateLarge (self, Lk, clas):
        # int
        i = None
        j =  None
        size=  None
        Lnew = []
        newItemset =  None
        itemseti =  None
        itemsetj =  None

        size = Lk.size()

        if size > 1:
            if (((Lk.get(0)).size() < self.nVariables) and ((Lk.get(0)).size() < self.depth)):
                  Lnew = [ ]
                  for i in range(0,size-1) :
                      itemseti = Lk.get(i)
                      for j in range( i+1, j < size) :
                          itemsetj = Lk.get(j)
                          if self.isCombinable(itemseti, itemsetj):
                              newItemset = itemseti.clone()
                              newItemset.add((itemsetj.get(itemsetj.size()-1)).clone())
                              newItemset.calculateSupports(self.dataBase, self.train)
                              if newItemset.getSupportClass() >= self.minsup:
                                  Lnew.add(newItemset)


                      self.generateRules(Lnew, clas)
                      self.generateLarge(Lnew, clas)
                      Lnew.clear()
                      gc.collect()


    def  isCombinable(itemseti, itemsetj):
          # int
          i = None
          itemi = None
          itemj = None
          itemset = None

          itemi = itemseti.get(itemseti.size()-1)
          itemj = itemsetj.get(itemseti.size()-1)
          if itemi.getVariable() >= itemj.getVariable():
              return False

          return True


        # /**
        #  * Returns the rules generated on the Stage 1.
        #  * @return the rules of the Stage 1
        #  */
    def  getRulesStage1(self):
          return self.ruleStage1


    def  generateRules(self, Lk, clas):
	    #int
        i = None
        uncover = None
        itemset=None
        confidence = None
        for i in range (Lk.size() - 1, 0,-1) :
            itemset = Lk.get(i)

            if itemset.getSupport() > 0.0:
               confidence = itemset.getSupportClass() / itemset.getSupport()
            else:
               confidence = 0.0
            if confidence > 0.4:
                self.ruleBaseClase.add(itemset)
                self.ruleStage1 = self.ruleStage1 + 1
            if confidence > self.minconf:
                Lk.remove(i)
            if self.ruleBaseClase.size() > 500000:
                self.ruleBaseClase.reduceRules(clas)
                gc.collect()


