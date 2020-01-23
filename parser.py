from bs4 import BeautifulSoup
import csv

with open ('UofO_Courses.html') as html_file:
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
    if course.find('p', class_='courseblockdesc noindent') == None:
        course_description = ""
    else:
        course_description = course.find('p', class_='courseblockdesc noindent').text

    csv_writer.writerow([course_title.encode('utf-8', errors='ignore'), course_description.encode('utf-8', errors='ignore')])

# Export to html
f = open("parsed_UofO_Courses.html", "w")
for course in soup.find_all('div', class_='courseblock'):
    
    course_title = course.find('p', class_='courseblocktitle noindent')
    course_description = course.find('p', class_='courseblockdesc noindent')

    f.write(str(course_title))
    f.write(str(course_description))
f.close()

   