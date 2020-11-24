# **bioRxivbot**

A twitter bot from [@MiriukaLab](https://twitter.com/MiriukaLab) for filtering just published  [@bioRxivpreprint](https://twitter.com/biorxivpreprint) papers according to keywords. 


**Purpose:** A bot that checks what papers were published the day before and tweets them if some keywords are found in the abstract. Ideally, you should set a crontab for a scheduled activation and tweeting in a server. Alternatively, just run it everyday :(

## Installation


```bash
git clone https://github.com/Miriu/bioRxivbot.git
```

### Dependencies

* python >=3.7
* Tweepy >= 3.9.0
* requests >= 2.25.0

Not checked in older versions. 

## Set up

1. Create a twitter account. 
2. Apply for a [developers twitter account](https://developer.twitter.com/en)
3. Get the four long complex weird keys and add them to the **credential.txt** file. Replace the fake ones provided. 
4. The idea is that your bot will tweet what you are interested in. So, write down your keywords in the **search.txt** file. For example, you can write __*(pluripotent stem cell OR embryonic stem cell) AND (microRNA OR miRNA)*__. Boolean operators supported are AND, OR, and NOT. Note that the search is case-insensitive. Do not use any quoation marks. Suuports the use of parenthesis for term aggregation. 
5. You can then use [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) to activate it, i.e., every morning and check any new interesting paper posted in bioRxiv with breakfast.



#### Authors: [Felipe Miriuka](https://github.com/Miriu/) and [Santiago Miriuka](https://github.com/sgmiriuka/)
