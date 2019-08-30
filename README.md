# Salesforce

Don't worry this stuff will be commented at some point by me. I'm creating this small readme and will update over the weekend after I help some people move stuff in. 

#### config.py

Since this is a private repo, I included this as it has all the necessary information for logging into salesforce through the simple salesforce api. Change credentials as needed!

#### sftest.py

I created this file as a way to delete Clinics (opportunities) and Contacts programatically so that I could test other functionalities of the salesforce api. 

#### salesforce.py

The bread and butter of the whole operation. With this, you are able to create contacts and clinics (opportunities) 1 by 1, or you can read in a csv. Either one is fine. The Clinics2016-20171-2.csv and 1-3.csv are the formats I followed. The other ones will not work. There is a way to automate that as well, but I felt having a single system that was the same would be the best option and the most efficient. We can figure this out throughout the semester though. 

#### ids.csv

This csv contains a Full Name: User ID format that we can use to assign owners to in salesforce.py. ids1.csv has the User Id: Full Name format that can be used to query and look up users. Grabbing id's and looking them up is still rough and hasn't been implemented correctly yet. 

I think that is all in terms of the py files and their functionalities. As I mentioned earlier, I'll comment my code as best as possible so that anyone looking at it can pick it up and do as they need to it. Thank you for the great summer and I hope to continue working with yall in the fall. 
