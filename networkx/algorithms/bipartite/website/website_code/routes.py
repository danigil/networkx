import pandas

import networkx as nx
from . import app
from .forms import EnvyFreeMatchingForm, Button, EdgeItem, EnvyFreeMatchingCSVForm, EnvyFreeMatchingCSVAndTextForm
from .algorithms import envy_free_matching
from flask import render_template, redirect, url_for, request, flash, json
from pandas import read_csv
import json

@app.route('/')
def home_page():
    return render_template('home.html', title='Envy Free Bipartite Matching')


@app.route('/article')
def article_page():
    return render_template('article.html', title='Envy Free Bipartite Matching Article')


# edges = pandas.DataFrame()
# top_nodes = []


@app.route("/algo1", methods=['GET', 'POST'])
def algo1_page():
    form = EnvyFreeMatchingCSVAndTextForm()
    if not form.validate_on_submit():
        return render_template('algo1.html', title='Algo1', form=form)
    else:
        input_file = form.file.data
        input_text = form.top_nodes.data

        if input_file and input_text:
            # print(input_text)

            # global top_nodes
            top_nodes = [int(num) for num in input_text.split(',')]

            # global edges
            edges = read_csv(input_file, header=None)
            edges = [tup for tup in edges.itertuples(index=False, name=None)]
            # if not is_valid_input_csv("non_weighted", edges):
            #     flash(f'ERROR edge csv file is malformed', category="error")
            #     return render_template('algo1.html', title='Algo1', form=form)
            # else:
            flash(f'Calculating, top_nodes: {top_nodes}!', 'success')
            # print("input: \n", edges)
            return redirect(url_for(".calc1_page", edges=json.dumps(edges), top_nodes=json.dumps(top_nodes)))
                # return redirect("/calculate1")
        else:
            flash(f'ERROR missing input',category="error")
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
    edges = json.loads(request.args['edges'])
    top_nodes = json.loads(request.args['top_nodes'])

    print("edges: ",edges)
    print("top_nodes: ", top_nodes)
    calc_response(edges, top_nodes)

    return render_template('article.html', title='Envy Free Bipartite Matching Article')





valid_input_csv_functions = {
    "non_weighted": lambda df: df.applymap(lambda x: type(x) == int and x > 0).all().all()
}
def is_valid_input_csv(type, df):
    return valid_input_csv_functions[type](df)

def calc_response(edges, top_nodes):
    G = nx.Graph(edges)

    matching_ret = envy_free_matching.envy_free_matching(G, top_nodes=top_nodes)
    matching_edges = list(filter(lambda tup: matching_ret[tup[0]] == tup[1], edges))
    print("ret: ", matching_edges)
