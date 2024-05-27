from bs4 import BeautifulSoup
import csv
import requests
import datetime
from itertools import zip_longest
import urllib.parse


# declaring empty lists to add the info to it later.
job_titles_lst = []
job_skills_lst = []
company_name_lst = []
location_lst = []
date_posted_lst = []
job_details = []
job_type_lst = []
job_link_lst = []
salary_lst = []

page_num = 0
search_sentence = input("What are you searching for: ")
csv_dir = input('''
    Open a target folder for saving the file, open the terminal in it, 
    and run `pwd`. wirte the reust here: 
''')

while True:
    # 1st use request to fetch the url
    try:
        # URL encoding
        def generate_search_url(search_sentence):
            base_url = 'https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q='
            encoded_sentence = urllib.parse.quote(search_sentence)
            search_url = base_url + encoded_sentence + f"&start={page_num}"
            return search_url

        page = requests.get(generate_search_url(search_sentence))

        # 2nd save the page content
        src = page.content

        # 3rd create object to parse the content
        soup = BeautifulSoup(src, 'lxml')
 
        # 4th finding the elements job_title, company_name, location, job_type, job_skills, date_posted

        job_title = soup.find_all('h2', {'class':'css-m604qf'})
        company_name = soup.find_all('a', {'class':'css-17s97q8'})
        location = soup.find_all('span', {'class':'css-5wys0k'})
        job_skill = soup.find_all('div', {'class':'css-y4udm8'})
        date_posted = soup.find_all('div',{'class':'css-d7j1kk'})

        '''
        Can be implemented later

        # getting the job type and add them to a list to be added
        job_type = soup.find_all('div', {'class':'css-1lh32fc'})
        job_type_str = ''
        for div in job_type:
            job_type_str += div.text + "| "
        job_type_lst = job_type_str.split('|')
        '''
        
        # writng the info to the empty lists declared above.
        for i in range(len(job_title)):
            job_titles_lst.append(job_title[i].text)
            job_skills_lst.append(job_skill[i].find_all('div')[1].text)
            company_name_lst.append(company_name[i].text[:-2])
            location_lst.append(location[i].text)
            date_posted_lst.append(date_posted[i].find('div').text)
            job_link_lst.append("https://wuzzuf.net"+job_title[i].find('a').attrs['href'])

        # some logic to terminate the while loop
        jobs_founded  = soup.find('strong').text
        founded_pages = int(jobs_founded) // 15
        if page_num  > founded_pages:
            print("Pages ended!")
            print(f"{jobs_founded} jobs founded!")
            break
        
        page_num += 1
        print("page switched")
    except:
        print("Error Occurred")
        break


# get the current date and time
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# specify the name of the csv file using the current time
filename = "scraped_data " + search_sentence + " " + current_time + ".csv"
file_list = [job_titles_lst, company_name_lst, location_lst, date_posted_lst, job_skills_lst, job_link_lst]
exported = zip_longest(*file_list)

def export_csv(filename, exported):
    with open(f'{csv_dir}/{filename}', 'w') as output:
        wr = csv.writer(output)
        wr.writerow(['Job Title', 'Company Name', 'Location List', 'Post Date','Job Skills', 'Job Link'])
        wr.writerows(exported)
        print("File Created Successfully")

export_csv(filename, exported)

