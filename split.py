import os
import glob
import numpy as np


#goal: when I have a directory structure that looks like this:
# -data
#   -cats(contains all cat images)
#   -dogs(contains all dog images)
#   -elephants(contains all elephant images)
#
#It needs to end up like this:
# -data
#   -train
#       -cats
#       -dogs
#       -elephants
#   -validation
#       -cats
#       -dogs
#       -elephants
#
#where the train directory has 75% of the files and the validation has 25% of the files.

def create_dataset(directory):
    #directory == directory where dataset is located
    if not os.path.exists(directory):
        return 0
    #change to dataset directory as wkdir
    os.chdir(directory)
    work_dir = os.getcwd()

    #list with all subdirectories of the dataset directory
    dir_list = get_immediate_subdirectories(directory)

    #remove train and validation folder form the subdirectories
    if "train" in dir_list:
        dir_list.remove("train")
    if "valid" in dir_list:
        dir_list.remove("valid")

    #get path to train and valid
    train_dir = os.path.abspath('train')
    valid_dir = os.path.abspath('valid')

    #if train or valid does not exist: mkdir
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    if not os.path.exists(valid_dir):
        os.mkdir(valid_dir)

    #loop trough dir_list, all names are directories and also labels
    for data_dir in dir_list:
        label = data_dir
        print('Started moving: ' + str(label))

        #get list for current class directory
        image_list = [os.path.basename(x) for x in glob.glob(os.path.join(directory, label) + '\*.jpg')]

        #create directory for the classes in train and validation directory
        if not os.path.exists(os.path.join(train_dir, label)):
            os.mkdir(os.path.join(train_dir, label))
        if not os.path.exists(os.path.join(valid_dir, label)):
            os.mkdir(os.path.join(valid_dir, label))

        #move all images in the right directory
        move_images(directory, train_dir, valid_dir, image_list, label)

        print('Finished moving: ' + str(label))


def move_images(directory, train_dir, valid_dir, image_list, label):
    #shufles all images
    random_set = np.random.permutation(len(image_list))

    #select 80% of the images at random
    train_list = random_set[:round(len(random_set) * 0.8)]

    #selects all images minus training images
    valid_list = random_set[-(len(image_list) - len(train_list))::]

    train_images = []
    valid_images = []
    #adds the images to the train/valid_images with regards to the shuffled index
    for index in train_list:
        train_images.append(image_list[index])
    for index in valid_list:
        valid_images.append(image_list[index])

    #moves the images to their respective folders
    for train_image in train_images:
        os.rename(os.path.join(directory, label, train_image), os.path.join(train_dir, label, train_image))
    for valid_image in valid_images:
        os.rename(os.path.join(directory, label, valid_image), os.path.join(valid_dir, label, valid_image))

    os.removedirs(os.path.join(directory, label))

#https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
def get_immediate_subdirectories(data_directory):
    return [name for name in os.listdir(data_directory)
            if os.path.isdir(os.path.join(data_directory, name))]

#call the function to create dataset
create_dataset("C:\\Users\\Alex Chen\\Desktop\\Data\\Garbage classification\\Garbage classification")