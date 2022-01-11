class Filter:
    def __init__(self, guess, answer):
        self.word_must_contain = set()
        self.word_must_not_contain = set()
        self.letter_must_be = []
        self.letters_must_not_be = [[] for i in range(5)]

        # Individual letter filter
        for i, (guess_letter, answer_letter) in enumerate(zip(guess, answer)):
            if guess_letter == answer_letter:
                # Green letter
                self.letter_must_be.append((i, guess_letter))
            else:
                # Yellow or gray letter
                self.letters_must_not_be[i].append(guess_letter)

        # Whole word filter
        for guess_letter in guess:
            if guess_letter in answer:
                # Green or yellow letter
                self.word_must_contain.add(guess_letter)
            else:
                # Gray letter
                self.word_must_not_contain.add(guess_letter)

    def isPossibleMatch(self, word):
        for i, letter in self.letter_must_be:
            if word[i] != letter:
                return False

        for i, letters in enumerate(self.letters_must_not_be):
            for letter in letters:
                if word[i] == letter:
                    return False

        for letter in self.word_must_contain:
            if letter not in word:
                return False

        for letter in self.word_must_not_contain:
            if letter in word:
                return False

        return True
        

    def applyFilter(self, words):
        # Computes list of remaining words after filter is applied
        remaining_words = []
        for word in words:
            if self.isPossibleMatch(word):
                remaining_words.append(word)
        return remaining_words