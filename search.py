''' Implements dynamic search algorithm from Venkataraman '''

import math

# lexicon is a dictionary or words and their respective frequencies
lexicon = {}

# syllables is a dictionary of syllables and their respective frequencies.
syllables = {' ':1}

def evalUtterance(utterance):
	'''
	Takes an unsegmented string and returns it as a segmented string with spacing.
	Args:
		utterace: utterance u where u[i] are the syllables in it i.e bihgS
			      "bihgSdrahmS"

	Returns:
		segmentedWord: best segmentation of utterance based on negative log of the probability of the word and phoneme (uses Katz back-off).
					   i.e. "Iz D&t f%D6dOgi"

	'''
	n = len(utterance)
	bestCost = [0] * n
	prevBoundary = [0] * n

	if n == 0:
		return 0;

	for i in range(0, n):
		# i+1 is different from Venkataraman's because you have to account for how i stops at n - 1
		bestCost[i] = evalWord(utterance[0:i+1])
		prevBoundary[i] = -1

		for j in range(i):
			word = utterance[j+1:i+1]
			evalWordResult = evalWord(word)
			cost = bestCost[j] + evalWordResult

			if cost < bestCost[i]:
				bestCost[i] = cost
				prevBoundary[i] = j

	i = n - 1
	segUtterance = utterance

	allWords = []
	while i >= 0:
		newWord, segUtterance = insertWordBoundary(segUtterance, prevBoundary[i])

		allWords.append(newWord)
		i = prevBoundary[i]

	# allWords is just to return the string with spaces in it
	allWords.reverse()
	return " ".join(allWords)

def insertWordBoundary(utterance, bestSegpoint):
	'''
	Addeds the best segmentation of the utterance into lexicon table.
	If the best segmentation is a new word, add each of its syllables into the syllables table.

	Args:
		utterace: utterance u[0..n] where u[i] are the syllables in it.
		bestSegpoint: an integer representing the index of bestSegpoint
	Returns:
		segUtterance: new smaller utterance after removal of newWord
		newWord: the newWord segmented and updated into the syllables and lexicon tables.

	'''
	if bestSegpoint == -1:
		newWord = utterance
	else:
		newWord = utterance[bestSegpoint + 1:]

	wordString = "S".join(newWord) + "S"

	if wordString in lexicon:
		lexicon[wordString] += 1
	else:
		lexicon[wordString] = 1
		syllables[" "] += 1
		for syllable in newWord:
			if syllable in syllables:
				syllables[syllable] += 1
			else:
				syllables[syllable] = 1

	return wordString, utterance[:bestSegpoint + 1]

def evalWord(word):
	'''
	Calculates a log score for word.

	Args:
		word: word w[0..k] where w[i] are the syllables in it. Word is a string.
	Returns:
		score: calculated based on phoneme and lexicon tables using Katz back-off.

	'''
	score = 0

	if len(word) == 0:
		return score

	wordString = "S".join(word) + "S"

	# unigram
	if wordString in lexicon:
		P_W = lexicon[wordString] / (sum(lexicon.values()) + len(lexicon))
		score += -math.log(P_W)
		# print("Cost1("+ wordString + ") = " + str(score))
		return score
	else:
		# back off to syllables
		if len(lexicon) != 0:
			score += -math.log(len(lexicon) / (sum(lexicon.values()) + len(lexicon)))

	P_0 = syllables[' '] / sum(syllables.values())
	if P_0 != 1:
		prob = P_0 / (1-P_0)
	else:
		prob = P_0 / (1-0.9999999999999999)

	for i in range(len(word)):
		if word[i] in syllables:
			prob *= float(syllables[word[i]]) / sum(syllables.values())

	score += -math.log(prob)

	return score

if __name__ == "__main__":
	with open('data/new.mother.speech.txt', "r") as text:
		with open('results/result.txt','w') as result:
			for count, line in enumerate(text):
				processedLine = line.replace('\n', '').replace(' ', '')
				processedLine = processedLine.split("S")
				processedLine.remove("")

				segmentedWord = evalUtterance(processedLine)
				print("SEGMENTED WORD", segmentedWord)
				result.write(segmentedWord + "\n")

		with open('results/lexicon.txt', 'w') as writeLexicon:
			writeLexicon.write(str(lexicon))

	