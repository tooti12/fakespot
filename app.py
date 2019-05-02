from flask import Flask, redirect, url_for, render_template, request,jsonify
import os
import re
from datetime import datetime
from collections import defaultdict
import calendar
import numpy as np
import urllib
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import numpy as np
import pickle


app = Flask(__name__)


from sqlalchemy import create_engine
import pandas as pd
import cx_Oracle
oracle_connection_string = 'oracle+cx_oracle://system:umarjaved@localhost:1521/orcl'
engine = create_engine(oracle_connection_string)
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(a,b,c,d,e,pic,url,nor,f,g,h,i,j,k):

    sql = ('insert into FYP( PRODNAME,CATEGORY,DISCRIPTION,TRUTHFUL,DECEPTIVE,IMAGE,LINK,NOR,T1X,T1Y,T2X,T2Y,T3X,T3Y ) values (:namep,:cat,:discp,:tp,:dp,:img,:url,:nr,:x1,:y1,:x2,:y2,:x3,:y3 )')
    empPicture = convertToBinaryData(pic)

    result  = engine.execute(sql,  {'namep': a, 'cat': b, 'discp': c, 'tp': d, 'dp': e,'img':empPicture,'url':url,'nr':nor,'x1':f,'y1':g,'x2':h,'y2':i,'x3':j,'y3':k})

    print ("Image and file inserted successfully as a BLOB into python_employee table", result)

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def readBLOB(url,picture):

        sql=('select PRODNAME,T3Y,DISCRIPTION,TRUTHFUL,DECEPTIVE,IMAGE,LINK,NOR,T1X,T1Y,T2X,T2Y,T3X,CATEGORY from FYP where LINK=:am')
        record=engine.execute(sql,{'am':url})
        #print(record)
        for row in record:
            print("prodname = ", row[0], )
            print("category = ", row[13])
            print("discp = ", row[2],)
            print("truthfu = ", row[3])
            print("decptive = ", row[4],)
            image =  row[5]
            print("Storing employee image and bio-data on disk \n")
            print(row[6])
            print(row[8])
            print(row[9])
            print(row[10])
            print(row[11])
            print(row[12])
            print(row[1])
            print("---------------------------------------------------------")
            write_file(image, picture)
            return record

@app.route('/')
def index2():
    return render_template('index.html')


@app.route('/response', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        url2 = request.form['num']

        # -----------------------------------
        #images = "static/hello1.jpg"
        imagess="static/22.JPG"
        c1x = [1, 2, 3, 4]
        c1y = [5, 2, 8, 3]
        c2x = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        c2y = [10,43,2,14,23]
        c3x = [1, 2, 3, 4]
        c3y = [5, 2, 8, 3]

        answer = readBLOB(url2, imagess)
        print(answer)
        link=None
        print("-----------pppp")
        if(answer!=None):
            for row in answer:
                print("abcd")
                n = row[0]
                print(row[0])
                c = row[13]
                dis = row[2]
                tf = row[3]
                dp = row[4]
                image = row[5]
                link = row[6]
                print(link)
                print(row[6])
                nr = row[7]
                cx1=row[8]
                cy1=row[9]
                cx2=row[10]
                cy2=row[11]
                cx3=row[12]
                cy3=row[1]
                print("------"+cy3)
                print(n)
                list1 = cx1.split(",")
                print(list1)
                li1 = []
                for i in list1:
                    li1.append(float(i))
                print(li1)
                list2 = cy1.split(",")
                print(list2)
                li2 = []
                for i in list2:
                    li2.append(int(i))
                print(li2)
                list3 = cx2.split(",")
                print(list3)
                li3 = []
                for i in list3:
                    li3.append(str(i))
                print(li3)
                list4 = cy2.split(",")
                print(list4)
                li4 = []
                for i in list4:
                    li4.append(str(i))
                print(li4)
                list5 = cx3.split(",")
                print(list5)
                li5 = []
                for i in list5:
                    li5.append(str(i))
                print(li5)
                list6 = cy3.split(",")
                print(list6)
                li6 = []
                for i in list6:
                    li6.append(int(i))
                print(li6)
                # print("Storing employee image and bio-data on disk \n")
                write_file(image, imagess)
                i11 = "How are reviewers describing this item? (Good, Must Try)"
                i21 = "Our engine has profiled the reviewer patterns and has determined that there is " + str(
                    dp) + "% deception involved."
                i31 = "Our engine has discovered that over " + str(tf) + "% high quality reviews are present."
                i41 = "This product had a total of " + nr + " as of our last analysis date on April 1st 2019."
        print(url2)
        print("a")
        print(link)

        if (url2 == link):
            print("---------------------")
            # results=sample(range(1,10),5)
            # return jsonify({'results': sample(range(1, 10), 5)})
            # return render_template('response.html', image=images, pname=n, pdiscp=dis, nor=10, dp=dp,tp=tf, pcat=c,res=results)
            return render_template('response.html', image=imagess, pname=n, pdiscp=dis, nor=nr, dp=dp,
                                   tp=tf, pcat=c,
                                   a=li1, b=li2, c=li3, d=li4, e=li5, f=li6, info1=i11, info2=i21, info3=i31, info4=i41)
        else:

            hotel_name='marriot'
            hotel_reviews='75'
            decep_percent=70
            truth_percent=30
            start = 0
            num_pages = 5
            end = 20 * num_pages
            hotel_name = ""
            hotel_rating = ""
            hotel_reviews = ""
            reviews = []
            reviewer_name = []
            reviewer_rating = []
            review_date = []
            reviewer_city = []
            iterator=0
            while (start < end):
                url = url2 + '?start=' + str(start)
                start += 20
                print(url)
                page = urlopen(url)
                soup = BeautifulSoup(page)
                if (start <= 20):
                    name = soup.findAll('h1', {"class": "biz-page-title embossed-text-white"})
                    #print ("name",name)
                    name2= soup.findAll('h1', {"class": "biz-page-title embossed-text-white shortenough"})
                   # print("name", name)
                    total_reviews = soup.find("span", {"class": "review-count rating-qualifier"}).contents[ 0]  # number of reviews
                    rating = soup.find("img", {"class": "offscreen"})  # collects tag for rating
                    price = soup.find("span", {"class": "business-attribute price-range"}).contents[
                        0]  # price of restaurant
                    city = soup.find("div", {"class": "map-box-address"})  # City of restaurant
                    imgs = soup.findAll("div", {"class":"showcase-photo-box"})
                    for img in imgs:
                        temp=img.find('img',src=True)
                        #print (temp.get('src'))
                        print(temp['src'])
                        os.chdir(r"C:\Users\Umar Javed\PycharmProjects\untitled3\static")
                       # print (type(img))
                       # break
                        imgUrl =temp['src']
                        #imgUrl+=temp['href']
                        urllib.request.urlretrieve(imgUrl, os.path.basename('hello1.jpg'))
                        break

                    for temp in name:
                            hotel_name += (temp.text)
                            #print (temp.text)
                    for temp in name2:
                        hotel_name += (temp.text)

                    hotel_reviews = total_reviews.strip()
                    hotel_rating = rating.get('alt')
                    # print (name)
                    city = city.find('address')
                    hotel_location = city.text.strip()

                for reviewBody in soup.findAll('div', {"class": "review-content"}):
                    reviews.append(reviewBody.find('p').text)
                    # print(i)
                    # i=i+1
                for i, j in zip(soup.findAll('li', {"class": "user-name"}), soup.findAll('li', {"class": "user-location"})):
                    reviewer_name.append(i.text)
                    reviewer_city.append(j.text)
                rating = soup.findAll('div', {"class": "biz-rating biz-rating-large clearfix"})
                count = 0
                for i in (rating):
                    if (count < len(rating) - 1):
                        # print (i.find('span').text)\
                        try:
                            review_date.append(i.find('span').text)
                            # print (i.div.div.get('title'))
                            reviewer_rating.append(i.div.div.get('title'))
                        except:
                            reviewer_rating.append(reviewer_rating[iterator-1])
                    #  print('done')
                    count += 1
                iterator+=1;

            indices=[]
            for i , elem in enumerate(review_date):
                if 'Previous' in elem:
                    indices.append(i)
            for i in indices:
                del review_date[i];
                del reviewer_rating[i];
            os.chdir(r"C:\Users\Umar Javed\PycharmProjects\untitled3")
            loaded_model = pickle.load(open("PU_model_trip.sav", 'rb'))
            vec_model = pickle.load(open("vec_model_trip.sav", 'rb'))

            m = vec_model.transform(reviews)
            pred=loaded_model.predict(m)


            c, f = np.unique(pred, return_counts=True)
            decep_percent = round((f[0] / float(sum(f))) * 100)
            truth_percent = round((f[1] / float(sum(f))) * 100)

            print(np.unique(pred, return_counts=True))
            print(truth_percent)
            print(decep_percent)
            # nor = count
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

            # YAI GRAPHS KAI CODE HAIN
            truthful_reviews = []
            name = []
            rating = []
            date = []
            city = []

            for i in range(len(pred)):
                if pred[i] == 'truthful':
                    truthful_reviews.append(reviews[i])
                    rating.append(float(reviewer_rating[i].split()[0]))
                    date.append(review_date[i].split()[0])
                    city.append(reviewer_city[i].split(',')[1].split()[0])
                    name.append(reviewer_name[0].split()[0])

            np.unique(pred, return_counts=True)
            data = pd.DataFrame(
                {'review': truthful_reviews, 'reviewer_name': name, 'rating': rating, 'date': date, 'reviewer_state': city})

            #### 1st Graph: Rating vs review count (bar chart)
            rv_ct = np.array(data.groupby('rating').count()['review'])
            rt = np.unique(data["rating"])
            print(rt)  # x-axis data
            print(type(rt[0]))

            # c1x=[int(rt[0]),int(rt[1]),int(rt[2]),int(rt[3]),int(rt[4])]
            # rt=[1,2,3,4,5]
            print(hotel_rating)
            print(rv_ct)  # y-axis data
            print(type(rv_ct[0]))
            # rv_ct=[5,10,11,3,2]
            ##### 2nd Graph State Vs review Count
            state_ct = np.array(data.groupby('reviewer_state').count()['review'])
            state = np.unique(data["reviewer_state"])
            print(state)  # x-axis data
            print(type(state[0]))
            print(state_ct)  # y-axis data
            print(type(state_ct[0]))
            print(hotel_reviews)
            print(type(hotel_reviews))
            i1 = "How are reviewers describing this item? (Good, Must Try)"
            i2 = "Our engine has profiled the reviewer patterns and has determined that there is "+str(decep_percent)+"% deception involved."
            i3 = "Our engine has discovered that over "+str(truth_percent)+"% high quality reviews are present."
            i4 = "This product had a total of "+hotel_reviews+" as of our last analysis date on April 1st 2019."
            # insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # n=0
            # while (n<len(state)):
            #     if(len(state[n]>2)):
            #       name=
            q=rt.tolist()
            w=rv_ct.tolist()
            r=state.tolist()
            s=state_ct.tolist()
            print(s)
            x1 = ""
            for row in rt:
                if ((q.index(row)) < (len(q) - 1)):
                    x1 += str(row) + ','
                else:
                    x1 += str(row)
            print(x1)
            x2 = ""
            for row in rv_ct:
                if ((w.index(row)) < (len(w) - 1)):
                    x2 += str(row) + ','
                else:
                    x2 += str(row)
            print(x2)
            x3="Mon,Tue,Wed,Thu,Fri"
            x4="10,12,24,34,6"
            x5 = ""
            for row in state:
                if ((r.index(row)) < (len(r) - 1)):
                    x5 += str(row) + ','
                else:
                    x5 += str(row)
            print(x5)
            x6 = ""
            for row in s:
                if ((s.index(row)) < (len(s) - 1)):
                    x6 += str(row) + ','
                else:
                    x6 += str(row)
            print(x6)
            x6=x6[:-1]
            print(x6)
            images = "static/hello1.jpg"
            insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews,x1,x2,x3,x4,x5,x6)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            insertBLOB(hotel_name, 'Hotel', 'A 5 star hotel', truth_percent, decep_percent, images, url2, hotel_reviews,
                       x1, x2, x3, x4, x5, x6)



            # truthful_reviews=[]
            # name=[]
            # rating=[]
            # date=[]
            # city=[]
            #
            # for i in range(len(pred)):
            #     if pred[i]=='truthful':
            #         truthful_reviews.append(reviews[i])
            #         rating.append(float(reviewer_rating[i].split()[0]))
            #         date.append(review_date[i].split()[0])
            #         city.append(reviewer_city[i].split(',')[1].split()[0])
            #         name.append(reviewer_name[0].split()[0])
            #
            # np.unique(pred,return_counts=True)
            # # date=[ i.split('/')[1:] for i in date]
            # date1=[]
            # for i in date:
            #     i=i.split('/')
            #     temp=int(i[0])#+'-'+i[2][2:]
            #     date1.append(temp)
            #
            # data=pd.DataFrame({'review':truthful_reviews, 'reviewer_name':name, 'rating':rating, 'date':date1, 'reviewer_state':city})
            #
            # #### 1st Graph: Rating vs review count (bar chart)
            # rv_ct = np.array(data.groupby('rating').count()['review'])
            # rt = np.unique(data["rating"])
            # print(rt)  # x-axis data
            # print(type(rt[0]))
            #
            # # c1x=[int(rt[0]),int(rt[1]),int(rt[2]),int(rt[3]),int(rt[4])]
            # # rt=[1,2,3,4,5]
            # print(hotel_rating)
            # print(rv_ct)  # y-axis data
            # print(type(rv_ct[0]))
            # # rv_ct=[5,10,11,3,2]
            # ##### 2nd Graph State Vs review Count
            # state_ct=np.array(data.groupby('reviewer_state').count()['review'])
            # state= np.unique(data["reviewer_state"])
            # dic=defaultdict(lambda: 0)
            # for i in range(len(state_ct)):
            #     if state_ct[i]==1:
            #         dic['others']+=1
            #     else:
            #         dic[state[i]]=state_ct[i]
            # # print (dic.keys())   #x-axis data
            # # print (dic.values()) #y-axis data
            # state=list(dic.keys())
            # state_ct=list(dic.values())
            # print(state)  # x-axis data
            # print(type(state[0]))
            # print(state_ct)  # y-axis data
            # print(type(state_ct[0]))
            # print(hotel_reviews)
            # print(type(hotel_reviews))
            # i1 = "How are reviewers describing this item? (Good, Must Try)"
            # i2 = "Our engine has profiled the reviewer patterns and has determined that there is "+str(decep_percent)+"% deception involved."
            # i3 = "Our engine has discovered that over "+str(truth_percent)+"% high quality reviews are present."
            # i4 = "This product had a total of "+hotel_reviews+" as of our last analysis date on April 1st 2019."
            # # insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews)
            # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # q=rt.tolist()
            # w=rv_ct.tolist()
            # #r=state.tolist()
            # #s=state_ct.tolist()
            # r=state
            # s=state_ct
            # print(s)
            # x1 = ""
            # for row in rt:
            #     if ((q.index(row)) < (len(q) - 1)):
            #         x1 += str(row) + ','
            #     else:
            #         x1 += str(row)
            # print(x1)
            # x2 = ""
            # for row in rv_ct:
            #     if ((w.index(row)) < (len(w) - 1)):
            #         x2 += str(row) + ','
            #     else:
            #         x2 += str(row)
            # print(x2)
            #
            # x3="Mon,Tue,Wed,Thu,Fri"
            # x4="10,12,12,3,4"
            # x5 = ""
            # for row in state:
            #     if ((r.index(row)) < (len(r) - 1)):
            #         x5 += str(row) + ','
            #     else:
            #         x5 += str(row)
            # print(x5)
            # x6 = ""
            # for row in s:
            #     if ((s.index(row)) < (len(s) - 1)):
            #         x6 += str(row) + ','
            #     else:
            #         x6 += str(row)
            # print(x6)
            # x6=x6[:-1]
            # print(x6)
            # images = "static/hello1.jpg"
            # insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews,x1,x2,x3,x4,x5,x6)
            # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # insertBLOB(hotel_name, 'Hotel', 'A 5 star hotel', truth_percent, decep_percent, images, url2, hotel_reviews,
            #            x1, x2, x3, x4, x5, x6)
            # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

            return render_template('response.html', image=images, pname=hotel_name, pdiscp="A 5 star hotel", nor=hotel_reviews, dp=decep_percent,
                                   tp=truth_percent, pcat="Hotels",
                                   a=q, b=w, c=c2x, d=c2y, e=r, f=s, info1=i1, info2=i2, info3=i3, info4=i4)

    else:
        return render_template('index.html')

@app.route('/reanalyze')
def contact1():
    return render_template('reanalyze.html')
@app.route('/response2', methods=['GET', 'POST'])
def check1():
    if request.method == 'POST':
        url2 = request.form['num']

        # -----------------------------------
        #images = "static/hello1.jpg"
        imagess="static/22.JPG"
        c1x = [1, 2, 3, 4]
        c1y = [5, 2, 8, 3]
        c2x = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        c2y = [10,43,2,14,23]
        c3x = [1, 2, 3, 4]
        c3y = [5, 2, 8, 3]


        hotel_name='marriot'
        hotel_reviews='75'
        decep_percent=70
        truth_percent=30
        start = 0
        num_pages = 5
        end = 20 * num_pages
        hotel_name = ""
        hotel_rating = ""
        hotel_reviews = ""
        reviews = []
        reviewer_name = []
        reviewer_rating = []
        review_date = []
        reviewer_city = []
        iterator=0
        while (start < end):
            url = url2 + '?start=' + str(start)
            start += 20
            print(url)
            page = urlopen(url)
            soup = BeautifulSoup(page)
            if (start <= 20):
                name = soup.findAll('h1', {"class": "biz-page-title embossed-text-white"})
                #print ("name",name)
                name2= soup.findAll('h1', {"class": "biz-page-title embossed-text-white shortenough"})
               # print("name", name)
                total_reviews = soup.find("span", {"class": "review-count rating-qualifier"}).contents[ 0]  # number of reviews
                rating = soup.find("img", {"class": "offscreen"})  # collects tag for rating
                price = soup.find("span", {"class": "business-attribute price-range"}).contents[
                    0]  # price of restaurant
                city = soup.find("div", {"class": "map-box-address"})  # City of restaurant
                imgs = soup.findAll("div", {"class":"showcase-photo-box"})
                for img in imgs:
                    temp=img.find('img',src=True)
                    #print (temp.get('src'))
                    print(temp['src'])
                    os.chdir(r"C:\Users\Umar Javed\PycharmProjects\untitled3\static")
                   # print (type(img))
                   # break
                    imgUrl =temp['src']
                    #imgUrl+=temp['href']
                    urllib.request.urlretrieve(imgUrl, os.path.basename('hello1.jpg'))
                    break

                for temp in name:
                        hotel_name += (temp.text)
                        #print (temp.text)
                for temp in name2:
                    hotel_name += (temp.text)

                hotel_reviews = total_reviews.strip()
                hotel_rating = rating.get('alt')
                # print (name)
                city = city.find('address')
                hotel_location = city.text.strip()

            for reviewBody in soup.findAll('div', {"class": "review-content"}):
                reviews.append(reviewBody.find('p').text)
                # print(i)
                # i=i+1
            for i, j in zip(soup.findAll('li', {"class": "user-name"}), soup.findAll('li', {"class": "user-location"})):
                reviewer_name.append(i.text)
                reviewer_city.append(j.text)
            rating = soup.findAll('div', {"class": "biz-rating biz-rating-large clearfix"})
            count = 0
            for i in (rating):
                if (count < len(rating) - 1):
                    # print (i.find('span').text)\
                    try:
                        review_date.append(i.find('span').text)
                        # print (i.div.div.get('title'))
                        reviewer_rating.append(i.div.div.get('title'))
                    except:
                        reviewer_rating.append(reviewer_rating[iterator-1])
                #  print('done')
                count += 1
            iterator+=1;

        indices=[]
        for i , elem in enumerate(review_date):
            if 'Previous' in elem:
                indices.append(i)
        for i in indices:
            del review_date[i];
            del reviewer_rating[i];
        os.chdir(r"C:\Users\Umar Javed\PycharmProjects\untitled3")
        loaded_model = pickle.load(open("PU_model_trip.sav", 'rb'))
        vec_model = pickle.load(open("vec_model_trip.sav", 'rb'))

        m = vec_model.transform(reviews)
        pred=loaded_model.predict(m)


        c, f = np.unique(pred, return_counts=True)
        decep_percent = round((f[0] / float(sum(f))) * 100)
        truth_percent = round((f[1] / float(sum(f))) * 100)

        print(np.unique(pred, return_counts=True))
        print(truth_percent)
        print(decep_percent)
        # nor = count
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        # YAI GRAPHS KAI CODE HAIN
        truthful_reviews = []
        name = []
        rating = []
        date = []
        city = []

        for i in range(len(pred)):
            if pred[i] == 'truthful':
                truthful_reviews.append(reviews[i])
                rating.append(float(reviewer_rating[i].split()[0]))
                date.append(review_date[i].split()[0])
                city.append(reviewer_city[i].split(',')[1].split()[0])
                name.append(reviewer_name[0].split()[0])

        np.unique(pred, return_counts=True)
        data = pd.DataFrame(
            {'review': truthful_reviews, 'reviewer_name': name, 'rating': rating, 'date': date, 'reviewer_state': city})

        #### 1st Graph: Rating vs review count (bar chart)
        rv_ct = np.array(data.groupby('rating').count()['review'])
        rt = np.unique(data["rating"])
        print(rt)  # x-axis data
        print(type(rt[0]))

        # c1x=[int(rt[0]),int(rt[1]),int(rt[2]),int(rt[3]),int(rt[4])]
        # rt=[1,2,3,4,5]
        print(hotel_rating)
        print(rv_ct)  # y-axis data
        print(type(rv_ct[0]))
        # rv_ct=[5,10,11,3,2]
        ##### 2nd Graph State Vs review Count
        state_ct = np.array(data.groupby('reviewer_state').count()['review'])
        state = np.unique(data["reviewer_state"])
        print(state)  # x-axis data
        print(type(state[0]))
        print(state_ct)  # y-axis data
        print(type(state_ct[0]))
        print(hotel_reviews)
        print(type(hotel_reviews))
        i1 = "How are reviewers describing this item? (Good, Must Try)"
        i2 = "Our engine has profiled the reviewer patterns and has determined that there is "+str(decep_percent)+"% deception involved."
        i3 = "Our engine has discovered that over "+str(truth_percent)+"% high quality reviews are present."
        i4 = "This product had a total of "+hotel_reviews+" as of our last analysis date on April 1st 2019."
        # insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        q=rt.tolist()
        w=rv_ct.tolist()
        r=state.tolist()
        s=state_ct.tolist()
        print(s)
        x1 = ""
        for row in rt:
            if ((q.index(row)) < (len(q) - 1)):
                x1 += str(row) + ','
            else:
                x1 += str(row)
        print(x1)
        x2 = ""
        for row in rv_ct:
            if ((w.index(row)) < (len(w) - 1)):
                x2 += str(row) + ','
            else:
                x2 += str(row)
        print(x2)
        x3="Mon,Tue,Wed,Thu,Fri"
        x4="10,12,24,34,6"
        x5 = ""
        for row in state:
            if ((r.index(row)) < (len(r) - 1)):
                x5 += str(row) + ','
            else:
                x5 += str(row)
        print(x5)
        x6 = ""
        for row in s:
            if ((s.index(row)) < (len(s) - 1)):
                x6 += str(row) + ','
            else:
                x6 += str(row)
        print(x6)
        x6=x6[:-1]
        print(x6)
        images = "static/hello1.jpg"
        insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews,x1,x2,x3,x4,x5,x6)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        insertBLOB(hotel_name, 'Hotel', 'A 5 star hotel', truth_percent, decep_percent, images, url2, hotel_reviews,
                   x1, x2, x3, x4, x5, x6)



        # truthful_reviews=[]
        # name=[]
        # rating=[]
        # date=[]
        # city=[]
        #
        # for i in range(len(pred)):
        #     if pred[i]=='truthful':
        #         truthful_reviews.append(reviews[i])
        #         rating.append(float(reviewer_rating[i].split()[0]))
        #         date.append(review_date[i].split()[0])
        #         city.append(reviewer_city[i].split(',')[1].split()[0])
        #         name.append(reviewer_name[0].split()[0])
        #
        # np.unique(pred,return_counts=True)
        # # date=[ i.split('/')[1:] for i in date]
        # date1=[]
        # for i in date:
        #     i=i.split('/')
        #     temp=int(i[0])#+'-'+i[2][2:]
        #     date1.append(temp)
        #
        # data=pd.DataFrame({'review':truthful_reviews, 'reviewer_name':name, 'rating':rating, 'date':date1, 'reviewer_state':city})
        #
        # #### 1st Graph: Rating vs review count (bar chart)
        # rv_ct = np.array(data.groupby('rating').count()['review'])
        # rt = np.unique(data["rating"])
        # print(rt)  # x-axis data
        # print(type(rt[0]))
        #
        # # c1x=[int(rt[0]),int(rt[1]),int(rt[2]),int(rt[3]),int(rt[4])]
        # # rt=[1,2,3,4,5]
        # print(hotel_rating)
        # print(rv_ct)  # y-axis data
        # print(type(rv_ct[0]))
        # # rv_ct=[5,10,11,3,2]
        # ##### 2nd Graph State Vs review Count
        # state_ct=np.array(data.groupby('reviewer_state').count()['review'])
        # state= np.unique(data["reviewer_state"])
        # dic=defaultdict(lambda: 0)
        # for i in range(len(state_ct)):
        #     if state_ct[i]==1:
        #         dic['others']+=1
        #     else:
        #         dic[state[i]]=state_ct[i]
        # # print (dic.keys())   #x-axis data
        # # print (dic.values()) #y-axis data
        # state=list(dic.keys())
        # state_ct=list(dic.values())
        # print(state)  # x-axis data
        # print(type(state[0]))
        # print(state_ct)  # y-axis data
        # print(type(state_ct[0]))
        # print(hotel_reviews)
        # print(type(hotel_reviews))
        # i1 = "How are reviewers describing this item? (Good, Must Try)"
        # i2 = "Our engine has profiled the reviewer patterns and has determined that there is "+str(decep_percent)+"% deception involved."
        # i3 = "Our engine has discovered that over "+str(truth_percent)+"% high quality reviews are present."
        # i4 = "This product had a total of "+hotel_reviews+" as of our last analysis date on April 1st 2019."
        # # insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews)
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # q=rt.tolist()
        # w=rv_ct.tolist()
        # #r=state.tolist()
        # #s=state_ct.tolist()
        # r=state
        # s=state_ct
        # print(s)
        # x1 = ""
        # for row in rt:
        #     if ((q.index(row)) < (len(q) - 1)):
        #         x1 += str(row) + ','
        #     else:
        #         x1 += str(row)
        # print(x1)
        # x2 = ""
        # for row in rv_ct:
        #     if ((w.index(row)) < (len(w) - 1)):
        #         x2 += str(row) + ','
        #     else:
        #         x2 += str(row)
        # print(x2)
        #
        # x3="Mon,Tue,Wed,Thu,Fri"
        # x4="10,12,12,3,4"
        # x5 = ""
        # for row in state:
        #     if ((r.index(row)) < (len(r) - 1)):
        #         x5 += str(row) + ','
        #     else:
        #         x5 += str(row)
        # print(x5)
        # x6 = ""
        # for row in s:
        #     if ((s.index(row)) < (len(s) - 1)):
        #         x6 += str(row) + ','
        #     else:
        #         x6 += str(row)
        # print(x6)
        # x6=x6[:-1]
        # print(x6)
        # images = "static/hello1.jpg"
        # insertBLOB(hotel_name,'Hotel','A 5 star hotel',truth_percent,decep_percent,images,url2,hotel_reviews,x1,x2,x3,x4,x5,x6)
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # insertBLOB(hotel_name, 'Hotel', 'A 5 star hotel', truth_percent, decep_percent, images, url2, hotel_reviews,
        #            x1, x2, x3, x4, x5, x6)
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        return render_template('response2.html', image=images, pname=hotel_name, pdiscp="A 5 star hotel", nor=hotel_reviews, dp=decep_percent,
                               tp=truth_percent, pcat="Hotels",
                               a=q, b=w, c=c2x, d=c2y, e=r, f=s, info1=i1, info2=i2, info3=i3, info4=i4)

    else:
        return render_template('index.html')


@app.route('/product')
def data():
    print('heh')

    return render_template('product.html')
    #return jsonify({'results': sample(range(1,10),5)})

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


if __name__ == '__main__':
    app.run()
