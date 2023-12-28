import string
import numpy as np

class WordleGame:
    def __init__(self, word_len:int, word_dict:dict):
        self.word_len = word_len
        self.word_dict = word_dict
        self._allowed_chars =  list(string.ascii_lowercase)
        self.available_chars = set(string.ascii_lowercase)
        self.letter_freq_dict = dict(zip(self._allowed_chars, [0 for i in range(len(self._allowed_chars))]))
        feasible_word_list = [y for y in word_dict.keys() if word_dict[y] == word_len]
        # feasible_word_list = [y for y in feasible_word_list if len(y) == len(set(y))]
        self.feasible_word_list = feasible_word_list
        # self.num_feasible_words = len(feasible_word_list)
        self.current_guess = [None for i in range(word_len)]
        self.correct_charset = set()
        self.negative_charset = set()
        self.misplaced_char_dict = {}
        self.rounds = 0

    def _get_word_len_from_dict(self, candidate_word: str):
        word_dict = self.word_dict
        try:
            response_val = word_dict[candidate_word]
        except Exception as e:
            # print(e)
            response_val = 0

        return response_val

    def _sample_random_word(self):
        num_feasible_words = len(self.feasible_word_list)
        if num_feasible_words >1:
            idx = np.random.randint(0,num_feasible_words-1)
        else:
            idx = 0
        return (self.feasible_word_list)[idx]

    def _set_target_word(self, target_word = None):
        if target_word is not None:
            self.target_word = target_word
        else:
            self.target_word = self._sample_random_word()

    def _check_word(self, candidate_word: str):
        cand_word_list = list(candidate_word)
        targ_word_list = list(self.target_word)
        word_len = self.word_len

        correctly_placed = []
        for i in range(word_len):
            cand_letter = cand_word_list[i]
            if cand_letter == targ_word_list[i]:
                self.current_guess[i] = cand_letter
                correctly_placed.append(cand_letter)
            elif cand_letter in targ_word_list:
                self.misplaced_char_dict[cand_letter] = i

        letter_compare = [cand_word_list[i] in targ_word_list for i in range(word_len)]
    
        return letter_compare

    def _update_available_chars(self, candidate_word: str):
        letter_compare = self._check_word(candidate_word)
        candidate_word_list = list(candidate_word)
        word_len = self.word_len
        
        #Get letters to exclude
        letters_to_exclude = set([candidate_word_list[i] for i in range(word_len) if not(letter_compare[i])])
        # print(letters_to_exclude)
        available_chars = self.available_chars
        self.available_chars = available_chars - letters_to_exclude
        self.negative_charset.update(letters_to_exclude)
        
        #Get set of correct letters and their positions
        letters_to_include = set([candidate_word_list[i] for i in range(word_len) if letter_compare[i]])
        self.correct_charset.update(letters_to_include)

    
    def _update_guess_set(self, candidate_word:str, print_word = False):
        self._update_available_chars(candidate_word)
        feasible_word_list = self.feasible_word_list
        word_len = self.word_len
        current_guess = self.current_guess
        correct_charset = self.correct_charset
        negative_charset = self.negative_charset
        misplaced_char_dict = self.misplaced_char_dict

        # First remove words containing negative characters
        if negative_charset != set():
            feasible_word_list = [x for x in feasible_word_list if negative_charset.intersection(set(list(x))) == set()]
        
        if current_guess != [None for i in range(self.word_len)]:
            idx_to_check = [i for i in range(word_len) if current_guess[i] is not None]
            feasible_word_list_mod = [''.join(s[j] for j in idx_to_check) for s in feasible_word_list]
            guess_mod = ''.join(current_guess[j] for j in idx_to_check)
            feasible_word_list = [feasible_word_list[i] for i in range(len(feasible_word_list)) if feasible_word_list_mod[i] == guess_mod]
        
        if correct_charset != set():
            feasible_word_list = [x for x in feasible_word_list if correct_charset.issubset(set(list(x)))]

        if misplaced_char_dict != {}:
            for misplaced_char, pos in misplaced_char_dict.items():
                feasible_word_list = [x for x in feasible_word_list if x[pos] != misplaced_char]
        
        self.feasible_word_list = feasible_word_list
        if print_word:
            print(current_guess)

    def _subset_by_letters(self, letter_set: set):
        return [x for x in self.feasible_word_list if set(x) == letter_set]

    def _gen_letter_freq(self):
        pass
    
    def _high_frequency_guess(self):
        pass