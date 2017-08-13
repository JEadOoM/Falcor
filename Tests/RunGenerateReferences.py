import subprocess
import argparse
import os
from datetime import date
import shutil
import stat
import sys
import json
import pprint

import RunTestsSet as rTS
import CloneRepo as cloneRepo
import Configs as configs
import Helpers as helpers


# Parse the Test Collection.
def runTestCollection(json_filename="TestsCollectionsAndSets\\TestsCollection.json"):
    try:
        # Try and open the json file.
        with open(json_filename) as json_file:
            
            # Try and parse the data from the json file.
            try:
                json_data = json.load(json_file)

                # pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(json_data)

            # Exception Handling.
            except ValueError:
                print "Error parsing Tests Set file : " + json_filename
                return None

            # Check if the Tests Name is defined.
            if not json_data['Tests Name']:
                print 'Error "Tests Name" not defined in json file : ' + json_filename
                return None

            # Check if the Tests Array is defined.
            if not json_data['Tests Name']:
                print 'Error "Tests" not defined in json file : ' + json_filename
                return None


            repositoryTarget = configs.gDefaultCloneRepository
            branchTarget = configs.gDefaultCloneBranch
            destinationTarget = configs.gDefaultCloneDestination 

            # Check if the Repository Target is defined.
            if json_data['Repository Target']:
                if json_data['Repository Target'] != "": 
                    repositoryTarget = json_data['Repository Target']

            # Check if the Branch Target is defined.
            if json_data['Branch Target']:
                if json_data['Branch Target'] != "":
                    branchTarget = json_data['Branch Target']

            # Check if the Destination Target is defined.
            if json_data['Destination Target']:
                if json_data['Destination Target'] != "":
                    destinationTarget = json_data['Destination Target']


            # Initialize the Test Results.
            testSetsResults = []

            # Run all the Test Set.
            for currentTestsSet in json_data["Tests"]:

                # Check if a solution target is defined.
                if currentTestsSet['Solution Target']:
                    if currentTestsSet['Solution Target'] == "":
                        continue
                else:
                    continue

                # Check if a configuration target is defined.
                if currentTestsSet['Configuration Target']:
                    if currentTestsSet['Configuration Target'] == "":
                        continue
                else:
                    continue

                # Check if a configuration target is defined.
                if currentTestsSet['Tests Set']:
                    if currentTestsSet['Tests Set'] == "":
                        continue
                else:
                    continue


                try:
                    
                    solutionTarget = currentTestsSet['Solution Target']
                    configurationTarget = currentTestsSet['Configuration Target']
                    testsSet = currentTestsSet['Tests Set']
                    destinationBranchConfigurationTarget = destinationTarget + branchTarget + '\\' + configurationTarget + '\\'                      



                    # Run the Tests Set and get the results.
                    currentTestSetResult = rTS.runTestsSet(destinationBranchConfigurationTarget, solutionTarget, configurationTarget, testsSet, True)

                    # 
                    if currentTestSetResult == None:
                        continue

                    # Add the Test Result to the Test Results.
                    testSetsResults.append(currentTestSetResult)

                # Exception Handling.
                except (rTS.TestsSetOpenError, rTS.TestsSetParseError) as runTestsSetError:
                    print runTestsSetError.args
                    continue
            
            allRanSuccessfully = True

            #   Check to see if any of the test run failed.

            #   Iterate over the Test Set Results.
            for index, currentTestSetResult in enumerate(testSetsResults):

                for currenTestName in currentTestSetResult:

                    for currentTestRunResult in currentTestSetResult[currenTestName]:

                        if currentTestRunResult['Completed'] != True:

                            allRanSuccessfully = False

            helpers.directoryCleanOrMake(configs.gDefaultReferenceTarget + "Results\\")
            helpers.directoryCopy("Results\\", configs.gDefaultReferenceTarget + "Results\\")
            
            if allRanSuccessfully:
                print "Ran!"
                # Move the references.
                return 0



        return 0

    # Exception Handling.
    except (IOError, OSError) as jsonopenerror:
        print 'Error opening Tests Collection json file : ' + json_filename
        return None



def main():

    # Argument Parser.
    parser = argparse.ArgumentParser()

    # Add the Argument for which Test Collection to use.
    parser.add_argument('-testsCollection', nargs='?', action='store', help='Specify the Test Collection', default='TestsCollectionsAndSets\\TestsCollection.json')

    # Add the Arguments for do not build and for show summary, and whether to run it locally.
    parser.add_argument("-nb", action='store_true', help='Whether or not to build the solutions again.')


    # Parse the Arguments.
    args = parser.parse_args()

    # Parse the Test Collection.
    return runTestCollection(args.testsCollection)




if __name__ == '__main__':
    main()
