The file e1244_hw1.zip contains this README file,  the file TDOA_data.mat, a Matlab .mat data file, and the file mapimage.jpeg, an image of the IISc campus that indicate the anchors and the Transvahan e-vehicle.  This data file can be read, from within Matlab, simply by entering 

load TDOA_data.mat

The data contains the following variables


 Name                 	                 

  anchor_location      a 2x4  matrix containing the two-dimensional pixel co-ordinates of the anchor nodes a1, a2, a3, and a4                     
  target_location      a 2x1 vector containing the two-dimension pixel co-ordinates of the target, i.e., the transvahan x                     
  true_distances       a 4x1 vector containing the pairwise distances between the Transvahan and the anchors                    
  sigma2               a 10x1 vector containing different measurement noise variances.                   
  noisy_distances      a 4x1000x10 tensor containing 1000 realizations of the 4 pairwise distances between the Transvahan and the anchors. The  
                                  third dimension of the tensor contains these observations for 10 different noise variances collected in sigma2.      


To plot the estimated Transvahan location using different methods that you will develop, you may use the following example Matlab commands:

Im = imread('mapimage.jpeg');
figure(1); imshow(Im); hold on;
target_location = [807,809].'; %here the true target location is used for illustration 
plot(target_location(1),target_location(2),'x', 'MarkerSize',50);