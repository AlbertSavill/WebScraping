import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice

# list to store the scraped data
all_quotes = []

# This URL is constant
base_url = "http://quotes.toscrape.com/"

# This URL will keep changing
url = "page/1" # No need a '/' at the start of this url seeing the base url already ends with '/'

while url:

	# Concatenate both URLs together
	# Using requests.get to actually get the url
	res = requests.get(f"{base_url}{url}")
	print(f"Now Scraping{base_url}{url}")

	# Site is using html only, therefore html parser
	# Therefore use the text extracted from request and specify html parser parameter
	soup = BeautifulSoup(res.text, "html.parser") 
	# Extracting all elements
	# Look at HTML to find that class is "quote"
	quotes = soup.find_all(class_="quote")

	# For loop where 

	for quote in quotes:
		all_quotes.append({
			"text": quote.find(class_="text").get_text(), # Acutal quote in HTML
			"author": quote.find(class_="author").get_text(), # Author name in HTML
			"bio-link": quote.find("a")["href"]	# a href links bio of the author in HTML site
		})
	next_btn = soup.find(_class="next") # Next page in URL class on HTML site
	url = next_btn.find("a")["href"] if next_btn else None # Goes to next page until find no more
	sleep(2) # Delay the process for 2 seconds

quote = choice(all_quotes) # Randomize the scrapped data
remaining_guesses = 4
print("Here's a quote: ")
print(quote["text"])

# While loop below needs fixing, over engineered.

guess = ""
hints = [
	lambda: f"The author was born on {birth_date} {birth_place}",
	lambda: f"The author's first name starts with {quote['author'][0]}",
	lambda: f"The author's last name starts with: {quote['author'].split(' ')[1][0]}"
]

# print(len(hints))

# Getting the bio details once instead of repeatedly
if remaining_guesses > 3:
	res = requests.get(f"{base_url}{quote['bio-link']}")
	soup = BeautifulSoup(res.text, "html.parser")
	birth_date = soup.find(class_="author-born-date").get_text()
	birth_place = soup.find(class_="author-born-location").get_text()

# Whille loop to begin the remaining guesses and begin user input.
# Keep the game on if the guess is not equal to the author and remaining guesses havent ran out yet.
while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
	guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} ")

	# Condition for the user to win.
	if guess.lower() == quote["author"].lower():
		print("Congratulations!!! You Got it right!")
		break

	# Minus a remaining guess if user hasn't guesses correctly yet
	# If there's still remaining guesses, keep giving hints (lambda list above) but take away a guess every time a hint is given.
	# the len of hints is 3 as there's 3 hints in the list.
	# Once the remaining guesses are not above 0 in other words user ran out of guesses, then lose, and the programme
	# Prints the correct author.
	remaining_guesses -= 1
	if remaining_guesses > 0:
		if remaining_guesses <= len(hints):
			print(f"Here's a hint: {hints[len(hints) - remaining_guesses]()}")
	else:
		print(f"Sorry, you ran out of guesses. The answer was: {quote['author']}")
