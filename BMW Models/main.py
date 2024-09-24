import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# set up web driver
def setup_driver():
    driver = webdriver.Chrome()
    return driver

# Download the HTML content of a page and save it to a file.
def download_html_page(driver, url, page_name, directory):
    driver.get(url)
    page_source = driver.page_source
    file_path = os.path.join(directory, f'{page_name}')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page_source)
    print(f"Saved: {file_path}")

# to extract all the models' link
def extract_links_and_names(driver, class_name, css_selector):
    elements = driver.find_elements(By.CLASS_NAME, class_name)
    links = []
    page_names = []
    for element in elements:
        link_element = element.find_element(By.CSS_SELECTOR, css_selector)
        href = link_element.get_attribute('href')
        name = link_element.text
        links.append(href)
        page_names.append(name)
    return links, page_names

# defining a main function
def main():
    # setup driver
    driver = setup_driver()
    try:
        # defining the main url and downloading it
        main_url = 'https://www.bmwusa.com/all-bmws.html'
        download_html_page(driver, main_url, page_name='main_page.html', directory=output_dir)

        # getting ready to extract sub page links    
        driver.get(main_url)
        links, page_names = extract_links_and_names(driver, "model-s-hero", ".model-s-hero__details-title.headline-5 a")

        # downloading the sub pages (all models of bmw in html)
        for link, name in zip(links, page_names):
            page_name = f'{name}.html'
            download_html_page(driver, link, page_name, output_dir)
    finally:
        # closing the web driver
        driver.quit()


if __name__ == "__main__":

    # Create a directory to save HTML files
    output_dir = "BMW_model_pages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    main()
