# gender-in-plots

The purpose of the project is to look at gender disparities in terms of plot descriptions of movies and other stories on Wikipedia. Specifically, we use the count of gendered pronouns within plot descriptions as indicators of the gender of the most important characters.

## Source Code

extractplots.py
The function findplots takes a Wikipedia category and an output file name, and extracts all plots (anything with a subheader containing the word "plot") from each page in the category. It outputs plots to the output file, alternating between the title of the page and the contents of the plot description.

pronounAnalysis.py
From a file in the format extracted by extractplots.py (that is, alternating between title and plot descriptions), computes the counts of male and female pronouns. (he/him/himself/his, she/her/herself/hers)
For a single category, computes a scatterplot of the pronoun counts, and compute the ECDF of male vs female counts.
Also runs a permutation test for the data under the null hypothesis that the male and female pronoun counts came from the same distribution. For many categories, we see strong evidence that male pronouns are used significantly more than female pronouns, which suggests that the stories are really "about" men and boys, or at least that Wikipedia editors believe so.
For the data from moviesByYear, we can see that the trend over time within movies is for the counts to get closer together, but they are still different.

## Plotdata

Contains files obtained by extractplots.py. The files in moviesByYear use the movie categories from 1990-2018 which allow for an analysis of change over time.

## Figures

Contains figures created by pronounAnalysis.py.

## Acknowledgments

Inspired by https://github.com/markriedl/WikiPlots (and some code in the misc folder is based on this data)
