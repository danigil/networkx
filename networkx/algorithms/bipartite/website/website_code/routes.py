import networkx as nx
from . import app
from .forms import EnvyFreeMatchingForm, Button, EdgeItem, EnvyFreeMatchingCSVForm
from .algorithms import envy_free_matching
from flask import render_template, redirect, url_for, request
from pandas import read_csv

@app.route('/')
def home_page():
    return render_template('home.html', title='Envy Free Bipartite Matching')

@app.route('/article')
def article_page():
    return render_template('article.html', title='Envy Free Bipartite Matching Article')
df = None
@app.route("/algo1", methods=['GET', 'POST'])
def algo1_page():
    form = EnvyFreeMatchingCSVForm()
    if not form.validate_on_submit():
        return render_template('algo1.html', title='Algo1', form=form)
    else:
        input_file = form.file.data
        global df
        df = read_csv(input_file, header=None)


        print("input: \n",df)
        # return redirect(url_for(".calc1_page", filename=""))
        return redirect("/calculate1")
    # form = EnvyFreeMatchingForm()
    #
    # add_button = Button("Add Edge")
    # remove_button = Button("Remove Edge")
    #
    # if add_button.validate_on_submit():
    #     print("bingus")
    #     form.edges.append_entry()
    #
    #
    # if remove_button.validate_on_submit():
    #     print("dddddingus")
    #     form.edges.pop_entry()
    #
    # if not form.validate_on_submit():
    #     return render_template('algo1.html', title='Algo1', form=form,addButton=add_button,removeButton=remove_button)


    # else:
    #     myhome.homepage = form.homepage.data
    #     return redirect(url_for(myhome.__name__))

@app.route("/calculate1")
def calc1_page():
    calc_response()
    return render_template('article.html', title='Envy Free Bipartite Matching Article')

def calc_response():

    global df
    gen = df.itertuples(index=False, name=None)
    top_nodes = next(gen)
    matching = next(gen)
    print("top: ",top_nodes)
    print("matching: ",matching)

    df = df.drop([0,1])
    # df = df.iloc[: , :-1]
    print(df)
    edges = [(tup[0],tup[1]) for tup in gen]

    G = nx.Graph(edges)

    matching_ret = envy_free_matching.envy_free_matching(G,top_nodes=top_nodes)
    matching_edges = list(filter(lambda tup: tup[0] in matching_ret, edges))


