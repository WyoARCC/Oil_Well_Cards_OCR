"""
This script will seperate PDF files based on the visual similarity of their
first pages. It will do this using clustering techniques.

Written by Cody Sloan
"""
import os
import shutil
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Model
from sklearn.cluster import Birch


def load_pdf_filenames(pdf_dir):
    """Takes a list ofmodel_vgg16mes and a path to a directory with PDFs, then
    adds all of the paths of the PDF files in that directory to the 
    filenames list.
    
    Parameters:
        filenames - List of PDF file paths as strings, initially empty.
        pdf_dir - String containing file system location of PDF files.
    Returns:
        filenames - Updated list of PDF file paths.
    """
    filenames = []
    # Scan recursively over all pdf files in a directory
    for folder, subfolders, files in os.walk(pdf_dir):
        for file in files:
            if file.endswith('.pdf'):
                #Add all the .pdf filenames to a list
                filename = os.path.join(folder, file)
                filenames.append(filename)
                
    return filenames
    
    
def convert_pdfs_to_imgs(filenames, path_to_poppler):
    """Takes a list of PDF file paths, and converts the first page of 
    each PDF to an image, and adds that image to an image list.
    
    Parameters:
        filenames - List of PDF file paths as strings.
        path_to_poppler - String containing the location of your poppler
            installation. This is usually the /bin/ directory in your 
            conda environment.
    Returns:
        imgs - List of images of the first page of each PDF.
    """
    imgs = []
    # Loop over all pdfs and convert the first page to an image
    for filename in filenames:
        # converts only the pdf files and adds them to the list
        img = convert_from_path(filename, \
                                first_page=1, \
                                last_page=1, \
                                poppler_path=path_to_poppler
                               )
        imgs.append(img[0])
        
    return imgs


def extract_features(images, model):
    """Takes a list of pillow images and uses a modified neural network model
    to extract features from those images.
    
    Parameters:
        images - List of images that are of type 'PIL.Image.Image'.
        model - A modified neural network.
    Returns:
        features - A list of each image's features.
    """
    feat = []
    # loop through each image in the dataset
    for img in images:
        # Resize the image to be 224x224
        img = img.resize((224,224))
        # convert from 'PIL.Image.Image' to numpy array
        img = np.array(img) 
        # reshape the data for the model reshape
        # (num_of_samples, dim 1, dim 2, channels)
        reshaped_img = img.reshape(1,224,224,3) 
        # prepare image for model
        imgx = preprocess_input(reshaped_img)
        # get the feature vector
        feat.append(model.predict(imgx))
    
    # get a list of just the features
    features = np.array(feat)
    # Remove the extra image dimension required for the model prediction
    features = features.reshape(-1, model.output.shape[1])
    
    return features


def birch_train(filenames, features, num_clusters, thresh=0.01):
    """Trains the BIRCH clustering algorithm on inputted features. Creates
    <num_clusters> clusters based on those features.
    
    Parameters:
        filenames - List of filenames that need to be clustered.
        features - List of features extracted from images.
        num_clusters - Target number of clusters.
        thresh - Threshold: the maximum number of data points a sub-cluster in
            the leaf node of the clustering features tree can hold.
    Returns:
        clusters - A dictionary where the keys are cluster numbers and the
            values are filenames.
        birch - The trained BIRCH clustering model.
    """
    # Train the algorithm and find the training set's clusters
    birch = Birch(threshold=thresh, n_clusters=num_clusters).fit(features)
    # Create the clusters dictionary with filename values
    clusters = {}
    for file, label in zip(filenames, birch.labels_):
        # If the key isn't in the dict, add it
        if label not in clusters.keys():
            clusters[label] = []
        # Add the file to its cluster
        clusters[label].append(file)
    return clusters, birch


def find_clusters(filenames, features, alg, num_clusters, thresh=0.01):
    """Uses a trained birch clustering algorithm model to cluster files based
    on inputted features. Creates <num_clusters> clusters.
    
    Parameters:
        filenames - List of filenames that need to be clustered.
        features - List of features extracted from images.
        alg - The trained clustering algorithm model.
        num_clusters - Target number of clusters.
        thresh - Threshold: the maximum number of data points a sub-cluster in
            the leaf node of the clustering features tree can hold.
    Returns:
        clusters - A dictionary where the keys are cluster numbers and the
            values are filenames
    """
    # Find which cluster each image belongs to
    labels = alg.fit_predict(features)
    # Create the clusters dictionary with filename values
    clusters = {}
    for file, label in zip(filenames, labels):
        # If the key isn't in the dict, add it
        if label not in clusters.keys():
            clusters[label] = []
        # Add the file to its cluster
        clusters[label].append(file) 
    return clusters

     
def view_cluster(cluster_num, cluster_dict, path_to_poppler, page=1):
    """Allows viewing of images in a cluster. Only 100 images can be displayed
    at a time, but this function allows you to choose which 'page' of 100
    images you want to see. This is useful when you want to test the
    clustering methods in a notebook file.
    
    Parameters:
        cluster_num - Number of cluster you would like to view.
        cluster_dict - A dictionary containing files and the clusters they
            belong to.
        path_to_poppler - String containing the location of your poppler
            installation. This is usually the /bin/ directory in your 
            conda environment.
        page - Number of section of 100 images to be viewed in the cluster.
            For Ex: page=2 means you would like to view images 100-200 of that
            cluster.
    """
    plt.figure(figsize = (25,25));
    # gets the list of filenames for a cluster
    files = cluster_dict[cluster_num]
    # only allow up to 30 images to be shown at a time
    if len(files) > 100:
        if page == 1:
            print(f"Loading first 100 files out of {len(files)}")
            files = files[:100]
        elif page <= 0:
            print("Page must be 1 or greater")
        else:
            files = files[(page-1)*100 : page*100]
            print(f"Loading files {(page-1)*100}-{((page-1)*100)+len(files)}")
    # plot each image in the cluster
    for index, file in enumerate(files):
        plt.subplot(10,10,index+1)
        img = convert_from_path(file, \
                                first_page=1, \
                                last_page=1, \
                                poppler_path=path_to_poppler
                               )
        img = np.array(img[0])
        plt.imshow(img)
        plt.axis('off')
    plt.show()
                
        
def save_cluster(clusters, save_dir):
    """Saves the cluster. This will copy the PDF files to their cluster
    location in the file system.
    
    Parameters:
        clusters - A dictionary containing files and the clusters they
            belong to.
        save_dir - Location of cluster subdirectories that files will be
            separated into.
    """
    for cluster in clusters:
            for file in clusters[cluster]:
                full = os.path.join(save_dir, 'cluster'+str(cluster+1), \
                                    os.path.basename(file))
                shutil.copyfile(file, full)            
    return


def separate_dataset(filenames, save_dir, model, path_to_poppler, \
                     algorithm, batch_size=1000):
    """Seperates the non-training data into their clusters.
    
    Parameters:
        filenames - The names of the files that will be separated.
        save_dir - The directory that each cluster directory will be found in.
        model - The model that will extract the data's features
        path_to_poppler - String containing the location of your poppler
            installation. This is usually the /bin/ directory in your 
            conda environment.
        algorithm - The trained clustering algorithm model that will do the
            seperating of the files.
        batch_size - The size of the batch of files that will be clustered at
            a time.
    """
    # Loop over all batches of data
    for i in range(0, len(filenames), batch_size):
        batch = filenames[i:i+batch_size]
        # Grab image data
        images = convert_pdfs_to_imgs(batch, path_to_poppler)
        # Extract features from images
        features = extract_features(images, model)
        # Use extracted features to cluster the data
        clusters = find_clusters(batch, features, algorithm, num_clusters=4)
        # Save the clusters
        save_cluster(clusters, save_dir)
    return
                
def main():
    # Set the seed for randomizing data
    np.random.seed(123)
    
    # Load the filenames list and shuffle it randomly
    print("Loading Filenames ... ", end='')
    pdf_dir = r'/project/arcc-students/enhanced_oil_recovery_cards/'
    filenames = load_pdf_filenames(pdf_dir)
    np.random.shuffle(filenames)
    print("Finished")
    
    # Load the model, removing the fully connected layers so it can be used
    # for feature extraction.
    print("Loading ResNet50 Model ... ", end='')
    model = ResNet50()
    model = Model(inputs = model.inputs, outputs = model.layers[-2].output)
    print("Finished")
    
    print("Training Clustering Algorithm ... ", end='')
    # Define the training set
    split = 500
    train = filenames[:split]
    # Convert PDFs in training set to images
    path_to_poppler = r'/project/arcc-students/csloan5/environments/GPU_env/bin/'
    images = convert_pdfs_to_imgs(train, path_to_poppler)
    # Extract features from training data
    features = extract_features(images, model)
    # Generate clusters from training data, and also train the clustering
    # algorithm
    clusters, birch = birch_train(train, features, num_clusters=4)
    # Save the training data clusters
    save_dir = r'/project/arcc-students/csloan5/OilWellCards_project/sorted_cards/'
    save_cluster(clusters, save_dir)
    print("Finished")
    
    print("Clustering Files ... ", end='')
    # Cluster and separate the non-training data
    filenames = filenames[split:]
    separate_dataset(filenames, save_dir, model, path_to_poppler, birch, \
                     batch_size=500)
    print("Finished")
    print("Separation Completed")
    return


if __name__ =='__main__':
    main()
