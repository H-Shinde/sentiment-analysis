import pickle
from sklearn.metrics import accuracy_score, classification_report


X_test = ['The best spicy chicken crisp I had at any McDonalds. Other McDonalds there soft, this place was crispy as advertised. The service was fast and super friendly. There was even 2 cookies in the bag from the GM.No complaints at all, great job!']

#.88 Accuracy
with open('Models\LinReg-Model','rb')as f:
   logReg = pickle.load(f)


y_pred_logReg = logReg.predict(X_test)



print('negative' if y_pred_logReg==0 else 'positive')


# print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
# print(classification_report(y_test, y_pred))