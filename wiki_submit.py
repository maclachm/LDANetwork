import wikipedia
f2=open('t.txt','r')
for article in f2:
#	print article
	pcontent= wikipedia.page(title=article,pageid=None,
	auto_suggest=True, redirect=True, preload=False).content
	pcontent=pcontent.encode('ascii','ignore')
	saved=(article)
	f=open(saved,'w')
	print >>f,pcontent
	f.close()
f2.close()