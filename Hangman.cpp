// Hangman.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <string>

std::string words [] = { "hello", "python" };

void user_guess(std::string &current, std::string &word) {
	std::cout << "Current state: " << current << std::endl;
	char guess;
	std::cin >> guess;
	if (word.find(guess) != std::string::npos &&
		current.find(guess) == std::string::npos) {
		char *c, *w;
		for (c = &current[0], w = &word[0];
			 c < &current[0] + current.length();
			 ++c, ++w) {
			*c = *w == guess ? *w : *c;
		}
	}
	else {
		std::cout << "Nope! " << guess << " is not in the word." << std::endl;
	}
}

int main()
{
	for (std::string word : words) {
		int remaining = 5;
		std::string current = std::string(word.length(), '*');
		std::string old_state;
		bool broke = false;
		while (remaining > 0) {
			old_state = current;
			user_guess(current, word);
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