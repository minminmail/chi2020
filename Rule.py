# /***********************************************************************
#
# 	This file is part of KEEL-software, the Data Mining tool for regression,
# 	classification, clustering, pattern mining and so on.
#
# 	Copyright (C) 2004-2010
#
# 	F. Herrera (herrera@decsai.ugr.es)
#     L. S谩nchez (luciano@uniovi.es)
#     J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
#     S. Garc铆a (sglopez@ujaen.es)
#     A. Fern谩ndez (alberto.fernandez@ujaen.es)
#     J. Luengo (julianlm@decsai.ugr.es)
#
# 	This program is free software: you can redistribute it and/or modify
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
# **********************************************************************/

import Fuzzy_Chi
from Fuzzy import Fuzzy
from data_row import data_row

# * <p>This class contains the structure of a Fuzzy Rule</p>
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 29/10/2007
# * @version 1.0
# * @since JDK1.5

class Rule:
    antecedent = None
    class_value = None
    weight = None
    compatibilityType = None

    # added by rui for negative rule
    rule_type = None
    rule_priority = None
    data_row_here = None
    granularity_sub_zone = None
    # added at 2020/06/25 to check positive rule confident
    confident_value = None

    def __init__(self):

        # print("__init__ of Rule")
        self.data_row_here = data_row()

    # Default constructor

    # * Constructor with parameters
    # * @param n_variables int
    # * @param compatibilityType int

    def setTwoParameters(self, n_variables, compatibilityType):
        # print("In rule calss , setTwoParameters method, the n_variables = " + str(n_variables))
        self.antecedent = [Fuzzy() for x in range(n_variables)]
        self.compatibilityType = compatibilityType

        # * It assigns the class of the rule
        # * @param clas int

    def setClass(self, clas):
        self.class_value = clas

    # added by rui for negative rule
    def get_class(self):
        return self.class_value

    # * It assigns the rule weight to the rule
    # * @param train myDataset the training set
    # * @param ruleWeight int the type of rule weight

    def assingConsequent(self, train, ruleWeight):
        if ruleWeight == Fuzzy_Chi.Fuzzy_Chi.CF:
            self.consequent_CF(train)

        elif ruleWeight == Fuzzy_Chi.Fuzzy_Chi.PCF_II:
            self.consequent_PCF2(train)
        # arrived here
        elif ruleWeight == Fuzzy_Chi.Fuzzy_Chi.PCF_IV:
            self.consequent_PCF4(train)

        elif ruleWeight == Fuzzy_Chi.Fuzzy_Chi.NO_RW:
            self.weight = 1.0

    # * It computes the compatibility of the rule with an input example
    # * @param example double[] The input example
    # * @return double the degree of compatibility

    def compatibility(self, example):
        if self.compatibilityType == Fuzzy_Chi.Fuzzy_Chi.MINIMUM:
            # print("self.compatibilityType == Fuzzy_Chi.Fuzzy_Chi.MINIMUM")
            return self.minimumCompatibility(example)
    # arrived here
        else:
            # print("self.compatibilityType != Fuzzy_Chi.Fuzzy_Chi.MINIMUM"+", self.compatibilityType = "+ str(
            # self.compatibilityType))
            # here is the algorithm arrives
            # print("in compatibility before the productCompatibility method:  ")
            return self.productCompatibility(example)

    # * Operator T-min
    # * @param example double[] The input example
    # * @return double the computation the the minimum T-norm

    def minimumCompatibility(self, example):
        minimum = None
        membershipDegree = None
        minimum = 1.0
        for i in range(0, len(self.antecedent)):
            # print("example[" + str(i) + "] = " + example[i])
            membershipDegree = self.antecedent[i].setX(example[i])
            # print("membershipDegree in minimumCompatibility = " + str(membershipDegree))
            minimum = min(membershipDegree, minimum)

        return minimum

    # * Operator T-product
    # * @param example double[] The input example
    # * @return double the computation the the product T-norm
    # arrive here
    def productCompatibility(self, example):

        product = 1.0
        antecedent_number = len(self.antecedent)
        # print("antecedent_number = " + str(antecedent_number))
        # print("before the antecedent loop :")
        for i in range(0, antecedent_number):
            # print("example[i="+ str(i)+"]"+":"+ str(example[i]))
            # print("in loop before get memebershipdegree")
            membershipDegree = self.antecedent[i].setX(example[i])
            # print("membershipDegree in productCompatibility  = " +str(membershipDegree))
            product = product * membershipDegree
        # print("product: "+ str(product))
        return product

    # * Classic Certainty Factor weight
    # * @param train myDataset training dataset

    def consequent_CF(self, train):
        train_Class_Number = train.getnClasses()
        # to have enough class_sum space
        classes_sum = [0.0 for x in range(train_Class_Number+1)]
        for i in range(0, train.getnClasses()+1):
            classes_sum[i] = 0.0

        total = 0.0
        comp = None
        # Computation of the sum by classes */
        for i in range(0, train.size()):
            comp = self.compatibility(train.getExample(i))
            classes_sum[train.getOutputAsIntegerWithPos(i)] = classes_sum[train.getOutputAsIntegerWithPos(i)] + comp
            total = total + comp

        print("classes_sum[self.class_value]  = " + str(classes_sum[self.class_value]) + "total" + str(total))
        self.weight = classes_sum[self.class_value] / total

    # * Penalized Certainty Factor weight II (by Ishibuchi)
    # * @param train myDataset training dataset

    def consequent_PCF2(self, train):
        classes_sum = float[train.getnClasses()]
        for i in range(0, train.getnClasses()):
            classes_sum[i] = 0.0

        total = 0.0
        comp = None
        # Computation of the sum by classes */
        for i in range(0, train.size()):
            comp = self.compatibility(train.getExample(i))
            classes_sum[train.getOutputAsIntegerWithPos(i)] = classes_sum[train.getOutputAsIntegerWithPos(i)] + comp
            total = total + comp

        sum_value = (total - classes_sum[self.class_value]) / (train.getnClasses() - 1.0)
        self.weight = (classes_sum[self.class_value] - sum_value) / total

    # * Penalized Certainty Factor weight IV (by Ishibuchi)
    # * @param train myDataset training dataset

    def consequent_PCF4(self, train):
        class_number = train.getnClasses()
        # print("train data set get the class_number: " + str(class_number))
        classes_sum_number = class_number + 1
        classes_sum = [0.0 for x in range(classes_sum_number)]
        # print("classes_sum length is : " + str(len(classes_sum)))
        # for have enough classes_sum for class value
        for i in range(0, train.getnClasses()+1):
            classes_sum[i] = 0.0

        total = 0.0
        train_size = train.size()
        # print("train_size: " + str(train_size))
        # Computation of the sum by classes */
        # print("Begin a new loop for calculating comp " + "/n/n")
        zeroCompNumber = 0

        # for i in range(0, train_size):
            # print("train.getExample(i) : " + str(train.getExample(i)))
            # class_type = train.getOutputAsIntegerWithPos(i)
            # print("test the class type print is : " + str(class_type))

        for i in range(0, train_size):
            # print("train.getExample(i) : " + str(train.getExample(i)))
            comp = self.compatibility(train.getExample(i))
            if comp == 0:
                zeroCompNumber = zeroCompNumber+1

            # print(" The list index out of range is i = " + str(i))
            class_type = train.getOutputAsIntegerWithPos(i)
            # print(" class_type = " + str(class_type))
            classes_sum[class_type] = classes_sum[class_type] + comp
            total = total + comp

        # print("self.clas =" + str(self.class_value) + "classes_sum[self.clas] :" + str(classes_sum[self.class_value]))
        # print(" The zero comp number in this loop is :" + str(zeroCompNumber))
        sum_value = total - classes_sum[self.class_value]
        self.weight = (classes_sum[self.class_value] - sum_value) / total
        print("self.weight is " + str(self.weight))

    # * This function detects if one rule is already included in the Rule Set
    # * @param r Rule Rule to compare
    # * @return boolean true if the rule already exists, else false

    def comparison(self, rule):
        contador_value = 0
        for j in range(0, len(self.antecedent)):
            if self.antecedent[j].label == rule.antecedent[j].label:
                contador_value = contador_value + 1

        if contador_value == len(rule.antecedent):
            if self.class_value != rule.class_value:  # Comparison of the rule weights
                if self.weight < rule.weight:
                    # Rule Update
                    self.class_value = rule.class_value
                    self.weight = rule.weight

            return True
        else:
            return False

    def calculate_confident(self, data_row_array):
        support_rule_number = 0
        self.confident_value = 0
        all_number_of_the_class = 0
        for i in range(0, len(data_row_array)):
            self.data_row_here = data_row_array[i]
            #  print("self.data_row_here.class_value  :" + str(self.data_row_here.class_value))
            #  print("self.class_value  :" + str(self.class_value))
            if self.data_row_here.class_value == self.class_value:
                all_number_of_the_class = all_number_of_the_class + 1
                meet_antecedent = 0
                for j in range(0, len(self.data_row_here.label_values)):

                    if self.antecedent[j].label == self.data_row_here.label_values[j]:  # meet the rule antecedent conditions
                        meet_antecedent = meet_antecedent + 1
                if len(self.antecedent) == meet_antecedent:
                    support_rule_number = support_rule_number + 1
        if all_number_of_the_class != 0:
            # print("support_rule_number :"+str(support_rule_number))
            # print("all_number_of_the_class :" + str(all_number_of_the_class))
            self.confident_value = support_rule_number / all_number_of_the_class
            print("self.confident_value in the rule:" + str(self.confident_value))


