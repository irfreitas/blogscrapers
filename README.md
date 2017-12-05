# blogscrapers

This package is based off the original scripts located at "jbharwani/blogscrapers".  The current status of this repo demonstrates scraping tools for blogspot and typepad style blogs, but can be adapted for use with any blog with the change of a few xpaths. The updated example scrapers use scrapy, beautifulsoup (works best with lxml also installed), and a working knowledge of xpath.

Need to install scrapy and beautifulsoup and lxml
	pip install scrapy
	pip install beautifulsoup
	pip install lxml

This package provides python scripts that can be used to scrape every archived blog posts from a blog. The scripts make the assumption that the sites follow a certain HTML structure which may vary depending on the theme and blogging platform. The following sites are examples of compatible blogs on blogspot and typepad. 

blogspot - "http://autismschmatism.blogspot.com/"
typepad - "http://ashleymorris.typepad.com/"


What is important is the xpath for the archives on the main page and the HTML tags for each post. Just modify the xpath in the scraper file to navigate to the archive links and scrape parts. Firefox and the firebug package will be very useful to this.

To scrape the blog x into a file titled "data.json":
	1. Open appropriate scraper and make changes as commented on the top of the file
	2. Go to the command line and navigate to the correct directory
	3. Run the following command
		scrapy runspider scraper.py -o data.json
