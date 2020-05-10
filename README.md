
## SECTION 1 : PROJECT TITLE
## SG Trippingo - Singapore Attractions Recommender & Itinerary Planner

<img src="TripAtUs\static\assets\img\portfolio\BgLogin.jpg"
     style="float: left; margin-right: 0px;" />


---
## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Imagine yourself planning for your next overseas trip to Singapore, doing countless hours of research on the attractions to visit and getting vexed over the perfect hotel for your family. The task of planning a trip can become extremely daunting for tourists who need to plan from selecting the attractions, booking the accommodations and charting their daily itinerary.

Indeed, according to the 2018 Q4 report published by the Singapore Tourism Board, the tourism sector had achieved record highs in International Visitor Arrivals and Tourism receipts for the third consecutive year. With the exponential increase in tourists to Singapore, the primary challenge of making full use of their trips while taking into consideration their limited time here is enormous. Based on our research, an average tourist usually takes up to 12 hours to plan their trips. Currently, there exists a sizable market gap in the tourism industry with modern travel tech players like Traveloka and Agoda provide limited active recommendations whilst the more traditional travel agencies tend to have a strict adherence to schedule and lack the much-desired flexibility. From our initial survey, we discovered a strong demand for a middle ground that combines the flexibility of planning your own trip yet provides active recommendations on places to visit. 

These thought-provoking discoveries led our team to explore an efficient recommendation system which allows tourists to effectively plan their trip in Singapore. Leveraging on our core competencies in intelligent reasoning, cognitive and optimisation systems, we have developed a dynamic itinerary planner which optimises both the hotel location as well as daily itinerary for our end users, thereby relieving them from the painstaking planning process. Our simple and intuitive front-end user interface hosts a dropdown form for tourists to input their preferences for common categories of attractions in less than 10 seconds. Linear programming optimization solver optimizes the attractions based on earlier defined user preferences and curates a list of attractions for our end users. With attractions selected, our end users can now book their recommended hotel, obtained by minimizing the distance to each of the attractions. At the heart of our itinerary planning process is a hybrid reasoning engine that combines a greedy best first search tree with the permutations of genetic algorithms. This computationally intensive task is executed asynchronously. All these with an aim of allowing our end users to relax and to receive a specially curated and customised itinerary sent directly for their use. 

But wait, theres more. We do not just stop at planning as we understand tourists desire a dynamic planner that can plan on the go. As the founder and CEO of Amazon, Jeff Bezos puts it “Any plan won't survive its first encounter with reality. The reality will always be different”. Our humanoid telebot accompanies our tourists throughout their trip in Singapore and dynamically plans through any changes in the schedule or preference. Our aim at Trip@Us is to be your friendly trip recommender system that follows you throughout your journey.


---
## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID  | Work Items |
| :---------------- |:---------------:| :-----|
| Mehta Vidish Pranav | A0213523U  | Project Leader, Initial proposal, mid project presentation and final project documentation. Core Programming and algorithm development (Attraction Selection, Book My Hotel, Plan My Trip and Telebot). Django UI Interface developer & Django API developer. Celery and rabbitmq integration to ubuntu iss-vm. Project Video|
| Anandan Natarajan | A0213514U  | Project Management, Proposal Expansion, Data Sourcing, Data Massaging, Prototype design, System Architecture, Database Design, Flow Diagrams, Testing,  Implementation & Testing, Project Management & Documentation|
| Ankeit Taksh| A0213496B   |  Proposal Expansion, System Architecture, Environment Engineering & DevOps,  Programming and algorithm development (Telebot). Django UI Interface developer. Implementation & Testing,, Association Mining, Association Knowledge Representation, Association Recommendation User Interface|
| Wang Kuan-Kai | A0198539H  | Project Management, Proposal Expansion, Data Sourcing, Data Massaging, Prototype design,  Mid project presentation and final project documentation Implementation & Testing, Project Management & Documentation|


---
## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[Project Video](https://www.youtube.com/watch?v=uRw_DnBMakg)


---
## SECTION 5 : USER GUIDE

`<Github File Link>` : /UserGuide folder

### [ 1 ] Run Trippingo (Backend)

> Download jar file from latest [release](https://github.com/vid1994/Trip-Us) into a new project directory

> Navigate to project directory and execute the command below in command line:

```bash
python main.py runserver
```

> API will be available on 8000 port of the localhost

### [ 2 ] Run Trippingo-Web (Frontend)

> Use the package manager [pip](https://pip.pypa.io/en/stable/) to install application dependencies

```bash
pip install -r requirements.txt
```

> Start the Django application from [Trippingo-Web project](https://github.com/vidur6789/trippingo-web) directory in terminal

```bash
python manage.py runserver
```

---
## SECTION 6 : PROJECT REPORT / PAPER

`<Github File Link>` : <https://github.com/vid1994/Trip-Us>

---
## SECTION 7 : MISCELLANEOUS

### AttractionsData.xlsx
* Singapore attractions data scraped from data.sg (Govt Data Source File)
* Includes basic information and reviews, which were subsequently used in our system
### HotelList.xlsx
* Singapore Hotel data scraped from data.sg (Govt Data Source File)
* Includes basic information and reviews, which were subsequently used in our system