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
# df = pd.read_csv("test.csv")

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



# processed_reviews = preprocessing(df, 'text')




# with open('process_reviews','wb')as f:
#     pickle.dump(processed_reviews,f)




# target_data_toNum(df,'sentiment')


# y_data = df['sentiment']


# with open('new-y_data','wb')as f:
#    pickle.dump(y_data,f)





# Model Training/Feature Extraction


with open('mainX','rb') as f:
   mainX = pickle.load(f)

with open('mainY','rb') as f:
   mainY = pickle.load(f)
main_df = pd.DataFrame({
    'review': mainX,
    'sentiment': mainY
})

X_train,X_test,y_train,y_test = train_test_split(main_df.review,main_df.sentiment,test_size=.2,random_state=2022,stratify=main_df.sentiment)

X_train = [' '.join(review) for review in X_train]
X_test = [' '.join(review) for review in X_test]



# #KNN Classifier
# v.fit(X_train)
# clf = Pipeline([('vectorizer_tfidf',v),
#     ('KNN',KNeighborsClassifier())]
   
# )
# clf.fit(X_train,y_train)
# with open('KNN-Model','wb') as f:
#    pickle.dump(clf,f)


# #Linear Regression Classifier
# v.fit(X_train)
# clf = Pipeline([('vectorizer_tfidf',v),
#     ('logreg',LogisticRegression())]
   
# )
# clf.fit(X_train,y_train)

# with open('LinReg-Model','wb') as f:
#    pickle.dump(clf,f)

with open('KNN-Model','rb')as f:
   KNN = pickle.load(f)

with open('LinReg-Model','rb')as f:
   LR = pickle.load(f)

# y_pred_KNN = KNN.predict(X_test)
y_pred_LR = LR.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred_LR)}")
print(classification_report(y_test, y_pred_LR))
