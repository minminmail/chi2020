# ***********************************************************************

# /**
#  * <p>Title: Farchd</p>
#  * <p>Description: It contains the implementation of the Farchd algorithm</p>
#  * <p>Company: KEEL </p>
#  * @author Written by Jesus Alcala (University of Granada) 09/02/2011

#  */

# **********************************************************************/
from DataBase import DataBase
from RuleBase import RuleBase
from MyDataSet import MyDataSet
import datetime
import random
import time
import os.path

# * <p>It contains the implementation of the Chi algorithm</p>
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 02/11/2007
# * @version 1.0
# * @since JDK1.5

class Farchd:
    train_myDataSet = None
    val_myDataSet = None
    test_myDataSet = None

    outputTr = ""
    outputTst = ""

    fileDB = ""
    fileRB = ""
    fileTime = ""
    fileHora = ""
    data_string = ""
    fileRules = ""
    evolution = ""

    rulesStage1 = None
    rulesStage2 = None
    rulesStage3 = None

    dataBase = None
    ruleBase = None

    apriori = None

    population = None

    # algorithm parameters
    # int
    nLabels = None
    populationSize = None
    depth = None
    K_parameter = None
    maxTrials = None
    typeInference = None
    BITS_GEN = None
    double = None
    minsup = None
    minconf = None
    alpha = None

    # boolean
    somethingWrong = False  # to check if everything is correct.

    def __init__(self, parameters):
        print("__init__ of Fuzzy_Chi begin...")
        self.train_myDataSet = MyDataSet()
        self.val_myDataSet = MyDataSet()
        self.test_myDataSet = MyDataSet()
        self.startTime = datetime.datetime.now()

        try:
            self.fileToSavePath = parameters.file_path
            inputTrainingFile = parameters.getInputTrainingFiles()
            print("Reading the training set: "+ inputTrainingFile)
            self.train_myDataSet.readClassificationSet(inputTrainingFile, True, parameters.file_path)
            print("Reading the validation set: ")
            inputValidationFile = parameters.getValidationInputFile()
            self.train_myDataSet.readClassificationSet(inputTrainingFile, True, parameters.file_path)
            print("Reading the test set: ")
            self.test_myDataSet.readClassificationSet(parameters.getInputTestFiles(), False, parameters.file_path)
            print(" ********* test_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")
        except IOError as ioError:
            print("I/O error: " + str(ioError))
            self.somethingWrong = True
        except Exception as e:
            print("Unexpected error:" + str(e))
            self.somethingWrong = True
        self.somethingWrong = self.somethingWrong or self.train_myDataSet.hasMissingAttributes()
        self.outputTr = parameters.getTrainingOutputFile()
        self.outputTst = parameters.getTestOutputFile()

        self.fileDB = parameters.getOutputFile(0)
        self.fileRB = parameters.getOutputFile(1)
        self.data = parameters.getTrainingInputFile()
        self.fileTime = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
            '/')) + "/time.txt"
        self.fileTime = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
            '/')) + "/time.txt"
        self.fileHora = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
            '/')) + "/hora.txt"
        self.fileRules = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
            '/')) + "/rules.txt"
        # Now we parse the parameters long
        seed = int(float(parameters.getParameter(0)))

        self.nLabels = int(parameters.getParameter(1))
        self.minsup = float(parameters.getParameter(2))
        self.minconf = float(parameters.getParameter(3))
        self.depth = int(parameters.getParameter(4))
        self.K = int(parameters.getParameter(5))
        self.maxTrials = int(parameters.getParameter(6))
        self.populationSize = int(parameters.getParameter(7));
        if self.populationSize % 2 > 0:
                self.populationSize=self.populationSize + 1
        self.alpha = float(parameters.getParameter(8))
        self.BITS_GEN = int(parameters.getParameter(9))
        self.typeInference = int(parameters.getParameter(10))
        random.seed(seed)

    def execute(self):
        if self.somethingWrong:  # We do not execute the program
            print("An error was found, the data-set have missing values")
            print("Please remove the examples with missing data or apply a MV preprocessing.")
            print("Aborting the program")
        # We should not use the statement: System.exit(-1);
        else:
            print("No errors, Execute in FarcHD execute :")
            self.dataBase = DataBase(self.nLabels, self.train);
            self.ruleBase = RuleBase(self.dataBase, self.train, self.K, self.typeInference)
            self.apriori = Apriori(self.ruleBase, self.dataBase, self.train, self.minsup, self.minconf, self.depth)
            self.apriori.generateRB()
            self.rulesStage1 = self.apriori.getRulesStage1()
            self.rulesStage2 = int(self.ruleBase.size())

            pop = Population(self.train, self.dataBase, self.ruleBase, self.populationSize, self.BITS_GEN, self.maxTrials,self.alpha)
            pop.Generation()

            print("Building classifier")
            self.ruleBase = pop.getBestRB()

            self.rulesStage3 = int(self.ruleBase.size())

            self.dataBase.saveFile(self.fileDB);
            self.ruleBase.saveFile(self.fileRB);

            #  Finally we should fill the training and test  output files
            self.doOutput(self.val, self.outputTr)
            self.doOutput(self.test, self.outputTst)


            current_millis = int(round(time.time() * 1000))
            self.totalTime = current_millis - self.startTime
            self.writeTime()
            self.writeRules()
            print("Algorithm Finished")

    def write_time(self):
        aux = None # int
        seg = None # int
        min = None # int
        hor = None # int
        stringOut = ""
        stringOut = "" + self.totalTime / 1000 + "  " + self.data + "\n";
        Files.addToFile(self.fileTime, stringOut)
        self.totalTime /= 1000
        seg = self.totalTime % 60
        self.totalTime = self.totalTime/60
        min = self.totalTime % 60
        hor = self.totalTime / 60
        stringOut = ""
        if hor < 10:
            stringOut = stringOut + "0"+ hor + ":"
        else:
            stringOut = stringOut + hor + ":"
        if min < 10:
            stringOut = stringOut + "0"+ min + ":"
        else:
            stringOut = stringOut + min + ":"

        if seg < 10:
             stringOut = stringOut + "0"+ seg
        else :
             stringOut = stringOut + seg

        stringOut = stringOut + "  " + self.data + "\n"
        Files.addToFile(self.fileHora, stringOut)

    # """
    #    * It generates the output file from a given dataset and stores it in a file
    #    * @param dataset myDataset input dataset
    #    * @param filename String the name of the file
    #    *
    #    * @return The classification accuracy
    # """

    def doOutput(self, dataset, filename):
        output = ""
        output = dataset.copyHeader() #we insert the header in the output file
        #We write the output for each example
        for i in range(0, dataset.getnData()):
        # for classification:
            output = output+ dataset.getOutputAsString(i) + " " + self.classificationOutput(dataset.getExample(i)) + "\n"

        if os.path.isfile(filename):
            print("File exist")
            output_file = open(filename, "a+")
        else:
            print("File not exist")
            output_file = open(filename, "w+")

        output_file.write(output)


    # * It returns the algorithm classification output given an input example
    # * @param example double[] The input example
    # * @return String the output generated by the algorithm



    def classificationOutput(self, example):
        output = "?"
        # Here we should include the algorithm directives to generate the
        # classification output from the input example
        classOut = self.ruleBase.FRM(example)
        clas = self.ruleBase.FRM(example)
        if clas >= 0:
            output = self.train.getOutputValue(clas)

        return output
