#  /***********************************************************************
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

#  * <p>It reads the configuration file (data-set files and parameters)</p>
#  *
#  * @author Written by Alberto Fern谩ndez (University of Granada) 15/10/2007
#  * @Modified by Rui Min 28/09/2018
#  * @version 1.0
#  * @since Python 3

import logging
import re
from pathlib import Path


class ParseParameters:
    __algorithmName = ""
    __trainingFile = ""
    __validationFile = ""
    __testFile = ""

    __inputFiles = []
    __outputTrFile = ""
    __outputTstFile = ""
    __outputFiles = []
    file_path = None

    __parameters = {}

    # * Default constructor

    def __init__(self):
        self.__inputFiles = []
        self.__outputFiles = []
        self.__parameters = []
        self.file_path = None

        # * It obtains all the necesary information from the configuration file.<br/>
        # * First of all it reads the name of the input data-sets, training, validation and test.<br/>
        # * Then it reads the name of the output files, where the training (validation) and test outputs will be stored<br/>
        # * Finally it read the parameters of the algorithm, such as the random seed.<br/>
        # *
        # * @param fileName Name of the configuration file
        # *

    def parseConfigurationFile(self, fileName):

        logging.info("fileName in parseParameters = " + fileName)
        logging.info("before open file")
        # print(fileName)
        # print("file in parseConfigurationFile is :" + str(fileName))
        self.file_path = '\\'.join(fileName.split('\\')[0:-1])
        # print("file_path in parseConfigurationFile is :" + self.file_path)
        file = open(fileName, "r")

        # file is an string containing the whole file
        fileString = file.read()
        line = fileString.splitlines()

        for lineNumber in range(0, len(line)):
            # print("In line " + str(lineNumber) + ", the str is:begin ***   " + line[lineNumber] + "   ***end")
            if lineNumber == 0:
                self.readName(line[lineNumber])
            elif lineNumber == 1:
                self.readInputFiles(line[lineNumber])  # We read all the input files
            elif lineNumber == 2:
                self.readOutputFiles(line[lineNumber])  # We read all the output files
            else:  # read parameters and save into map
                self.readAllParameters(line[lineNumber])  # We read all the possible parameters
        # print("********* Summary for readAllParameters :" + " *********")
        # for key, value in self.__parameters:
            # print("********* parameters are : (" + key + ", " + value + " ) *********")

    # """
    #     * It reads the name of the algorithm from the configuration file
    #     * @param line StringTokenizer It is the line containing the algorithm name.
    # """
    def readName(self, line):
        # print("In side the readName method the parameter pass is :" + str(line))
        name = line.rpartition("=")[2]
        name = name.strip()
        # print("In side the readName method after split =, we get:" + str(name))
        self.__algorithmName = name

    # """
    #     * We read the input data-set files and all the possible input files
    #     * @param line StringTokenizer It is the line containing the input files.
    # """
    def readInputFiles(self, line):
        # print("Inside the readInputFiles mehtod, we get parameter is:" + str(line))
        firstParts = line.split()
        line_number = len(firstParts)
        file_list = []
        for lineNumber in range(0, line_number):
            wholeName = firstParts[lineNumber]
            # print("Inside readInputFiles, line " + str(lineNumber) + ",wholeName: " + str(wholeName))
            fileNameWithStr = wholeName.rpartition('/')[2]
            # print("Inside readInputFiles, line " + str(fileNameWithStr) + ",fileNameWithStr: " + str(fileNameWithStr))
            fileName = fileNameWithStr[:-1]
            # print("Inside readInputFiles, line " + str(lineNumber) + ",fileName: " + str(fileName))

            file_type = fileName[-3:]
            if file_type == "dat" or file_type == "tra" or file_type == "tst":
                file_list.append(fileName)

        file_number = len(file_list)
        # print("file_number :" + str(file_number))
        for i in range(0, file_number):
            if i == 0:
                self.__trainingFile = file_list[i]
            elif i == 1:
                self.__validationFile = file_list[i]
            elif i == 2:
                self.__testFile = file_list[i]
            else:
                self.__inputFiles.append(file_list[i])

        # print("The other remaining Input files number is :" + str(len(self.__inputFiles)))

        # for file in self.__inputFiles:
            # print("input file is :" + file)

        # print("********* Summary for readInputFiles :" + " *********")
        # print("********* The Input training file  is :" + str(self.__trainingFile) + " *********")
        # print("********* The Input validation file  is :" + str(self.__validationFile) + " *********")
        # print("********* The Input test file  is :" + str(self.__testFile) + " *********")

    # """
    #     * We read the output files for training and test and all the possible remaining output files
    #     * @param line StringTokenizer It is the line containing the output files.
    # """
    def readOutputFiles(self, line):
        # print("Inside the readInputFiles method, we get parameter is:" + str(line))
        firstParts = line.split()
        file_list = []
        line_number = len(firstParts)
        for lineNumber in range(0, line_number):
            wholeName = firstParts[lineNumber]
            # print("Inside readOutputFiles, line " + str(lineNumber) + ",wholeName: " + str(wholeName))
            fileNameWithStr = wholeName.rpartition('/')[2]
            # print("Inside readOutputFiles, line " + str(fileNameWithStr) + ",fileNameWithStr: " + str(fileNameWithStr))
            fileName = fileNameWithStr[:-1]
            # print("Inside readOutputFiles, line " + str(lineNumber) + ",fileName: " + str(fileName))

            file_type = fileName[-3:]
            if file_type == "txt" or file_type == "tra" or file_type == "tst":
                file_list.append(fileName)

        file_number = len(file_list)
        # print("file_number" + str(file_number))
        for i in range(0, file_number):
            if i == 0:
                self.__outputTrFile = file_list[i]
            elif i == 1:
                self.__outputTstFile = file_list[i]
            else:
                self.__outputFiles.append(file_list[i])

        # print("********* Summary for readOutputFiles :" + " *********")
        # print("*********  The output training file  is :" + str(self.__outputTrFile) + " *********")
        # print("*********  The output test file  is :" + str(self.__outputTstFile) + " *********")

        for file in self.__outputFiles:
            print("********* output file is :" + file + " *********")

    # """
    #     * We read all the possible parameters of the algorithm
    #     * @param line StringTokenizer It contains all the parameters.
    # """
    def readAllParameters(self, line):

        # print("readAllParameters begin,  line is :" + line)
        key = line.rpartition("=")[0]
        # print("The parameter key is :" + key)
        value = line.rpartition("=")[2]
        # print("The parameter value is :" + value)
        # remove the space in key and value of parameters and save into dictionary
        if key != "":
            self.__parameters.append((key, value))

    # If the algorithm is non-deterministic the first parameter is the Random SEED

    # """
    # * It returns the algorithm name
    # *
    # * @return the algorithm name
    # """

    def getAlgorithmName(self):
        return self.__algorithmName

    # """
    # * It returns the name of the parameters
    # *
    # * @return the name of the parameters
    # """
    def getParameters(self):
        param = self.__parameters
        return param

    # """
    # * It returns the name of the parameter specified
    # *
    # * @param key the index of the parameter
    # * @return the value of the parameter specified
    # """
    def getParameter(self, pos):

        return self.__parameters[pos][1]

    # """
    # * It returns the input files
    # *
    # * @return the input files
    # """

    def getInputFiles(self):
        return str(self.__inputFiles)

    # """
    # * It returns the input training files
    # *
    # * @return the input training files
    # """

    def getInputTrainingFiles(self):
        return self.__trainingFile

    # """
    #  * It returns the input test files
    #  *
    #  * @return the input test files
    #  """

    def getInputTestFiles(self):
        return self.__testFile

    # * It returns the validation input file
    # *
    # * @return the validation input file

    def getValidationInputFile(self):
        return self.__validationFile

    # /**
    #  * It returns the training output file
    #  *
    #  * @return the training output file
    #  */
    def getTrainingOutputFile(self):
        return self.__outputTrFile

    # * It returns the test output file
    # *
    # * @return the test output file

    def getTestOutputFile(self):
        return self.__outputTstFile

    # * It returns the algorithm name
    # *
    # * @return the algorithm name

    def getAlgorithmName(self):
        return self.__algorithmName

    # * It returns the name of the parameters
    # *
    # * @return the name of the parameters

    def getParameters(self):
        return self.__parameters

    # * It returns the input files
    # *
    # * @return the input files

    def getInputFiles(self):
        return self.__inputFiles

    # """
    # * It returns the input file of the specified index
    # *
    # * @param pos index of the file
    # * @return the input file of the specified index
    # """
    def getInputFile(self, pos):
        return self.__inputFiles[pos]

    # """
    # * It returns the output files
    # *
    # * @return the output files
    # """
    def getOutputFiles(self):
        return self.__outputFiles

    # """
    # * It returns the output file of the specified index
    # *
    # * @param pos index of the file
    # * @return the output file of the specified index
    # """
    def getOutputFile(self, pos):
        return self.__outputFiles[pos]
