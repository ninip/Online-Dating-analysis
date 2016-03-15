# -*- coding: utf-8 -*-
# Final project
# CSE 160
# Sidney Sullivan & Naomi Provost
# 
# data from: http://www.pewinternet.org/datasets/may-2013-online-dating-prelim/


import csv
import operator

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# A dictionary the references what each website is to its recorded number in 
# the data set.
website_ref = {'1': 'Match.com', '2': 'eHarmony', '3': 'OK Cupid', '4': 'Plenty of Fish', '5': 'Christian Mingle', '6': 'True.com', '7': 'Zoosk',
                '8': 'J Date', '9': 'Date Hookup', '10': 'Ashley Madison', '11': 'Facebook', '12': 'Twitter', '13': 'Adult Friend Finder', 
                '14': 'Blackplanet', '15': 'Chemistry.com', '16': 'Craigslist', '17': 'Other', '98': 'Unknown', '99': 'Refused'}

# A dictionary the references what each app is to its recorded number in the 
# data set.
app_ref = {'1': 'Match.com', '2': 'eHarmony', '3': 'OK Cupid', '4': 'Tinder', '5': 'Grindr', '6': 'Blendr', '7': 'Lets Date',
                '8': 'Plenty of Fish', '9': 'How About We', '10': 'Meexo', '11': 'Flirtomatic', '12': 'JDate', '13': 'Jazzed', 
                '14': 'Skout', '15': 'SpeedDate', '16': 'Other', '17': 'Multiple Response', '18': 'Not Valid', '98': 'Unknown', '99': 'Refused'}

###########################Gets demographics count##############################
def demographic_count(dict_demo):
    ''' 
    Parameters: 
        dict_demo: a dictionary that maps ID numbers to list of strings, where
        item[0] of the list is sex, [1] is age, [2] is income, [3] is hispanic,
        [4] is race. 
        ['sex', 'age', 'inc', 'hisp', 'race']
    Returns:
        none
    Prints the percentage amount for each demographic.    
    '''
    # initialize counters
    female = 0
    male = 0
    below_twentyfive = 0
    thirtyfive = 0
    fortyfive = 0
    fiftyfive = 0
    older_fiftyfive = 0
    less20k = 0 # 1-2
    less40k = 0 # 3-4
    less75k = 0 # 5-6
    less100k = 0 # 7
    more100k = 0 # else
    hisp = 0
    white = 0
    black = 0
    asian = 0
    mixed = 0
    native = 0
    other = 0
        
    # Loops item through dict_demo.values, which is a list of lists.
    for user_demo in dict_demo.values():
        # counts male or female
        if user_demo[0] == '1':
           female += 1 
        else:
            male += 1
    
        # counts age groups
        user_age = int(user_demo[1])
        if user_age <= 25:
            below_twentyfive += 1
        elif user_age <= 35:
            thirtyfive += 1
        elif user_age <= 45:
            fortyfive += 1
        elif user_age <= 55:
            fiftyfive += 1
        # data set responses 98 and 99 are irrelevant
        elif user_age <= 97: 
            older_fiftyfive += 1    
      
        # counts income categories
        user_income = int(user_demo[2])
        if user_income <= 2:
            less20k += 1
        elif user_income <= 4:
            less40k += 1
        elif user_income <= 6:
            less75k += 1
        elif user_income == 7:
            less100k += 1
        elif user_income <= 9:
            more100k += 1
        
        # counts race demographics
        demo_race = user_demo[4]
        if user_demo[3] == '1': 
            hisp += 1
        if demo_race == '1':
            white += 1
        elif demo_race == '2':
            black += 1
        elif demo_race == '3':
            asian += 1
        elif demo_race == '4':
            mixed += 1
        elif demo_race == '5':
            native += 1
        else:
            other +=1
    
    def percent(num):
        ''' 
        Helper function parameters:
            takes in a number
        Returns:
            the percentage of the total
        '''
        return round((num / float(len(dict_demo.values())) * 100),2)

    print 'Percent of Sex Demographics'
    print 'male:', percent(male), 'female:', percent(female)
    
    print 'Percent of Age Demographics'
    print 'age 18-25:', percent(below_twentyfive), 'age 26-35:', percent(thirtyfive), 'age 36-45:', percent(fortyfive), 'age 46-55:', percent(fiftyfive), 'age 55+:', percent(older_fiftyfive)
    
    print 'Percent of Income Demographics'
    print 'less than 20k:', percent(less20k), '20k-40k:', percent(less40k), '40k-75k:', percent(less75k), '75k-100k:', percent(less100k), 'more than 100k:', percent(more100k)        

    print 'Percent of Race/ Ethnicity Demographics'
    print 'Hispanic:', percent(hisp), 'White:', percent(white), 'Black:',  percent(black), 'Asian:', percent(asian), 'Mixed:', percent(mixed), 'Native American:', percent(native), 'other:', percent(other) 

    assert(percent(male) + percent(female) == 100)
  
############################Find most popular dating website####################

def popularity_dict(pop_dating_lst):
    '''
    Parameters:
        pop_dating_lst: a list of websites and apps
    Returns:
        dictionary that maps number corresponding to website/app with counted 
        sum of each repeated result
    '''
    # Create a new list with only if data set response is a digit.
    digit_lst = [item for item in pop_dating_lst if item.isdigit()] 
    # Creates empty dictionary that maps num corresponding website/app to count.
    counts = {}
    for response in digit_lst:
        # counts how many times each number is mentions in data set responses, 
        # or returns 0 if not in list
        counts[response] = counts.get(response, 0) + 1  
    return counts
    
def combine_dictionaries(value_dict, ref_dict):
    '''
    Parameters:
        value_dict = dictionary that maps number corresponding to website/app 
            with counted sum of each repeated result
        ref_dict = dictionary that maps number corresponding to website/app to 
           actual name of webiste/app
   Returns:
       a list of tuples where the first response is the amount of website/app 
       is counted, and the second response is the name of app/website
    '''
    for key in value_dict:
        if key in ref_dict:
            #combine value with name
            value_dict[key] = (ref_dict[key], value_dict[key]) 
    #return list of tuples of value and name
    return value_dict.values() 
    
############Find Details on LGBT vs Straight Usage of Dating Websites###########

def lgtb_percent_dict(dict_lgbt):
    '''
    Parameters:
        dict_lgbt: takes in a dictionary mapping ID to data set response 
        regarding lgbt survey questions, where item[0] is sexual orientation
        item[1] and item[2] are response to using either website or dating app
    Returns:
        none
    Prints out count of responses, and calculates percentage
    '''
    # initialize counter
    count_lgbt = 0
    count_straight = 0
    hetro_online_use = 0
    lgbt_online_use = 0
    
    for response in dict_lgbt.values():
        sexual_orientation = response[0]
        # responder has used a website or dating app
        online_use = response[1] == '1' or response[2] == '1' 
        # counts responder for heterosexual or straight
        if sexual_orientation == '1': 
            count_straight += 1
            if online_use:
                hetro_online_use += 1
        # counts responder for gay, lesbian or bisexual
        elif sexual_orientation == '2' or sexual_orientation == '3': 
            count_lgbt += 1
            if online_use:
                lgbt_online_use += 1
    # Calculates percentage of responders who identify as lgbt.
    percent_lgbt_use = round((float(lgbt_online_use) / count_lgbt * 100),2)
    # Calculates percentage of responders who identify as straight.
    percent_straight = round((float(hetro_online_use) / count_straight * 100),2)

    print "number of LGBT responders:", count_lgbt, ", use online dating:", lgbt_online_use, ", percent:", percent_lgbt_use
    print "number of straight responders:", count_straight, ", use online dating:", hetro_online_use, ", percent:", percent_straight


##########################Check Relationship Status#############################
def check_relationship(relan_dict):
    '''
    Parameters: 
        dictionary item "0" is in a relationship, "1" is single if response is 
        two, "2" is single and looking.
    Returns:
        none
    Prints:
        A count of how many people are single, single and looking for a 
        relationship, or in a relationship.
    '''
    # initialize counters
    single = 0
    relationship = 0
    looking = 0
    
    for response in relan_dict.values():
        if response[0] == '1' or response[0] == '2' or response[1] == '1': # responder is in a relationship
            relationship += 1
        # responder is single
        elif response[1] == '2': 
            single += 1
            # responder is single and looking
            if response[2] == '1':
                looking += 1
                
    print "Single:", single, "& looking for a relationship:", looking 
    print "In a relationship:", relationship
    
#########################Text/Email Breakup Information#########################
def text_break(breakup_dict):
    '''
    Parameters:
        the breakup_dict where value "0" is responder sent a text/email and "1" is
        repsonder received a text/email.
    Returns:
        list where value 0 refers to the number of people who have sent a breakup 
        text/email and value 1 refers to the number of people who have received a 
        breakup text/email.
    '''
    # initialize counters
    sent_text = 0
    received_text = 0
   
    for response in breakup_dict.values():
        if response[0] == '1':
            # responder sent a text/email to break up
            sent_text += 1 
        if response[1] == '1':
            # responder received a text/email to break up
            received_text += 1 
    
    return [sent_text, received_text]
    
############################Text/EmailBreakup Graph ############################

def plot_text_break(text_break_data):
    '''  
    Parameters:
        the text_break_data, which is actually equivalent to the breakup_dict, 
        where value "0" is responder sent a text/email and "1" is repsonder received a 
        text/email.
    Returns:
        Graphs the frequencies of the sent/received breakup text/email for the dating data.
        The function should return None. 
    '''
    Transfers = [1, 2]
    freqs = text_break_data
    LABELS = ["Sent", "Received"]
    # width = .5
    width = .5
    plt.title('Breakup via Text/Email')
    plt.xlabel('Text/Email Transfers')
    plt.ylabel('Frequency of Texts/Emails')
    plt.bar(Transfers, freqs, width, align='center', color='m')
    plt.xticks(Transfers, LABELS)
    plt.savefig("text_email_breakups.png")
    # plt.show()
    plt.clf()
    
####################Expeierences with Online Dating#############################

def exp_dict(exp_list, first_age, second_age):
    ''' 
    Parameters:
        exp_list = a list of values where item "0" is age, "1" is responder 
        tried online dating, "2" is responder met current partner online, "3"
        is responder has been harrased through online dating, and "4" is 
        responder has discovered a misrepresented online dating profile. 
        first_age = lower bound age
        second_age = upper bound age
    Returns:
        dictionary that maps age groups in bound to corresponding responsing
    '''
    map_value = {}
    for response in exp_list:
        age = int(response[0])
        if age >= first_age and age <= second_age:
            if response[1] == '1':
                map_value["responder tried online dating"] = map_value.get("responder tried online dating", 0) + 1 
            elif response[2] == '1':
                map_value["relationship met partner online"] = map_value.get("relationship met partner online", 0) + 1
            elif response[3] == '1':
                map_value["responder felt harassed online"] = map_value.get("responder felt harassed online", 0) + 1
            elif response[4] == '1':
                map_value["responder found misrepresented profile"] = map_value.get("responder found misrepresented profile", 0) + 1
            elif response[2] != '1':
                map_value["relationship met partner online"] = map_value.get("relationship met partner online", 0)
    return map_value

def print_experience(dating_experience):
    '''
    Parameters:
        exp_dict = function which takes in list of values, and two ages then 
        returns dictionary
    Returns:
        none
    Prints: 
        each age group, and the dictionary of expience corresponding to each
    '''
    print "age group between 18 to 25:", exp_dict(dating_experience.values(), 18, 25)
    print "age group between 26 to 35:", exp_dict(dating_experience.values(), 26, 35)
    print "age group between 36 to 45:", exp_dict(dating_experience.values(), 36, 45)
    print "age group between 46 to 55:", exp_dict(dating_experience.values(), 46, 55)
    print "age group 56 and over:", exp_dict(dating_experience.values(), 56, 97) #98 and 99 are not relevant
    
    
def age_list_experience(dating_exp):
    ''' helper function used for plotting
    Parameters:
        dating_exp: dictionary of experiences that takes in age groups and returns dictionary
    Returns:
        list of dictionaries corresponding to age groups and dating experiences
    '''
    age_group1 = exp_dict(dating_exp.values(), 18, 25).values()
    age_group2 = exp_dict(dating_exp.values(), 26, 35).values()
    age_group3 = exp_dict(dating_exp.values(), 36, 45).values()
    age_group4 = exp_dict(dating_exp.values(), 46, 55).values()
    age_group5 = exp_dict(dating_exp.values(), 56, 97).values() 
    
    return [age_group1, age_group2, age_group3, age_group4, age_group5]


###################Dating Expeierences Graph####################################
 
def plot_exp(exp_list):
    
    ''' 
    Parameters:
        the exp_data, which is actually equivalent to the 
        age_list_experience(dating_experience)
    Returns:
        Graphs the frequencies responders of responder experiences based on 
        age groups. 
        The function should return None.
    code from: https://gist.github.com/ctokheim/6435202a1a880cfecd71 
    '''    
    
    #creates arrays for each age groups, values corresponding to experiences
    age_group1 = np.array(exp_list[0])
    age_group2 = np.array(exp_list[1])
    age_group3 = np.array(exp_list[2])
    age_group4 = np.array(exp_list[3])
    age_group5 = np.array(exp_list[4])
    
    #Labels each value in individual array
    responses = ['Tried Online Dating', 'Been Harrassed', 'Found Relationship', 'Misrepresented Profile']
    
    with sns.axes_style("white"):
        sns.set_style("ticks")
        sns.set_context("talk")
    
        # plot details
        bar_width = 0.35
        line_width = 1
        opacity = 0.7
        first_bar_positions = np.arange(len(age_group1))
        second_bar_positions = first_bar_positions + bar_width
    
        # make bar plots for each age group
        age_group1_bar = plt.bar(first_bar_positions, age_group1, bar_width,
                                color='#9400D3',
                                label='Age 18-25')
        age_group2_bar = plt.bar(first_bar_positions, age_group2, bar_width,
                                bottom=age_group1,
                                alpha=opacity,
                                color = '#0000FF',
                                edgecolor='#000000',
                                linewidth=line_width,
                                label='Age 25-35')
        age_group3_bar = plt.bar(first_bar_positions, age_group3, bar_width,
                                bottom=age_group2+age_group1,
                                alpha=opacity,
                                color = '#00FF00',
                                edgecolor='#000000',
                                linewidth=line_width,                                
                                label='Age 35-45')
        age_group4_bar = plt.bar(second_bar_positions, age_group4, bar_width,
                                color='#FFFF00',
                                label='Age 45-55')
        age_group5_bar = plt.bar(second_bar_positions, age_group5, bar_width,
                                bottom=age_group4,
                                color='#FF7F00',
                                edgecolor='#000000',
                                ecolor='#FF7F00',
                                linewidth=line_width,
                                label='Age 55+')
        #create labels                        
        plt.xticks(second_bar_positions, responses)
        plt.ylabel('Frequency of Responses')
        plt.xlabel('Range of Experiences')
        plt.title('Experiences with Online Dating')
        plt.legend(loc='best')
        
        sns.despine() #plot bars
    
    plt.savefig('exp_graph.png')
    #plt.show()
    plt.clf()   
    
    
#########################Opinions of Online Dating##############################
    
def opin_dict(opinion_list, first_age, second_age):
    '''
     Parameters:
        opinion_list = a list of string values where item "0" is age, "1" and "2" are 
        Positive (responders had positive responses to online dating), and item 
        "3" and "4" are Negative (responders had negative responses to online
        dating)
        first_age = int, lower bound age
        second_age = int, upper bound age
    Returns:
        dictionary that maps age groups in bound to corresponding responsing
    '''
    map_value = {}
    for response in opinion_list:
        age = int(response[0])
        # responder is Positive
        positive_response = response[1] == '1' or response[2] == '1' 
        # responder is Negative
        negative_response = response[3] == '1' or response[4] == '1' 
        if age >= first_age and age <= second_age:
            if positive_response: 
                map_value["positive"] = map_value.get("positive", 0) + 1
            elif negative_response: 
                map_value["negative"] = map_value.get("negative", 0) + 1
    return map_value

def print_opinion(dating_opinion):
    '''
    Parameters:
        opin_dict = function which takes in list of values, and two ages then returns dictionary
    Returns:
        none
    Prints: 
        each age group, and the dictionary of opinions corresponding to each
    '''
    print "age group between 18 to 25:", opin_dict(dating_opinion.values(), 18, 25)
    print "age group between 26 to 35:", opin_dict(dating_opinion.values(), 26, 35)
    print "age group between 36 to 45:", opin_dict(dating_opinion.values(), 36, 45)
    print "age group between 46 to 55:", opin_dict(dating_opinion.values(), 46, 55)
    # 98 and 99 are not relevant
    print "age group 56 and over:", opin_dict(dating_opinion.values(), 56, 97) 

def age_list_opinion(dating_opinion):
    '''helper function used for plotting
    Parameters:
        dating_opinion: dictionary of opinions that takes in age groups and returns dictionary
    Returns:
        list of dictionaries corresponding to age groups and dating opinion   
    '''
    age_group1 = opin_dict(dating_opinion.values(), 18, 25).values()
    age_group2 = opin_dict(dating_opinion.values(), 26, 35).values()
    age_group3 = opin_dict(dating_opinion.values(), 36, 45).values()
    age_group4 = opin_dict(dating_opinion.values(), 46, 55).values()
    age_group5 = opin_dict(dating_opinion.values(), 56, 97).values()  
    
    return [age_group1, age_group2, age_group3, age_group4, age_group5]
    
################################################################################    
    
def plot_opin(opin_list):
    N = 5
    positive = (opin_list[0][0], opin_list[1][0], opin_list[2][0], opin_list[3][0], opin_list[4][0])
    negative = (opin_list[0][1], opin_list[1][1], opin_list[2][1], opin_list[3][1], opin_list[4][1])
    
    # the x locations for the groups
    ind = np.arange(N) 
    # the width of the bars: can also be len(x) sequence
    width = 0.35 
   
    p1 = plt.bar(ind, positive, width, color='b')
    p2 = plt.bar(ind, negative, width, color='r', 
        bottom=positive)
    plt.ylabel('Number of Responses')
    plt.xlabel('Age Groups')
    plt.title('Opinions on Online Dating')
    plt.xticks(ind + width/2., ('18-25yr', '25-35yr', '35-45yr', '45-55yr', '56+yr'))
    plt.legend((p1[0], p2[0]), ('Postive', 'Negative'))
    plt.savefig("opinion_dating.png")
    # plt.show()  
    plt.clf()  
    
#########################Popular Website Graph #################################    

def plot_website(website_data):  
    '''  
    Parameters:
        the website_data, which is actually equivalent to the website_lst sorted
        by values.
    Returns:
        Graphs the frequencies that responders use the popular dating websites.
        The function should return None. 
    ''' 
    WebsiteNames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    freqs = website_data
    LABELS = ["Adult Friend Finder", "Refused", "J Date", "Zoosk", "Christian Mingle", "Unknown", "Plenty of Fish", "Other", "OK Cupid", "eHarmony", "Match.com"]
    width = .5
    plt.figure(figsize=(20, 10))
    plt.title('Popular Dating Websites')
    plt.xlabel('Dating Websites')
    plt.ylabel('Frequency of Website Usage')
    plt.bar(WebsiteNames, freqs, width, align='center', color='m')
    plt.xticks(WebsiteNames, LABELS)
    plt.savefig("pop_website.png")
    # plt.show()   
    plt.clf()
    
###########################Popular Apps Graph #################################    

def plot_app(app_data):   
    '''  
    Parameters:
        the app_data, which is actually equivalent to the app_lst sorted by values.
    Returns:
        Graphs the frequencies that responders use the popular dating apps.
        The function should return None. 
    ''' 
    AppNames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    freqs = app_data
    LABELS = ["Tinder", "Not Valid", "J Date", "Refused", "Skout", "eHarmony", "Multiple Response", "Unknown", "Match.com", "Other", "Plenty of Fish", "OK Cupid"]
    width = .5
    plt.figure(figsize=(18, 8))
    plt.title('Popular Dating Apps')
    plt.xlabel('Dating Apps')
    plt.ylabel('Frequency of App Usage')
    plt.bar(AppNames, freqs, width, align='center', color='m')
    plt.xticks(AppNames, LABELS)
    plt.savefig("pop_app.png")
    # plt.show() 
    plt.clf()
 
####################################Main#######################################
def main():
    
# If this file, dating_data.py, is run as a Python script (such as by typing
# "python dating_data.py" at the command shell), then run the main() function.
    information = 'May_2013_Online_Dating_CSV.csv'
    open_file = open(information, 'rb') 
    csv_file = csv.DictReader(open_file, delimiter = ',', quotechar = '"') 

    # Creates empty dictionaries for the file's general demographics. 
    demographics_dict = {}         # fips, sex, age, income, hisp, and race 
    relationship_status_dict = {}  # relan status: committed, single, single + looking     
    text_breakup_dict = {}         # breaks up via text/email message
    dating_experience = {}         # describes responders' exiperences
    dating_opinion = {}            # describes responders' opinions
    lgbt_dict = {}                 # sexual orientation and dating website/app usage
    
    # Creates empty list for the file's popular websites and apps.
    website_lst = []               # do you use dating websites, which one?
    app_lst = []                   # do you use dating apps, which one?
    
    
    # Loops through the file and creates dictionaries for the specific column names
    # identified as strings.
    for line in csv_file:   
        demographics_dict[line['psraid']] = [line['sex'], line['age'], line['inc'], line['hisp'], line['race']]
        lgbt_dict[line['psraid']] =  [line['lgbt'], line['date1a'], line['date2a']]
        relationship_status_dict[line['psraid']] = [line['mar'], line['mar2'], line['mar4']] 
        text_breakup_dict[line['psraid']] = [line['breaka'], line['breakb']]
        dating_experience[line['psraid']] = [line['age'], line['date5a'], line['date5b'], line['date5c'], line['date5d']]
        dating_opinion[line['psraid']] = [line['age'], line['date9a'], line['date9b'], line['date9c'], line['date9d']]
        # Loops through the file line "date1bm1" and creates list of popular dating 
        # websites.
        website_lst.append(line['date1bm1'])
        # Loops through the file line "date2bm1" and creates a list of popular 
        # dating apps.
        app_lst.append(line['date2bm1'])
    
    open_file.close()  
     
    # checks that the text_break function is working
    assert(len(text_break(text_breakup_dict)) == 2)
    assert(text_break({}) == [0,0])
    # checks that the maximum value in the list is less than than the total values 
    # that could be in the list
    assert(max(text_break(text_breakup_dict)) < len(text_breakup_dict.values()))
    
    #checks that when pass in null values, returns an empty dictionary
    assert(opin_dict([],0,0) ==  {})
    assert(exp_dict([],0,0) ==  {})
    assert(opin_dict(dating_opinion.values(), 0, 17) == {})
    assert(exp_dict(dating_experience.values(), 0, 17) == {})
    
    #checks that when pass in null values, returns a list of empty dictionaries
    assert(len(age_list_opinion(dating_opinion)) == 5)
    assert(len(age_list_experience(dating_experience)) == 5)
    
    
    # demographics count
    print "Demographics of Survey Responders:"
    demographic_count(demographics_dict)
    print
    
    # demographics of relationship vs single
    print "Relationship Status of Survey Responders:"
    check_relationship(relationship_status_dict)
    print
    
    # sexual orientation of survey responders IF used online dating
    print "Sexuality of Survey Responders IF Used Online Dating:"
    lgtb_percent_dict(lgbt_dict)
    print

    # most popular dating websites and apps
    print "Website and App Dating Service Popularity:"
    print "Websites:", sorted(combine_dictionaries(popularity_dict(website_lst), website_ref), key = operator.itemgetter(1), reverse = True)
    print "Apps:", sorted(combine_dictionaries(popularity_dict(app_lst), app_ref), key = operator.itemgetter(1), reverse = True)
    print
    
    # survey responder dating opinion
    print "Responders' Online Dating Opinions:"
    print_opinion(dating_opinion)
    print
    
    # survey responder dating experience
    print "Responders' Online Dating Experiences:"
    print_experience(dating_experience)
    print
    
    # break up by text/email 
    print "Responder Breakup Via Text/Email" 
    print "Amount of people who have sent a break up text/email:", text_break(text_breakup_dict)[0]
    print "Amount of people who have received a break up text/email:", text_break(text_breakup_dict)[1]
    
    # Calls text_break function with breakup_dict as parameters.
    text_break_data = text_break(text_breakup_dict)
    plot_text_break(text_break_data)
    
    # Calls age_list_experience function with dating_experience as parameters.
    exp_data = age_list_experience(dating_experience)
    plot_exp(exp_data)
    
    # Calls age_list_experience function with dating_opinion as parameters.
    opin_list = age_list_opinion(dating_opinion)
    plot_opin(opin_list)
    
    # Calls popularity_dict function with website_lst values as parameters.
    website_data = sorted(popularity_dict(website_lst).values())
    plot_website(website_data)
    
    # Calls popularity_dict function with app_lst values as parameters.
    app_data = sorted(popularity_dict(app_lst).values())
    plot_app(app_data)  
    
    
if __name__ == "__main__":
    main()