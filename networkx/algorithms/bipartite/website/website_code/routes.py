import pandas

import networkx as nx
from . import app
from .forms import EnvyFreeMatchingForm, Button, EdgeItem, EnvyFreeMatchingCSVForm, EnvyFreeMatchingCSVAndTextForm
from .algorithms import envy_free_matching
from flask import render_template, redirect, url_for, request, flash
from pandas import read_csv


@app.route('/')
def home_page():
    return render_template('home.html', title='Envy Free Bipartite Matching')


@app.route('/article')
def article_page():
    return render_template('article.html', title='Envy Free Bipartite Matching Article')


df = pandas.DataFrame()
top_nodes = []


@app.route("/algo1", methods=['GET', 'POST'])
def algo1_page():
    form = EnvyFreeMatchingCSVAndTextForm()
    if not form.validate_on_submit():
        return render_template('algo1.html', title='Algo1', form=form)
    else:


        input_file = form.file.data
        input_text = form.top_nodes.data

        if input_file and input_text:
            print(input_text)

            global top_nodes
            top_nodes = [int(num) for num in input_text.split(',')]
            flash(f'Calculating, top_nodes: {top_nodes}!', 'success')
            global df
            df = read_csv(input_file, header=None)

            print("input: \n", df)
            # return redirect(url_for(".calc1_page", filename=""))
            return redirect("/calculate1")
        else:
            flash(f'ERROR',category="error")
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


@app.route("/calculate1")
def calc1_page():
    calc_response()
    return render_template('article.html', title='Envy Free Bipartite Matching Article')


def calc_response():
    global df
    global top_nodes

    print(df)
    edges = [tup for tup in df.itertuples(index=False, name=None)]

    G = nx.Graph(edges)

    matching_ret = envy_free_matching.envy_free_matching(G, top_nodes=top_nodes)
    matching_edges = list(filter(lambda tup: tup[0] in matching_ret, edges))
