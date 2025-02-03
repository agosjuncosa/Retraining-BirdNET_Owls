### Retraining BirdNET with an Active Learning approach

#### Explained workflow only for AL

BirdNET is a CNN trained to recognize the sounds of more than 6,500 birds and other organisms such as mammals and the latest version is capable of detecting some environmental and anthropogenic sounds. It was developed by a team working at the K. Lisa Yang for Conservation Bioacoustics (Kahl et al. 2021) and it is openly available on [Github](https://github.com/kahst/BirdNET-Analyzer/tree/main). 
This is an amazing tool to automatize the detection of target species on large amounts of acoustic data. However, this model has a low performance on low-quality recordings like those obtained from Passive Acoustic Monitoring, especially if using low-cost recorders like AudioMoths. Moreover, some have documented that due a bias in sound availability from different regions in the libraries used to train the model like XenoCanto and Macaulay Library, the model does not perfom well for some neotropical bird species or in highly diverse environments as it does in recordings from neartic regions. 

To tackle these issues and be able to automatize the recognition (detection & classification) of the Atlantic Forest nocturnal birds from 7,000 h of recordings made with PAM using AudioMoth recorders I am developing this approach. Moreover this solution is intended to be easy adaptable to other problems and be able to develop in an ordinary computer.  
The workflow I proposed involve the use of the notebooks in this repository in an ordered manner and also maybe some other extra data manipulation. 


1- Run the ```1-5-Training_set_tracker.ipynb``` to track down all the trainig files you have for the first retrining of BirdNET. This file should be re run after each edits made into the training set. 

2- Run the ```2-Cmplx_Uncertainty_sampling.ipynb``` to select the clips to validate in your first active learning iteration. 

3- Run the ```3-7-Rename_del_score.ipynb``` file to remove the first part of the selected files. 

4- Validate your files using the method you prefer. I will use Raven Pro and I will generate a .txt annotation file for each validated class. Then rename the validated files using this code. This way you will have all your clips named as before with the addition at the end of the filename the new annotated class. Then, you can move the validated files into their corresponding training class folders. (I can create a code to automatize this). 
*After validate your top scoring clips per class, with your .txt annotations files created for each class, compute precision using this notebook. Create a df with a column named class and other named precision and save all the computed precision in a .csv in a specified directory. This will be used in the next iteration (only from iteration 2 onwards), at that time you will need to update the path to this precision.csv in the ```2-Cmplx_Uncertainty_campling.ipynb```.

5- Re-run the ```1-long_Training_set_tracker.ipynb``` by changing the parameter accordingly.
```python
current_iteration = 1  # Update this for each new iteration
```
6- Run ```4-Random_sampling.ipynb``` 

7- Go back to step 3. 

8- Go back to step 4.

9- Go back to step 5, remember this time do not change the iteration number. The number should be changed after retraining the model. 

#### END - (from iteration 2 onwards, include precision.csv in Cmplx_Uncertainty_sampling.ipynb). 




