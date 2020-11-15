import app

def main():
	inp = input("\n<< Digiter - Webversion (https://digiterbee.herokuapp.com) >> \n 1 > To Generate Meta tag for website headers \n 2 > To Generate Sitemap.xml \n 3 > To Check Keyword Density \n 4 > To Check Google Rank\n 5 > To Generate robots.txt \n 0 > To Exit ->")
	if (inp=="1"):
		website=input("-> Enter your website : ")
		app.getMeta(website)
		main()
	elif(inp=="2"):
		website=input("-> Enter your website : ")
		app.sitemap_genarator(website)
		main()
	elif(inp=="3"):
		website=input("-> Enter your website : ")
		app.keyword_density(website)
		main()
	elif(inp=="4"):
		url=input("-> Enter your Website : ")
		keyw=input("-> Enter your Keyword : ")
		device=input("-> Enter 'desktop' or 'mobile' : ")
		app.rank(url,keyw,device)
		main()
	elif(inp=="5"):
		agent=input("-> Enter Agent name or * : ")
		disallow=input("-> Enter Link not to allow : ")
		allow=input("-> Enter Link to allow : ")
		site=input("-> Enter your sitemap.xml link")
		robots(agent,disallow,allow,site)
		main()
	elif(inp=="0"):
		exit()
	else:
		print("Kindly Enter allowed input value.")
		main()

if __name__ == "__main__": 
    main()