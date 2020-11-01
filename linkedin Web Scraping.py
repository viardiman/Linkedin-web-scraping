# import web driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv

import parameters 

def validate_field(field):
	if field is None :
		field = 'No Result'
	return field

header = "Name,Job Title,Company,College,Location,URL,\n"
f = open(parameters.file_name, "w")
f.write(header)

driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')

driver.get('https://www.linkedin.com')

login_page_button = driver.find_element_by_class_name('nav__button-secondary')
login_page_button.click()

username = driver.find_element_by_id('username')
username.send_keys(parameters.linkedin_username)

password = driver.find_element_by_id('password')
password.send_keys(parameters.linkedin_password)

login_button = driver.find_element_by_class_name('login__form_action_container')
login_button.click()

driver.get('https://www.google.com')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "python developer" AND "London"')
search_query.send_keys(Keys.RETURN)

linkedin_urls = driver.find_elements_by_xpath("//*[@id='rso']/div/div/div[1]/a")
linkedin_urls = [url.get_attribute('href') for url in linkedin_urls]

for linkedin_url in linkedin_urls:
	driver.get(linkedin_url)
	sel = Selector(text=driver.page_source)

	name = sel.xpath('//*[@id="ember58"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
	if name:
		name = name.strip()

	job_title = sel.xpath('//*[@id="ember58"]/div[2]/div[2]/div[1]/h2/text()').extract_first()
	if job_title:
		job_title = job_title.strip()

	company = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li[1]/a/span/text()').extract_first()
	if company:
		company = company.strip()

	college = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li[2]/a/span/text()').extract_first()
	if college:
		college = college.strip()

	location = sel.xpath('//*[@id="ember58"]/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()
	if location:
		location = location.strip()

	linkedin_url = driver.current_url

	name = validate_field(name)
	job_title = validate_field(job_title)
	company = validate_field(company)
	college = validate_field(college)
	location = validate_field(location)
	linkedin_url = validate_field(linkedin_url)

	print('\n')
	print('Name: '+ name)
	print('Job Title: '+ job_title)
	print('Company: '+ company)
	print('College: '+ college)
	print('Location: '+ location)
	print('URL: '+ linkedin_url)
	print('\n')

	f.write(name+ "," + job_title+ "," +company+ "," +college+ "," +location+ "," +linkedin_url+ "," +'\n')

driver.quit()


