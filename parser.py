from bs4 import BeautifulSoup
import csv

with open ('./corpus/UofO_Courses.html') as html_file:
    soup = BeautifulSoup(html_file, 'html5lib')

csv_file = open('parsed_UofO_Courses.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Course Title', 'Course Description'])


# Export to CVS
for course in soup.find_all('div', class_='courseblock'):
    if course.find('p', class_='courseblocktitle noindent') == None:
        course_title = ""
    else:
        course_title = course.find('p', class_='courseblocktitle noindent').text
        course_title = " ".join(course_title.split())
        if ("3 crédits" in course_title) or ("è" in course_title):
            continue
    
    if course.find('p', class_='courseblockdesc noindent') == None:
        course_description = ""
    else:
        course_description = course.find('p', class_='courseblockdesc noindent').text
        course_description = " ".join(course_description.split())
        

    csv_writer.writerow([course_title, course_description])
csv_file.close()