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
url = "/page/1"

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

guess = ""
while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
	guess = input(
		f"Who said this quote? Guesses remaining {remaining_guesses} ")
	
	if guess == quote["author"]:
		print("CONGRATULATIONS!!! YOU GOT IT RIGHT!")
		break
	remaining_guesses -= 1

	if remaining_guesses == 3:
		res = requests.get(f"{base_url}{quote['bio-link']}")
		soup = BeautifulSoup(res.text, "html.parser")
		birth_date = soup.find(class_="author-born-date").get_text()
		birth_place = soup.find(class_="author-born-location").get_text()
		print(
			f"Here's a hint: The author was born on {birth_date} {birth_place} "
		)

	elif remaining_guesses == 2:
		print(
			f"Here's a hing: the authors first name starts with: {quote['author'][0]} "
		)
	
	elif remaining_guesses == 1:
		last_intial = quote["author"].split(" ")[1][0]
		print(
			f"Here's a hint: the author's last name starts with: {last_intial} "
		)
	
	else:
		print(
			f"Sorry, you ran out of guesses. the answer was {quote['author']} "
		)
	