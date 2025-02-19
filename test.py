import tensorflow as tf
import tensorflow.contrib.seq2seq as seq2seq
from lstm_network import RONet
import numpy as np
import DataPreprocessing
from plot_result import Visualization
from tqdm import tqdm, trange
import os
import argparse
import csv
from search_min_loss_file import search_min_loss_meta_file

os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3' #,1,2,3'
tf.set_random_seed(777)  # reproducibilityb
# hyper parameters
p =argparse.ArgumentParser()

#FOR TRAIN
#Train folder is essential for data_parser.fitDataForMinMaxScaler()!!
p.add_argument('--train_data', type=str, default="/home/shapelim/RONet/train_Karpe_181025/")

p.add_argument('--lr', type=float, default = 0.0001)
p.add_argument('--decay_rate', type=float, default = 0.7)
p.add_argument('--decay_step', type=int, default = 5)
p.add_argument('--epoches', type=int, default = 1500)
p.add_argument('--batch_size', type=int, default = 11257)

#NETWORK PARAMETERS
p.add_argument('--output_type', type = str, default = 'position') # position or pose
p.add_argument('--hidden_size', type=int, default = 3) # RNN output size
p.add_argument('--num_uwb', type=int, default = 8) #RNN input size: number of uwb
p.add_argument('--preprocessing_output_size', type=int, default = 50)
p.add_argument('--first_layer_output_size', type=int, default = 400)
p.add_argument('--second_layer_output_size', type=int, default = 500)
p.add_argument('--sequence_length', type=int, default = 5) # # of lstm rolling
p.add_argument('--output_size', type=int, default = 3) #position: 3 / pose: 6
p.add_argument('--network_type', type=str, default = 'test') #uni / bi
p.add_argument('--is_multimodal', type=bool, default = True) #True / False
#Loss terms
p.add_argument('--alpha', type=float, default = 1) #True / False
p.add_argument('--beta', type=float, default = 0)
p.add_argument('--gamma', type=float, default = 0) #True / False

#FOR TEST
p.add_argument('--load_model_dir', type=str, default="/home/shapelim/RONet/test_cudnn2/")
p.add_argument('--test_data', type=str, default='inputs/np_test_data_1.csv')
# p.add_argument('--test_data', type=str, default='inputs/np_test_2.csv')
FILE_NAME = '1109_bimul'
###########
args = p.parse_args()

min_loss_meta_file_name = search_min_loss_meta_file(args.load_model_dir)

print ("Meta files: ", min_loss_meta_file_name)

data_parser = DataPreprocessing.DataManager(args.train_data, args.sequence_length, args.num_uwb)
data_parser.fitDataForMinMaxScaler()
data_parser.transform_all_data()

print ("Set transformation complete")
tf.reset_default_graph()
ro_net = RONet(args)
viz = Visualization(args)
saver = tf.train.Saver(max_to_keep = 5)


# COUNT PARAMS
total_num_parameters = 0
for variable in tf.trainable_variables():
    total_num_parameters += np.array(variable.get_shape().as_list()).prod()
print("number of trainable parameters: {}".format(total_num_parameters))

###########for using tensorboard########
merged = tf.summary.merge_all()
########################################

with tf.Session() as sess:
   #For save diagonal data
        saver.restore(sess, min_loss_meta_file_name)
        # saver.restore(sess, args.load_model_dir)
        print ("Load success.")

        data_parser.set_dir(args.test_data)
        if args.is_multimodal:
            data_parser.set_val_data(args.test_data)
            data_parser.transform_all_data()
            # data_parser.set_data_for_8multimodal()
            data_parser.set_data_for_8multimodal_all_sequences()
            d0_data, d1_data, d2_data, d3_data, d4_data, d5_data, d6_data, d7_data = data_parser.get_range_data_for_8multimodal()

            prediction = sess.run(ro_net.pose_pred, feed_dict={ro_net.d0_data: d0_data,
                                                               ro_net.d1_data: d1_data,
                                                               ro_net.d2_data: d2_data,
                                                               ro_net.d3_data: d3_data,
                                                               ro_net.d4_data: d4_data,
                                                               ro_net.d5_data: d5_data,
                                                               ro_net.d6_data: d6_data,
                                                               ro_net.d7_data: d7_data}) #prediction : type: list, [ [[[hidden_size]*sequence_length] ... ] ]
        else:
            X_data = data_parser.set_range_data()
            prediction = sess.run(ro_net.pose_pred, feed_dict={ro_net.X_data: X_data}) #prediction : type: list, [ [[[hidden_size]*sequence_length] ... ] ]


        prediction = prediction[:, -1, :]

        data_parser.inverse_transform_by_train_data(prediction)

        output_csv = args.load_model_dir + FILE_NAME +".csv"
        output_plot = args.load_model_dir + FILE_NAME +".png"
        data_parser.write_file_data(output_csv)
        viz.set_3D_plot_name(output_plot)
        viz.drawResult3D(output_csv)
        viz.plotDistanceError3D(output_csv)
        _, rmse = viz._calDistanceError3D(output_csv)

        f = open(args.load_model_dir + FILE_NAME + "_RMSE.txt", 'w')
        f.write(str(rmse))
        f.close()