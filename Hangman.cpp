// Hangman.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <string>

std::string words [] = { "hello", "python" };

std::string * user_guess(std::string current, std::string word) {
	std::cout << "Current state: " << current << std::endl;
	std::string guess;
	std::cin >> guess;
	std::string returned [2];
	if (word.find(guess) != std::string::npos &&
		current.find(guess) == std::string::npos) {
		const int length = word.length();
		std::string * result;
		result = new std::string[length];
		for (int i = 0;
			i < length; ++i) {
			result[i] = word[i] == guess[0] ? word[i] : current[i];
		}
		returned[0] = *result;
		returned[1] = word;
	}
	else {
		std::cout << "Nope! " << guess << " is not in the word." << std::endl;
		returned[0] = current;
		returned[1] = word;
	}
	return returned;
}

int main()
{
	for (std::string word : words) {
		int remaining = 5;
		std::string current = "";
		for (unsigned int i = 0; i < word.length(); ++i) {
			current += "*";
		}
		std::string old_state;
		bool broke = false;
		while (remaining > 0) {
			old_state = current;
			std::string * ug;
			ug = user_guess(current, word);
			current = ug[0];
			word = ug[1];
			if (old_state == current) {
				--remaining;
				std::cout << "Remaining guesses: " << remaining << std::endl;
			}
			if (current == word) {
				std::cout << "You won! - " << word << std::endl;
				broke = true;
				break;
			}
		}
		if (!broke) {
			std::cout << "You lost. - " << word << std::endl;
		}
	}
	return 0;
}