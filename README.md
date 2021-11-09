# Top Shot Account Scraper To CSV

I built this to help my friends and I better track the NBA Top Shot Moments we had in our 3 accounts. The program starts by asking for a Top Shot username. It then uses Selenium to open and autoscroll through the account page to grab all the URLs of the Moments in each account. Each URL is the scraped using Beautiful Soup to extract pertinent information for each Moment. This info is then exported to a CSV file for data analytics purpose.
