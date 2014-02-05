from bs4 import BeautifulSoup
import urllib
import re
import os

# Base url for buldings urls
baseurl = "http://fs-uk.com"

# Dirty hack : all mod for farming sim are in category 1 (meta category)
modsurl = "http://fs-uk.com/mods/list/category/1/"

# Local directory where all category directories will be created
#	and mods downloaded
localdir = "D:\\fsuk2013\\"

#soup = BeautifulSoup(open("fsuk.html"))

# Regex for finding tags
isfs2013 = re.compile("For Farming Simulator 2013")
isgold = re.compile("gold")
isnottitle = re.compile("^((?!modTitle).)*$")
isdl = re.compile("Download")
iszip = re.compile("zip$")


# Mods list
mods = []
externalmods = []

# Dirty hack all mods for fs2013 are in the 16th first pages
#	(of 108 at the time I'm writing this)
#	Should parse first page to get max page number (much longer)
#	and need to stop parsing when 2~3 pages do not contain fs2013 mods
for pagenum in xrange(16,0,-1):
	# Going backward to get oldest mods first
	modsurlwithpage = modsurl + str(pagenum)
	soup = BeautifulSoup(urllib.urlopen(modsurlwithpage).read())
	for td in soup.find_all("td",class_="info"):
		# Searching for the fs 2013 mods
		foundtext = False
		for data in td.contents:
			if data.string:
				#print(data.string)
				#print(type(unicode(data.string)))
				if isfs2013.search(unicode(data.string)):
					foundtext = True
					break
		if foundtext:
			# Searching for gold mods
			foundgold = False
			for cl in td.parent.find_next_sibling("tr").td.div.get("class"):
				if isgold.search(cl):
					foundgold = True
					break
					
		if foundtext and foundgold:
			# Get all data (mod and category)
			modurl = baseurl + td.a.get("href")
			
			# Get and parse the mod page
			modsoup = BeautifulSoup(urllib.urlopen(modurl).read())
			
			modsoupdetail = modsoup.find("div",class_="titleBox")			
			modname = modsoupdetail.find("p",class_="modTitle").string
			# Category info
			modcategorylink = modsoupdetail.find("p",class_=None).a
			modcategoryname = modcategorylink.string
			modcategoryurl = baseurl + modcategorylink.get("href")
			
			# Last item of mod category url is category number
			modcategorynum = modcategoryurl.rsplit("/",1)[1]
			# Get the "manual download" zip link
			ziplink = modsoup.find("h2",text=isdl).find_next_sibling("div").find("a",href=iszip)
			if ziplink:
				# All mod do not have a manual zip
				modfile = baseurl + ziplink.get("href")
				
				# Debug infos
				#print(modname + " in \"" + modcategoryname + "\" (Cat #" + modcategorynum + " - " + modcategoryurl + ")\" from " + modfile)
				#print("xxxxxxxxxxx\n")
				
				# Get and parse the download page
				dlpagesoup = BeautifulSoup(urllib.urlopen(modfile).read())
				zipdirectlink = dlpagesoup.find("div",class_="content").p.a
				# Should always match
				if zipdirectlink:
					directlink = zipdirectlink.get("href")
					# Debug links (direct download)
					#print(directlink)
					# Create a list of dict for future uses
					mods.append({"name":modname,
								 "category":{"name":modcategoryname,"num":modcategorynum,"url":modcategoryurl},
								 "link":directlink})
			else:
				externaldownload = modsoup.find("h2",text=isdl).find_next_sibling("div").a
				externaldownloadlink = baseurl + externaldownload.get("href")
				externalmods.append({"name":modname,
								 "category":{"name":modcategoryname,"num":modcategorynum,"url":modcategoryurl},
								 "link":externaldownloadlink})

# Total number of external mods
nbextmod = len(externalmods)
# Processing of external mods
print "Following mods are external to fs-uk :"
for i in range(nbextmod):
	extmod = externalmods[i]
	print "Mod %s : %s" % (extmod["name"], extmod["link"])
	print "\n"

# Added new line for clarity when reading the output	
print "\n"

# Total number of mods
nbmod = len(mods)
# Processing of mods
for i in range(nbmod):
	mod = mods[i]
	# Basic counter
	print "Processing mod %i of %i" % (i+1, nbmod)
	# Debug mod info
	#print(mod["name"] + " (" + mod["link"] + ") in " + mod["category"]["name"])
	
	# Build the path with the category name
	# ! Not tested with names containing spaces
	workdir = localdir + mod["category"]["name"] + "\\"
		
	url = mod["link"]
	# Files downloaded will have the zip name
	file_name = workdir + url.split('/')[-1]
	
	# Create directories if necessary
	d = os.path.dirname(file_name)
	if not os.path.exists(d):
		os.makedirs(d)

	# Open download link		
	u = urllib.urlopen(url)
	# Open our local file
	f = open(file_name, 'wb')
	
	# Get meta info to get the file size
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)
	
	# Could optimize by checking if file with same name and target size already here
	
	# Download sequence
	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break
	
		file_size_dl += len(buffer)
		f.write(buffer)
		# Progress bar with size and advancement
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		print status,
	
	f.close()
	# Added new line for clarity when reading the output
	print "\n"

