# **bioRxivbot**

A twitter bot from [@MiriukaLab](https://twitter.com/MiriukaLab) for filtering just published  [@bioRxivpreprint](https://twitter.com/biorxivpreprint) papers according to keywords. 


**Purpose:** A bot that checks what papers were published the day before and tweets them if some keywords are found in the abstract. Ideally, you should set a crontab for a scheduled activation and tweeting in a server. Alternatively, just run it everyday :(

## Set up

1. Create a twitter account. 
2. Apply for a [developers twitter account](https://developer.twitter.com/en)
3. Get the four long complex weird keys and add them to the credential.txt file. Replace the fake ones provided. 
4. The idea is that your bot will tweet what you are interested in. So, write down your keywords in the search.txt file. For example, you can write *(pluripotent stem cell OR embryonic stem cell) AND (microRNA OR miRNA)*. Note that the search is case-insensitive.
5. [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) it to activate it, i.e., every morning and check any new interesting paper with breakfast.



#### Authors: Felipe Miriuka and Santiago Miriuka
