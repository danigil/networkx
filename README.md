# Envy Free Matchings in Bipartite Graphs Website
A website that demonstrates the algorithms for finding maximum envy-free matchings
in bipartite graphs.

### Getting started
First, create a new virtual environment and clone the project locally.
Make sure that all the relevant packages are installed.
Now, you need to run the project. Go to: ```networkx -> algorithms -> bipartite ->website```.
Run the file: ```run.py```. After these steps, the website should run. To use the website, open your
browser and write: ```localhost:5000```. After doing so, you should be able to see the next screen:![image](https://github.com/danigil/networkx/assets/93070344/e870d217-d509-4e6f-baa4-b04a3a5a0d8f)

### Working with the website
From the home screen, you can navigate to other screens.
For example, you can read the paper that the code was based on. You can do it by simply pressing
the "Article" button above or the link below.
The article page should look like this:
![image](https://github.com/danigil/networkx/assets/93070344/91767ef7-32e6-4afe-8d3a-2693621ad4af)
By pressing the buttons "Next" and "Previous" you can read the whole paper.

Now, for the demonstration of the algorithms. Press the button "Algorithms". It should show 2 options:
"NON Weighted Envy Free Matching" and "Weighted Envy Free Matching". The next explanation will be on the non-weighted version, the weighted
version is similar.

The page should look like this:
![image](https://github.com/danigil/networkx/assets/93070344/88a1abc3-df7e-41c3-ad55-efb36f634e98)

You can insert your graph (as pair of edges like in the example). After you have done so, press the "submit" button. 
The following page should display a graph that contains the maximum matching of the graph. The edges are colored with green
color and an explanation can be found below the graph:
![image](https://github.com/danigil/networkx/assets/93070344/91db5591-bd01-446f-9fe0-cc7a9ca52df0)
Press the button "Next Step" to advance with the algorithm steps.
The following page should display a graph that contains the maximum matching and the EFM partition. The vertices that are colored with  
blue color are associated with the sets X<sub>L</sub> and Y<sub>L</sub>. The vertices that are colored with red colors are associated with the sets 
 X<sub>S</sub> and Y<sub>S</sub> and as before, you can find the explanation below.
 
 The page should look like this:
 ![image](https://github.com/danigil/networkx/assets/93070344/0f125b03-5bf7-448a-a636-00dd42aeb830)
 For the final step, press again the button "Next Step". On the final page, you can find a graph with the maximum envy-free matching.
 The matching corresponded to the sub-matching: M[X<sub>L</sub>, Y<sub>L</sub>] where M is the maximum matching. The maximum envy-free matching
 painted with a blue color and as before, the explanation can be found below the graph.

 The page should look like this:
 ![image](https://github.com/danigil/networkx/assets/93070344/51cfb9d9-182e-467c-8c43-69c6acc45fc8)

* The only difference between the non-weighted and the weighted versions is that in the non-weighted version, the input includes a pair of vertices that represent
an edge (for example 5,4 7,4 5,3 7,2 8,2 6,1 5,1) and in the weighted version the input includes also the weight of the edge 
(for example: 5,4,1.0 7,4,111.0 5,3,1.0 7,2,1.0 8,2,1.0 6,1,1.0 5,1,1.0 7,3,1.0)

Created by: Benjamin Saldman and Daniel Gilkarov, Ariel University.
