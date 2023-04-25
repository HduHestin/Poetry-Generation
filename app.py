from flask import Flask, render_template, request, flash, redirect
import Generate_poetry as gp

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # 获取表单数据
        results = request.form
        words = results.get('word')
        if words == 'random':
            words_poem = gp.random_poetry()
        else:
            words_poem = gp.random_hide_poetry(list(words))
        return render_template('display.html', result=words_poem)
    else:
        return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
