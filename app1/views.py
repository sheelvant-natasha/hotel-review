from django.shortcuts import render,redirect
from django.http import HttpResponse
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
import joblib
import re
from .models import Review
#from sklearn.externals import joblib


class reviews:
    def __init__(self ,uname , ureview , uop):
        self.uname=uname
        self.ureview=ureview
        self.uop=uop


# Create your views here.
name=""
review=""
op=-1




def home(req):
    
    AllOb = Review.objects.raw('select * from app1_review')
    PositiveOb =Review.objects.raw('select * from app1_review where sentiment = %s ' ,[True])
    NegativeOb =Review.objects.raw('select * from app1_review where sentiment = %s ' ,[False])
    if not AllOb:
        AllObFlag=0
    else:
        AllObFlag=1
    if not PositiveOb:
        PositiveObFlag=0
    else:
        PositiveObFlag=1
    if not NegativeOb:
        NegativeObFlag=0
    else:
        NegativeObFlag=1

   
    if req.method=="POST":
        print("POST")
        name = req.POST["name"]
        review = req.POST["review"]      
      
        op = predict_result(review)

        #save the review
        robj = Review()
        robj.name=name
        robj.text=review
        robj.sentiment=op
        robj.save()

        AllOb = Review.objects.raw('select * from app1_review')
        PositiveOb =Review.objects.raw('select * from app1_review where sentiment = %s ' ,[True])
        NegativeOb =Review.objects.raw('select * from app1_review where sentiment = %s ' ,[False])
        if not AllOb:
            AllObFlag=0
        else:
            AllObFlag=1
        if not PositiveOb:
            PositiveObFlag=0
        else:
            PositiveObFlag=1
        if not NegativeOb:
            NegativeObFlag=0
        else:
            NegativeObFlag=1
        return render(req ,'home.html',{'name':name ,'review':review ,'op':op ,'h':1 ,'AllOb':AllOb ,'PositiveOb':PositiveOb ,'NegativeOb':NegativeOb,'AllObFlag':AllObFlag ,'PositiveObFlag':PositiveObFlag ,'NegativeObFlag':NegativeObFlag})
    else:
        #return render(req,'home.html',{'h':h,'reviews':reviews ,'ops':ops ,'reviews':reviews} )
        
      
        return render(req,'home.html',{'h':0,'AllOb':AllOb ,'PositiveOb':PositiveOb ,'NegativeOb':NegativeOb,'AllObFlag':AllObFlag ,'PositiveObFlag':PositiveObFlag ,'NegativeObFlag':NegativeObFlag} )

#=============================================================================================================
def predict_result(text):
    
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stopwrds = stopwords.words('english')

    to_be_removed =['not' ,'no' ,'nor' ,"wasn't" ,"wouldn't","weren't","doesn't" ,"didn't" ,"haven't" ]
    for w in to_be_removed:
        stopwrds.remove(w)

    ps2 = PorterStemmer()
    new_review = re.sub('[^a-zA-Z]' ," " ,text)
    new_review = new_review.lower()
    new_review = new_review.split()
    new_review = [ps2.stem(x) for x in new_review if not x in set(stopwrds)]
    new_review = " ".join(new_review)
    #print(new_review)
    new_corpus =[new_review]


    cvmodel = joblib.load('app1/MyModel/cv_model')
    corpus2 =cvmodel.transform(new_corpus).toarray()
    svmModel = joblib.load('app1/MyModel/svm_model')

    if svmModel.predict(corpus2)==0:
        print('negtive')
        return 0

    else:
        print('positive')
        return 1
    

