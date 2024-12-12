import os
from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup

html_report = fr'{Path.home()}\OneDrive - Micro systemation AB\Desktop\Test_cases_TestRail_xam\report_all_test_10_24.html'

def parse_html_file(html_report):
    html_report_path = os.path.abspath(html_report)
    file_url = f'file:///{html_report_path}'
    driver = webdriver.ChromiumEdge()
    # Open the HTML report
    driver.get(html_report)
    driver.implicitly_wait(10)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.select('tr.collapsible')
    test_names = []
    durations = []
    Results = []
    for row in rows:
        test_name_element = row.find('td', class_='col-testId')
        duration_element = row.find('td', class_='col-duration')
        results_element = row.find('td', class_='col-result')
        if test_name_element and duration_element:
            test_names.append(test_name_element.get_text(strip=True))
            durations.append(duration_element.get_text(strip=True))
            Results.append(results_element.get_text(strip=True))
    driver.quit()
    return test_names, durations, Results


#the main test to test the method howevr this method is used for all apis to identify whether the test passed or failed
if __name__ =="__main__":
    test_names, durations, Results = parse_html_file(html_report)
    # Output the extracted data
    print("Test Names:", test_names)
    print("Durations:", durations)
    print("Results", Results)

# Close the browser
