from flask import Flask,render_template,url_for,request,session,redirect
from main import getEmotions,getDescription,getStrPlatforms
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def index():
        
        if request.method=='POST':
               
               word = request.form.get('word')
               print(f"The word is {word}")
               emotions = getEmotions(word)
               description = getDescription(word)
               platforms =  getStrPlatforms(word)
               return render_template('result.html',data1 = emotions, data2=description,data3=platforms)

        return render_template('index.html')

@app.route("/about")
def about():
      return render_template('about.html')

   
@app.route("/how")
def how():
      return render_template('how.html')


if __name__ == '__main__':
    app.run(debug=True)