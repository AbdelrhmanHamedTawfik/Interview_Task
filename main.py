import requests
import asyncio
import pandas as pd
import SemanticSerch as ss
from bs4 import BeautifulSoup


# wrtie data to excel file
def WriteDataToExcel(company_data):
	df = pd.DataFrame.from_dict(company_data, orient='index')
	df.to_excel("task_output.xlsx", engine='openpyxl')

# deconde the coludflare email encryption
def DecodeColudeFlareEmail(encoded_email):
	r = int(encoded_email[:2], 16)
	email = ''.join([chr(int(encoded_email[i:i+2], 16) ^ r) for i in range(2, len(encoded_email), 2)])

	return email

# extract company attributes from the company page
def ExtractCompanyData(url):
	# parse html response
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	company_info = {}
	
	# extract required information using the htmla tags paresed above
	company_info["name"] = soup.select('h3.card-title')[0].text.strip()
	company_info["membership_number"] = soup.find('div', class_='info-name', string=lambda text: text and text.lower() == 'membership number').find_next_sibling('div', class_='info-value').text.strip()
	company_info["phone"] = soup.find('div', class_='info-name', string=lambda text: text and text.lower().strip() == 'phone').find_next_sibling('div', class_='info-value').text.strip()
	company_info["city"] = soup.find('div', class_='info-name', string=lambda text: text and text.lower().strip() == 'city').find_next_sibling('div', class_='info-value').text.strip()
	encoded_mail = soup.find('div', class_='info-name', string=lambda text: text and text.lower().strip() == 'email').find_next_sibling('div', class_='info-value').find().get('href').replace('mailto:', '').split("#")[1]
	company_info["email"] = DecodeColudeFlareEmail(encoded_mail)
	activities = ""
	
	# add all company activities as form of long string
	for tag in soup.select('h3.card-title')[1].find_next_sibling('ul'):
		if "map" in tag.find_next().text.lower():
			continue
		
		activities += tag.find_next().text.strip() + " "

	company_info["activities"] = activities.replace("\n", " ").replace("  ", " ")

	return company_info

async def RunWebCrawler():
	url = 'https://muqawil.org/en/contractors?'
	companies_data = {}

	for page_index in range(1, 11):
		# page number
		params = {'page': str(page_index)} 
		response = requests.get(url, params)

		# parse html response
		soup = BeautifulSoup(response.content, 'html.parser')
		# fetch each company page a tag
		companies_tag = soup.select('.card-title a')

		for index, tag in enumerate(companies_tag):
			company_url = tag.get('href')
			company_data = ExtractCompanyData(company_url)
			company_data["page"] = page_index
			dic_new_index = 0
			if companies_data:
				dic_new_index = list(companies_data.keys())[-1]

			companies_data[(dic_new_index + 1)] = company_data
			
			# add delay to avoid over floding the website with requests
			await asyncio.sleep(2)
	
	WriteDataToExcel(companies_data)

if __name__ == "__main__":
	asyncio.run(RunWebCrawler())
	# ss.SetupDataForSearch()
	# search_result = ss.Search("Construction of buildings")
	# ss.DrawSearchResult(search_result)
