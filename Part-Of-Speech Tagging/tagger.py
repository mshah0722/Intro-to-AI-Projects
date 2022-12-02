# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

# All global variables stored here
# List of Grammatical Tags
grammaticalTags = ["AJ0", "AJC", "AJS", "AT0", "AV0", "AVP", "AVQ", "CJC", "CJS", "CJT", "CRD", "DPS", "DT0", "DTQ", "EX0", "ITJ", "NN0", "NN1", "NN2", "NP0", "ORD", 
                   "PNI", "PNP", "PNQ", "PNX", "POS", "PRF", "PRP", "PUL", "PUN", "PUQ", "PUR", "TO0", "UNC", "VBB", "VBD", "VBG", "VBI", "VBN", "VBZ", "VDB", "VDD",
                   "VDG", "VDI", "VDN", "VDZ", "VHB", "VHD", "VHG", "VHI", "VHN", "VHZ", "VM0", "VVB", "VVD", "VVG", "VVI", "VVN", "VVZ", "XX0", "ZZ0"]

# List of Ambiguity Tags
ambiguityTags = ["AJ0-AV0", "AJ0-VVN", "AJ0-VVD", "AJ0-NN1", "AJ0-VVG", "AVP-PRP",  "AVQ-CJS", "CJS-PRP", "CJT-DT0", "CRD-PNI", "NN1-NP0", "NN1-VVB", "NN1-VVG", "NN2-VVZ", "VVD-VVN"]

# List of all Tags
allTags = grammaticalTags + ambiguityTags

# Set of all the words in the training data
setTrainingWords = []

# Initial Probability Dictionary
initialProbDict = {tag: 0 for tag in allTags}

# Tag occurence count
tagOccurenceCount = {tag: 0 for tag in allTags}

# Transmission Probability Matrix
transitionProbMat = np.zeros((len(allTags), len(allTags)))

# Emission Probability Matrix
emissionProbMat = np.zeros((0, 0))

# Global epsilon value for small values
epsilon = 0.000001

# All functions stored below
# Handle the case of inverting Ambiguity Tags
def handle_inverted_tags(tag):
    if len(tag) == 7 and tag not in ambiguityTags:
        beginning = tag[0:3]
        end = tag[4:]
        tag = end + "-" + beginning
        
    return tag

# Read training list and initialize training array with tuples
def read_training_file(training_list):
    openFile = open(training_list, 'r')
    allLines = openFile.readlines()
    
    trainingArray = []
    
    for line in allLines:
        line = line[:-1]
        trainingTuple = tuple(line.split(' : '))
        trainingArray.append(trainingTuple)
    return trainingArray

# Read testing list and initialize testing array with tuples
def read_testing_file(testing_list):
    openFile = open(testing_list, 'r')
    allLines = openFile.readlines()
    
    testingArray = []
    
    for line in allLines:
        line = line[:-1]
        testingArray.append(line)
        
    return testingArray

# Create output array with predictions
def write_to_output_file(testingArray, mostLikelyTagSeq, output_file):
    f = open(output_file, "w")
    
    for i in range(len(testingArray)):
        word = testingArray[i]
        tag = mostLikelyTagSeq[i]
        f.write(word + " : " + tag + "\n")
    f.close()
    
    return

# Initialize the set of training words
def init_set_training_words(trainingArray):
    # Access the following global variables
    global setTrainingWords
    
    # Set of all words from training array
    setTrainingWords = set([tup[0] for tup in trainingArray])
    
    # Convert set back to a list to allow indexing
    setTrainingWords = list(setTrainingWords)
    
    return

# Calculate Initial Probability
def calculate_initial_prob(trainingArray):
    # Access the following global variables
    global initialProbDict
    global tagOccurenceCount
    
    # Initialize a blank previous word, and sentence count to 0
    prevWord = ""
    sentenceCount = 0
    
    # Calculate the initial count for all tags
    for i in range(len(trainingArray)):
        word = trainingArray[i][0]
        tag = handle_inverted_tags(trainingArray[i][1])
        
        # Increase tag count for each tag
        tagOccurenceCount[tag] += 1
        
        # Increase the start of every sentence's tag by 1
        if prevWord == "." or i == 0:
            initialProbDict[tag] += 1
            sentenceCount += 1
        
        prevWord = word
    
    # Calculate the initial probability for all tags
    for tag in initialProbDict:
        if initialProbDict[tag] != 0:
            initialProbDict[tag] /= sentenceCount
    
    return  

# Calculate Transition Probability
def calculate_transition_prob(trainingArray):
    # Access the following global variables
    global transitionProbMat
    global tagOccurenceCount
    global epsilon
    
    # Calculate the transition count for all tags
    for i in range(len(trainingArray)-1):
        tag1 = handle_inverted_tags(trainingArray[i][1])
        tag2 = handle_inverted_tags(trainingArray[i+1][1])
        
        # Find the tag indices of each tag
        tag1Idx = allTags.index(tag1)
        tag2Idx = allTags.index(tag2)
        
        # Increase the transition count where tag1 is followed by tag2
        transitionProbMat[tag1Idx][tag2Idx] += 1
    
    # Calculate the transition probability for all tags
    for i in range(len(allTags)):
        count = tagOccurenceCount[allTags[i]]
        for j in range(len(allTags)):
            if transitionProbMat[i][j] != 0:
                transitionProbMat[i][j] /= count
            else:
                transitionProbMat[i][j] = epsilon
    
    return

# Calculate Emission Probability
def calculate_emission_prob(trainingArray):
    # Access the following global variables
    global emissionProbMat 
    global setTrainingWords
    global tagOccurenceCount
    global epsilon
    
    # Initialize the emission probability matrix  
    emissionProbMat = np.zeros((len(allTags), len(setTrainingWords)))
    
    # Calculate the emission count for all tags
    for i in range(len(trainingArray)):
        word = trainingArray[i][0]
        tag = handle_inverted_tags(trainingArray[i][1])
        idx = setTrainingWords.index(word)
        
        # Find the tag index of this tag
        tagIdx = allTags.index(tag)

        # Increase the amount that each word exists with this tag
        emissionProbMat[tagIdx][idx] += 1
                
    # Calculate the emission probability for all tags
    for i in range(len(allTags)):
        count = tagOccurenceCount[allTags[i]]
        for j in range(len(setTrainingWords)):
            if emissionProbMat[i][j] != 0:
                emissionProbMat[i][j] /= count
            else:
                emissionProbMat[i][j] = epsilon
    
    return

# Viterbi algorithm for part-of-speech tagging
def viterbi(testingArray):
    # Access the following global variables
    global setTrainingWords
    global allTags
    global initialProbDict
    global transitionProbMat
    global emissionProbMat
    global epsilon
    
    # Initialize the probability matrix
    probMatrix = np.zeros((len(allTags), len(testingArray)))
    
    # Initialize the previous matrix
    previousMatrix = np.zeros((len(allTags), len(testingArray)))
    
    # Initialize the first column of the probability matrix based on the first word
    for i in range(len(allTags)):
        word = testingArray[0]
        
        # Handle case where test word is not from training set
        # Set emission probability to epsilon
        if word not in setTrainingWords:
            emissionVal = epsilon
        else:
            idx = setTrainingWords.index(word)
            emissionVal = emissionProbMat[i][idx]
            
        probMatrix[i][0] = initialProbDict[allTags[i]] * emissionVal
        
        # Initialize the first column of the previous matrix to 0
        previousMatrix[i][0] = 0        
    
    # Fill in the rest of the probability matrix for steps 1 to length(E)-1
    for i in range(1, len(testingArray)):
        word = testingArray[i]
        
        # Handle case where test word is not from training set
        # Set emission probability to epsilon
        if word not in setTrainingWords:
            flag = False
            emissionVal = epsilon
        else:
            flag = True
            idx = setTrainingWords.index(word)
        
        for j in range(len(allTags)):
            # Handle case where test word is from the training set
            if flag:
                emissionVal = emissionProbMat[j][idx]
            
            # Get max probability value and index
            maxProbIdx = np.argmax(probMatrix[:,i-1] * transitionProbMat[:,j] * emissionVal)
            maxProb = probMatrix[maxProbIdx][i-1] * transitionProbMat[maxProbIdx][j] * emissionVal
            probMatrix[j][i] = maxProb
            previousMatrix[j][i] = maxProbIdx
        
        # Normalize the probability matrix for each column to reduce chances of going to zero
        probMatrix[:,i] /= np.sum(probMatrix[:,i])
            
    # Find the most likely tag sequence
    mostLikelyTagSeq = []
    maxProb = 0
    maxProbIdx = 0
    
    # Find the max probability in the last column of the matrix
    for i in range(len(allTags)):
        if probMatrix[i][len(testingArray)-1] > maxProb:
            maxProb = probMatrix[i][len(testingArray)-1]
            maxProbIdx = i
    mostLikelyTagSeq.append(allTags[maxProbIdx])
    
    # Backtrack through the previous matrix to find the most likely tag sequence
    for i in range(len(testingArray)-1, 0, -1):
        mostLikelyTagSeq.append(allTags[int(previousMatrix[maxProbIdx][i])])
        maxProbIdx = int(previousMatrix[maxProbIdx][i])
    
    # Reverse the most likely tag sequence
    mostLikelyTagSeq = mostLikelyTagSeq[::-1]
    
    return mostLikelyTagSeq

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")

    # Read the training list and create training array
    trainingArray = []
    
    # if len(training)
    for trainingFile in training_list:
        trainingArray += read_training_file(trainingFile)
    
    # Initialize the set of training words
    init_set_training_words(trainingArray)
    
    # Calculate the initial probability
    calculate_initial_prob(trainingArray)

    # Calculate the transition probability
    calculate_transition_prob(trainingArray)

    # Calculate the emission probability
    calculate_emission_prob(trainingArray)
    
    # Read the testing file and create testing array
    testingArray = read_testing_file(test_file)
    
    # Run the Viterbi Algorithm on the testing array
    mostLikelyTagSeq = viterbi(testingArray)
    
    # Write the most likely tag sequence to the output file
    write_to_output_file(testingArray, mostLikelyTagSeq, output_file)
    
    return

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Output file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)