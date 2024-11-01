Explanation of the Code
WebDriver Setup:

We start by setting up the Chrome WebDriver using chromedriver.exe, specifying its path to ensure compatibility and smooth running of the browser automation.
Opening the Website:

The website URL is loaded with driver.get(), specifically targeting CityGross’s "matvaror" page, which lists the various products in different categories.
Handling Cookie Consent:

A try-except block is used to handle cookie consent by clicking the "Allow all" button if it appears. The text is in Swedish ("Tillåt alla"), as it matches the website's language, ensuring the cookie pop-up is closed before proceeding.
The presence of this handler prevents errors in case the pop-up interferes with further actions.
CSV File Setup for Data Export:

A CSV file is opened with UTF-8 encoding (including a BOM for Excel compatibility), allowing us to store the extracted data in a structured format.
We initialize the CSV headers as "Category," "Name," "Description," and "Price."
Defining Categories for Testing:

The code specifies a list of three categories to limit the data extraction, speeding up testing while maintaining code flexibility. By focusing on only three categories and the first two pages, we ensure the code's functionality without extended runtime.
Each category is defined by a name and a CSS selector, which we use to locate it in the page's side menu.
Category Selection and Scrolling:

The code scrolls down to ensure the category menu is visible, particularly useful for categories that may be out of view initially.
For each category, the code then scrolls to its specific position in the side menu, guaranteeing it is centered in view and clickable.
Navigating Pages in Each Category:

For each category, the code captures the product information on the first two pages only. This limitation is primarily for testing efficiency, reducing load time while verifying the core functionality.
To capture more pages, simply change the range in the loop. This flexibility allows the script to be easily extended to all pages if needed.
Extracting Product Data:

The script identifies each product card on the page, extracting details such as the product name, description, and price.
For the price, it tries multiple selectors to ensure all potential formats are handled, with the latest selector accounting for cases specific to member-only pricing or special promotions.
Navigating Between Pages:

After completing data extraction on the first page, the code attempts to click the "Page 2" button to load the next page. We limit navigation to the first two pages for quicker testing.
A brief pause is added after each page load to ensure all elements are fully loaded before extraction.
Completing Extraction and Cleanup:

After each category’s data is extracted, the code moves on to the next category. Once all specified categories are processed, the browser is closed, and a confirmation message is displayed.
Testing and Flexibility
Limiting to Three Categories and Two Pages:

In testing, extracting only three categories and limiting the extraction to the first two pages provided a fast way to verify the code’s correctness. This approach ensures all critical parts of the code work without the overhead of scraping the entire website.
The code can be easily adjusted to extract more categories or pages as needed. To scrape all categories, add them to the categories list. For more pages, modify the page loop.
Cookie Consent in Swedish:

The cookie button uses Swedish ("Tillåt alla") to match the website's language. This ensures the button is located correctly and clicked regardless of browser localization, enhancing reliability when running on different systems or regions.
