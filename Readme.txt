This Repository Contains notebooks that help us organize our data and perform model validation. 

The one_hot_labeled_evalse.ipynb notebook help us create a multiclass one hot encoded dataframe for 
manually labeled recordings comparing the timestamp of manual annotations with the 3 second segments 
implemented by BirdNET and decide wheter a 3 s segments has a detection (1) or not (0).
The user can set a % of overlap between segments and also modify the duration of the segments. 
This is an adaptation of a notebook provided in the OpenSoundscape Repository. 

Then the one-hot_encodedBirdNET.ipynb is a notebook that compiles all the .txt files with BirdNET 
predictions into one single dataframe and creates a multiclass one-hot encoded dataframe. 

The continuous-score_labels.ipynb is a notebook that compiles all the .txt files with BirdNET 
predictions into one single dataframe and creates a multiclass continuous score dataframe that 
is to say that above each class (columns) and 3 second segment of every file (rows) it puts
the continuous score predicted by BirdNET for that specific segment and class. If there is no 
prediction it leaves a blank space.


