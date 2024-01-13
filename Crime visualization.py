import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Crime.csv', sep=',')

#Getting array of offense type and quantities of maked offense
topics = ['Date of Offense', 'District', 'Type of Hate Bias', 'Top Offense Type'] #Topics to analyse

def repeatedValues(text):
    repeatedValues = []
    uniqueValues = []
    elements = df[text]
    for i in range(len(elements)):
        if(elements[i] in uniqueValues):
            repeatedValues.append(elements[i])
        elif(elements[i] not in uniqueValues):
            uniqueValues.append(elements[i])
    return repeatedValues

def uniqueValues(text, repeatedValues):
    elements = df[text]
    uniqueValues = []
    for i in range(len(elements)):
        if(elements[i] not in repeatedValues):
            repeatedValues.append(elements[i])
            uniqueValues.append(elements[i])
    return repeatedValues, uniqueValues

def calculatingEach(repeatedValues, uniqeValueArray):
    watchedValues = []
    value = []
    valueQuantity = []
    for i in range(len(repeatedValues)):
        quantity = 1
        element = repeatedValues[i]
        if(element in uniqeValueArray):
            value.append(repeatedValues[i])
            valueQuantity.append(quantity)
            continue
        if(repeatedValues[i] not in watchedValues):
            for j in range(len(repeatedValues)):
                nextElement = repeatedValues[j]
                if(element == nextElement):
                    quantity += 1
            value.append(repeatedValues[i])
            valueQuantity.append(quantity)
            watchedValues.append(repeatedValues[i])
        else:
            continue
    return value, valueQuantity

def OffenseQuantity():
    offenseArray = []
    quantityArray = []
    for i in range(len(topics)):
        OffenseType= repeatedValues(topics[i])
        OffenseType, uniqeValueArray = uniqueValues(topics[i], OffenseType)
        offense, elements = calculatingEach(OffenseType, uniqeValueArray)
        offenseArray.append(offense)
        quantityArray.append(elements)
    return offenseArray, quantityArray

offenseTypes, quantity = OffenseQuantity()

def GettingArrayOfOffensive(columnName, offenseTypesGroup): 
    finalArray = []
    for i in range(len(offenseTypesGroup)):
        searchedValues = offenseTypesGroup[i]
        array = []
        for j in range(len(columnName)):
            if (columnName[j] == searchedValues):
                array.append(columnName[j])
        finalArray.append(array)
    return finalArray

def SimplePLot(nameOfPlot, offenseType, quantity, reverseBool):
    if(reverseBool == True):
        quantity.sort()
        offenseType.reverse()
    plt.plot(offenseType, quantity, linewidth=2)
    plt.title(nameOfPlot, weight='bold', fontsize=10)
    for i in range(len(quantity)):
        plt.scatter(i, quantity[i], s=30, zorder=10, label=offenseType[i]) #Taskas
        plt.text(i, quantity[i]+(np.sum(quantity)/len(quantity)*0.1), f"{quantity[i]}", horizontalalignment='center') #Tekstas virs tasko
    if(reverseBool == True):
        plt.legend(loc='upper left',  ncol=2, fontsize=8)
    else:
        plt.legend(loc='upper right',  ncol=2, fontsize=8)
    plt.tick_params(bottom=None, labelbottom=None)
    plt.ylim(-1, max(quantity)+max(quantity)*0.2)
    plt.grid(True)

def myFunc(e): #Sorting array by lenght
  return len(e)

def Histogram(nameOfPlot, columnName, quantity, offenseTypes): 
    quantity.sort()
    allArrays = GettingArrayOfOffensive(columnName, offenseTypes)
    allArrays.sort(key=myFunc)
    array = []
    for i in range(len(allArrays)):
        colorOfBars = plt.cm.seismic(i/len(allArrays))
        plt.hist(allArrays[i], bins=len(quantity), edgecolor="white", width=0.75, alpha=0.8, color=colorOfBars, label=allArrays[i][0])
        if((len(allArrays) - i) <= 3):
            plt.text(i+(np.sum(len(quantity))/len(quantity)*0.1), quantity[i]+(np.sum(quantity)/len(quantity)*0.1), f"{quantity[i]}", weight='bold')
        else:    
            plt.text(i+(np.sum(len(quantity))/len(quantity)*0.1), quantity[i]+(np.sum(quantity)/len(quantity)*0.1), f"{quantity[i]}")
        array.append(allArrays[i][0])
    plt.legend(ncol=2)
    plt.xticks(np.arange(len(allArrays)) + 0.3, array)
    plt.tick_params(bottom=None, labelbottom=None)
    plt.ylim(-1,  max(quantity)+max(quantity)*0.2)
    plt.title("Offense "+nameOfPlot, weight='bold', fontsize=10)
    plt.grid(True)

def GroupingDates(dateArray): 
    quantityArray = []
    monthsChecked = []
    dates = dateArray
    month = 1
    for i in range(len(dates)):
        quantity = 0
        date = dates[i]
        dateMonth = (date.split('/'))[0]
        for j in range(len(dates)):
            findingDate = dates[j]
            findingDateMonth = (findingDate.split('/'))[0]
            if(dateMonth == findingDateMonth):
                quantity += 1
        if(dateMonth not in monthsChecked):
            quantityArray.append(quantity)
            month += 1
        monthsChecked.append(dateMonth)
    return quantityArray

def MonthsLabels():
    stringArray = []
    months = np.arange(1, 13, 1)
    for i in range (len(months)):
        stringArray.append(str(months[i]))
    return stringArray

def MonthsToSeasons(months):
    seasonValues = []
    sum = 0
    months = months[-1:] + months[:-1]
    for i in range(1, len(months)+1):
        sum += months[i-1]
        if i % 3 == 0:
            seasonValues.append(sum)
            sum = 0
    return seasonValues

def PieGraph(title, datesColumn, labelsArray, seasonPie):
    if seasonPie:
        seasons = ['winter', 'spring', 'summer', 'autumn']
        eachMonthOffense = GroupingDates(datesColumn)
        splittedToSeasons = MonthsToSeasons(eachMonthOffense)
        plt.pie(splittedToSeasons, labels=seasons, autopct='%1.2f%%', radius=1.1, colors=plt.cm.summer(np.linspace(0, 1, len(splittedToSeasons))))
        plt.title("Season offense", weight='bold', fontsize=10)
    else:
        eachMonthOffense = GroupingDates(datesColumn)
        plt.pie(eachMonthOffense, labels=labelsArray, autopct='%1.2f%%', radius=1.1, colors=plt.cm.viridis(np.linspace(0, 1, len(eachMonthOffense))))
        plt.title(title + "(months)", weight='bold', fontsize=10)

plt.figure(figsize=(14, 11))

plt.subplot2grid((4, 4), (0, 0), rowspan=2, colspan=2) #Printing simple plot
SimplePLot(topics[2], offenseTypes[2], quantity[2], False)

plt.subplot2grid((4, 4), (0, 2), rowspan=2, colspan=2) #Printing histogram
Histogram(topics[1], df['District'], quantity[1], offenseTypes[1])

plt.subplot2grid((4, 4), (2, 0), rowspan=2, colspan=2) #Printing another simple plot
SimplePLot(topics[3], offenseTypes[3], quantity[3], True) 

plt.subplot2grid((4, 4), (2, 2), rowspan=2, colspan=1) #Printing PieGraph by months
PieGraph(topics[0], df['Date of Offense'], MonthsLabels(), False)

plt.subplot2grid((4, 4), (2, 3), rowspan=2, colspan=1) #Printing PieGraph by year seasons
PieGraph(topics[0], df['Date of Offense'], MonthsLabels(), True)
plt.savefig("visualisation.png")

plt.show()