## Retraining BirdNET with an Active Learning Approach

### Overview

**BirdNET** is a convolutional neural network (CNN) trained to recognize the sounds of more than 6,500 birds, as well as other organisms (e.g., mammals) and even some environmental and anthropogenic sounds. Developed by the team at [K. Lisa Yang for Conservation Bioacoustics](https://github.com/kahst/BirdNET-Analyzer/tree/main) (Kahl et al. 2021), this tool is an amazing resource for automating the detection of target species in large acoustic datasets.

However, BirdNET has limitations when it comes to low-quality recordings (such as those from Passive Acoustic Monitoring using low-cost recorders like AudioMoths). Additionally, due to biases in the training data (e.g., differences in sound availability from repositories like XenoCanto and Macaulay Library), the model may underperform for some neotropical bird species or in highly diverse environments compared to its performance in Nearctic regions.

### Project Goals

The goal of this project is to adapt BirdNET to better recognize and classify Atlantic Forest nocturnal birds using 7,000 hours of recordings obtained with AudioMoth recorders. This active learning (AL) approach is designed to:
- **Improve performance on low-quality recordings.**
- **Be easily adaptable to other acoustic classification problems.**
- **Run on an ordinary computer with minimal computational resources.**

### Workflow Overview

The workflow involves running a series of Jupyter notebooks in a specified order, along with some additional data manipulation as needed. Below is a step-by-step guide:

1. **Training Set Tracker**  
   Run the `1-4-Training_set_tracker.ipynb` notebook to track all training files for the initial BirdNET retraining.  
   > **Note:** Re-run this notebook after each update to the training set.

2. **Uncertainty Sampling (Iteration 1)**  
   Run the `2-Dynamic_Uncertainty_sampling.ipynb` notebook to select clips for validation in your first active learning iteration.

3. **Clip Validation**  
   Validate your selected clips using your preferred method (e.g., Raven Pro).  
   - Generate a `.txt` annotation file for each validated class.
   - Rename the validated files to append the new annotated class at the end of the filename.
   - Move the validated files into their corresponding training class folders.  
   > *(Optional: A script can be created to automate the renaming and moving process.)*

   **Post-Validation:**  
   After validating your top-scoring clips per class, compute precision using the notebook.  
   - Create a DataFrame with columns `class` and `precision`.
   - Save this DataFrame as a `.csv` file in a specified directory.  
   This precision file will be used from iteration 2 onwards.  
   > **Important:** Update the path to this `precision.csv` in the `2-Cmplx_Uncertainty_sampling.ipynb` notebook for subsequent iterations.

4. **Update Training Set Tracker**  
   Re-run the `1-4-Training_set_tracker.ipynb` notebook and update the iteration parameter in the code:
   ```python
   current_iteration = 1  # Update this for each new iteration

5. **Perform Random Sampling**
Run `5-Random_sampling.ipynb`

6. **Repeat Steps**

    - Go back to step 3.
    - Then proceed to step 4.
   > **Note: Do not change the iteration number after step 4; update it only after retraining the model.**

    **Additional Notes**
   * Iteration 2 Onwards:
     From iteration 2 forward, include the generated `precision.csv` file in the `2-Dynamic_Uncertainty_sampling.ipynb` notebook.
   * Helper vs. Target Classes:
     For helper classes (e.g., Red Junglefowl, frogs) that you include in training:
     They are integrated into the uncertainty sampling process but are excluded from random sampling. This ensures that while their performance is monitored, they do not overwhelm the training set relative to the target classes.


By following the above steps, you can iteratively improve BirdNET's performance on your target dataset while managing class imbalances and efficiently using your annotation budget.

Feel free to reach out with any questions or suggestions for improvements!




