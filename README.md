# Data Engineering assignment
Due to the hurry, I did not perform all of the necessary operations, instead describing missing parts.
I hope I wrote enough to sample code and the way of my thinking behind it.

## How to build and run the code
- Create a project, choose an env with Pandas or create new and install it.
- Copy the data and src files into the project.
- Run task.py

I assumed that requirements.txt is not necessary, while the only non-built-in dependency is Pandas.

## Documentation on your approach, i.e. what did you do and why?

After loading the data, I reformat the data frame, so:
- affiliations are listed,
- names are separated from surnames,
- names are split into parts.

What also should be done is normalising the format to avoid problems with encoding, different ways of writing
the same names and so on.

Then I cleanse and separate unique affiliations. It would be good to normalise the same ones into the
exact same names for further use while finding unique authors.

Next step is to get unique authors. Note, that the expected input should be modified - there is a possibility
that there are two authors with the exact same name. Then the third row would be affiliations, if not 
intersecting, so they can be further checked later.

First I sort the df by surnames (easier debug), then I split it into parts basing on surnames. 
This approach allows easier comparison, also reducing the computation costs - comparing names with each
other may scale up exponentially with number of distinct names and its variants in the group. The cons of 
this approach is that is may put an author with slightly different format of surname in different groups. This 
exception should be handled in the future. Good alternative might be to split groups by the affiliations,
if those would be reformatted good enough to be trusted.

After recording the obvious cases, the names and initials itself are compared. That is described in 
extensive comment in get_unique_authors() method.


## A reporting of potential failure points and bottlenecks.

Potential failure points:
- different format of input, multiple inputs, distorted input,
- differing format of names and surnames,
- large differences in affiliation names of the same affiliation.

Potential bottlenecks:
- larger input data could be too much for the memory and should be split,
- large amount of authors with the same surname would slow down the process,
- when put to production, verification versus growing number of authors would get slower,
 some way of dividing them into indexed groups would counter that if the speed is required, ex. API.

## An accounting of the remaining steps needed before putting deploying your code to a production system.

- upgrading load_data(), so its able to get data from multiple sources, formats, larger data
- sending/saving outcomes
- comparing new data not only to itself, but also to previously saved outcomes, so, effectively, 
also adding functionality getting previous outcomes
- indexing authors in groups and getting more data about them, to be able to join it with other tables,
so its usable and also to distinguish different people with the same name,
- optimising operations like reformatting or filtering
- freezing requirements; connecting with some input and output destination; maybe dockerising, 
if required for some reason.