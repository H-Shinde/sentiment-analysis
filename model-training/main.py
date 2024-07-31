import spacy
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
# Reads file into a pandas DataFrame
df = pd.read_csv("Data\test.csv")

v = TfidfVectorizer()
nlp = spacy.load('en_core_web_sm')


# Data Preprocessing Function
def preprocessing(df, column_name):
    # Remove special characters
    sp_ch_pat = '[^a-zA-Z\s0-9]'
    #Remove Html tags
    pat = '<.*?>'
    df[column_name] = df[column_name].str.replace(pat,'',regex=True)
    df[column_name] = df[column_name].str.replace(sp_ch_pat, '', regex=True)
    df[column_name] = df[column_name].str.lower()
    
    # Tokenization
    tok = [nlp(text) for text in df[column_name]]
    
    # Lemmatization and Stop Words Removal
    processed_docs = [[token.lemma_ for token in doc if not token.is_stop]for doc in tok]
    
    
    return processed_docs

def target_data_toNum(df,column_name):
  df[column_name] =   df[column_name].map({
        'neg':0,
        'pos':1
    })



processed_reviews = preprocessing(df, 'text')
target_data_toNum(df,'sentiment')
#Get new sentiment column
y_data = df['sentiment']


# Save new text into binary file
with open('process_reviews','wb')as f:
    pickle.dump(processed_reviews,f)

with open('new-y_data','wb')as f:
   pickle.dump(y_data,f)



#load Data
with open('Data\mainX','rb') as f:
   mainX = pickle.load(f)
with open('Data\mainY','rb') as f:
   mainY = pickle.load(f)



main_df = pd.DataFrame({
    'review': mainX,
    'sentiment': mainY
})


#split data into training | testing
X_train,X_test,y_train,y_test = train_test_split(main_df.review,main_df.sentiment,test_size=.2,random_state=2022,stratify=main_df.sentiment)

X_train = [' '.join(review) for review in X_train]
X_test = [' '.join(review) for review in X_test]



v.fit(X_train)

#KNN Classifier training
clfK = Pipeline([('vectorizer_tfidf',v),
    ('KNN',KNeighborsClassifier())]
   
)
clfK.fit(X_train,y_train)

#Linear Regression Classifier
clfL = Pipeline([('vectorizer_tfidf',v),
    ('logreg',LogisticRegression())]
   
)
clfL.fit(X_train,y_train)

#save models to binary file
with open('KNN-Model','wb') as f:
   pickle.dump(clfK,f)
with open('LinReg-Model','wb') as f:
   pickle.dump(clfL,f)




#load models
with open('KNN-Model','rb')as f:
   KNN = pickle.load(f)

with open('LinReg-Model','rb')as f:
   LR = pickle.load(f)

y_pred_KNN = KNN.predict(X_test)
y_pred_LR = LR.predict(X_test)


#Check Accuracy
print(f"Accuracy: {accuracy_score(y_test, y_pred_LR)}")
print(classification_report(y_test, y_pred_LR))



print(f"Accuracy: {accuracy_score(y_test, y_pred_LR)}")
print(classification_report(y_test, y_pred_LR))
