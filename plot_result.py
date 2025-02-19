from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np
import os
from scipy import interpolate
from scipy.interpolate import spline
# p =argparse.ArgumentParser()
# p.add_argument('--output_dir', type=str, default="/home/shapelim/KRoC_Results")
# p.add_argument('--test_data', type=str, default="inputs/np_test_data_1.csv")
# p.add_argument('--gt_dir', type=str, default="inputs/test_data_diagonal_curve2D.csv")
#In case of test 1
# p.add_argument('--uni', type=str, default= "/home/shapelim/KRoC_Results/1104_uni_poly.csv")
# p.add_argument('--bi', type=str, default= "/home/shapelim/KRoC_Results/1104_bi_poly.csv")
# p.add_argument('--multimodal_uni', type=str, default= "/home/shapelim/KRoC_Results/1104_unimul_poly.csv")
# p.add_argument('--multimodal_bi', type=str, default= "/home/shapelim/KRoC_Results/1104_bimul_poly.csv")

#In case of test 2
# p.add_argument('--bidirectional_LSTM_csv', type=str, default="results/RiTA/bi_lstm_to_curve_test.csv")
# p.add_argument('--stacked_bi_LSTM_csv', type=str, default="results/RiTA/stack_lstm_2.csv")
# p.add_argument('--unidirectional_LSTM_csv', type=str, default= "results/RiTA/uni_lstm_to_curve_test.csv")
# p.add_argument('--gru_csv', type=str, default= "results/RiTA/gru_to_curve_test.csv")
#
# p.add_argument('--trilateration_csv', type=str, default="results/RiTA/trilateration.csv")
# p.add_argument('--save_MSE_name', type=str, default="Distance_error_result__test2.png")
# p.add_argument('--save_error_percent_name', type=str, default="test_stack.png")
# p.add_argument('--save_trajectory_name', type=str, default="Test_trajectory11.png") #""Trajectory_result_refined_interval_10_smoothed_test_stack.png")
# p.add_argument('--data_interval', type=int, default= 21)

# args = p.parse_args()
'''
b blue
g green
r red
c cyan 
m magenta
y yellow
k balck
w white
'''
# COLORSET = [(0,0,1), 'g', 'r', 'm', 'c', 'y'] #, 'k','w']
COLORSET = [(241/255.0, 101/255.0, 65/255.0), (19/255.0, 163/255.0, 153/255.0), (2/255.0, 23/255.0, 157/255.0), (191/255.0, 17/255.0, 46/255.0)]
SOFT_COLORSET = [(241/255.0, 187/255.0, 165/255.0), (174/255.0, 245/255.0, 231/255.0), (115/255.0, 123/255.0, 173/255.0), (232/255.0, 138/255.0, 139/255.0)]
LINE = ['-', ':', '--', '-']
# LABEL = ['LSTM', 'GRU', 'Bi-LSTM', 'Stacked Bi-LSTM']
LABEL = ['uni', 'bi', 'multimodal_uni', 'multimodal_bi']

SMOOTHNESS = 200



class Visualization:
    def __init__(self, args):
        self.args = args
        self.folder_name = args.load_model_dir
        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)
        self.setGT(self.args.test_data)
        self.color_set = COLORSET
        self.label = LABEL

    def setGT(self, raw_csv_file):
        gt_xyz = np.loadtxt(raw_csv_file, delimiter=',')
        #x_array: gt_xy[:,0]
        #y_array: gt_xy[:,1]
        self.gt_xyz = gt_xyz[:, -3:]

    def _calDistanceError3D(self, predicted_result_dir):
        predicted_xyz = np.loadtxt(predicted_result_dir, delimiter=',')
        # gt_xy = np.random.randint(3,size = (4,2))
        # predicted_xy = np.random.randint(3, size = (4,2))
        dx_dy_dz_array = self.gt_xyz[4:] - predicted_xyz

        distance_square = np.square(dx_dy_dz_array[:,0]) \
                          + np.square(dx_dy_dz_array[:,1]) \
                          + np.square(dx_dy_dz_array[:,2])
        MSE = np.sum(distance_square)/distance_square.shape
        RMSE = np.sqrt(MSE)
        print ("RMSE: " + str(RMSE*100) + " cm")

        return np.sqrt(distance_square) , RMSE*100

    def plotDistanceError3D(self, *target_files_csv):
        plot_title = "Distance Error"
        plt.title(plot_title)
        # plt.rcParams['Figure.figsize'] = (14, 3)
        plt.figure(figsize=(7,4.326))
        for i, csv in enumerate(target_files_csv):

            distance_error, _ = self._calDistanceError3D(csv)
            distance_error = distance_error*100

            x_axis = range(distance_error.shape[0])

            # distance_error_refined = self.getRefinedData(distance_error, 30)
            # x_axis_refined = self.getRefinedData(x_axis, 30)

            # x_axis_refined, distance_error_refined = self.getSmoothedData(x_axis_refined, distance_error_refined)
            # x_axis = self.getRefinedData( x_axis, self.args.data_interval)
            # distance_error = self.getRefinedData( distance_error, self.args.data_interval)
            #marker o x + * s:square d:diamond p:five_pointed star


            # plt.plot(x_axis, distance_error, color= SOFT_COLORSET[i], #marker = marker,
            #                 linestyle = linestyle,label = self.label[i])

            plt.plot(x_axis, distance_error, color= self.color_set[i], #marker = marker,
                            linestyle = LINE[i],label = self.label[i])
            # plt.scatter(x_for_marker, distance_error_for_marker, color= self.color_set[i], marker = marker,
            #                 linestyle = linestyle) #,label = self.label[i])

        plt.legend()
        plt.grid(True)
        plt.xlim(0,1300)
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        plt.ylim(0.0,40)
        plt.xlabel("Time Step [t]")
        plt.ylabel("Distance Error [cm]")
        fig = plt.gcf()
        # plt.show()
        fig.savefig(self._3D_plot_name[:-4]+'_error.png')
        print ("Done")
    def getSmoothedData_3D(self,x_data, y_data, z_data):
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        z_data = np.array(z_data)

        tck, u = interpolate.splprep([x_data, y_data, z_data], s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        smoothed_x = out[0].tolist()
        smoothed_y = out[1].tolist()
        smoothed_z = out[2].tolist()

        return smoothed_x, smoothed_y, smoothed_z

    def getRefinedData(self, data, interval):
        count = 0
        refined_data = []
        for datum in data:
            if count%interval == 0 :
                refined_data.append(datum)
            count += 1
        return refined_data
    def plotErrorPercent(self,*target_files_csv):
        max_value = 0

        for i, csv in enumerate(target_files_csv):
            predicted_xy = np.loadtxt(csv, delimiter = ',')
            predicted_x = predicted_xy[:,0]
            predicted_y = predicted_xy[:,1]
        saved_file_name = self.args.save_error_percent_name
        # plot_title = "CDF of Distance Errors"
        # plt.title(plot_title)

        for i, csv in enumerate(target_files_csv):
            distance_error = self._calDistanceError(csv)
            x_axis = range(distance_error.shape[0])
            interval = 1000
            x_axis =np.linspace(0, np.max(distance_error), interval)
            y = [0]*interval
            for error in distance_error:
                min_residual = 100
                idx = 0
                for j, x in enumerate(x_axis):
                    residual = abs(x - error)
                    if (residual < min_residual):
                        idx = j
                        min_residual = residual
                y[idx] += 1

            y_axis =[0]*interval
            for s in range(interval):
                CDF_y_value = 0
                for t in range(interval):
                    if t <= s:
                        CDF_y_value += y[t]
                        y_axis[s] = CDF_y_value*100/distance_error.shape[0]

            x_axis = x_axis*100
            plt.plot(x_axis, y_axis, color=self.color_set[i],  # marker= marker,
                     linestyle=LINE[i], label=self.label[i])

        plt.grid(True)
        plt.xlim(0.0,40.0)
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        plt.ylim(0.0,100.0)
        plt.legend()
        # plt.xlim(-0.5,1.5)
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        # plt.ylim(-0.5,1.5)
        plt.xlabel("Distance Error [cm]")
        plt.ylabel("Percentage [%]")
        fig = plt.gcf()
        # plt.show()
        fig.savefig(saved_file_name)
        print("Done")

    def plot2DTrajectory(self, *target_files_csv):
        saved_file_name = self.args.save_trajectory_name
        plot_title = "Trajectory"
        # plt.title(plot_title)
        gt_x = self.gt_xyz[:,0]
        gt_y = self.gt_xyz[:,1]

        plt.figure(figsize=(8, 6))
        plt.plot(gt_x, gt_y,'k',linestyle='--' , label = 'GT')

        for i, csv in enumerate(target_files_csv):
            predicted_xy = np.loadtxt(csv, delimiter = ',')
            predicted_x = predicted_xy[:,0]
            predicted_y = predicted_xy[:,1]

            predicted_x = self.getRefinedData( predicted_x, self.args.data_interval)
            predicted_y = self.getRefinedData( predicted_y, self.args.data_interval)

            predicted_x, predicted_y = self.getSmoothedData(predicted_x, predicted_y)
            #marker o x + * s:square d:diamond p:five_pointed star

            plt.plot(predicted_x, predicted_y, color = self.color_set[i], #marker= marker,
                            linestyle = LINE[i],label = self.label[i])

        plt.legend()

        # plt.legend(bbox_to_anchor=(1, 1),
        #            bbox_transform=plt.gcf().transFigure)
        # plt.xlim(-0.5,1.5)
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        # plt.xticks(np.linspace(-0.5,1.5,10, endpoint =True))
        # plt.ylim(-0.5,1.5)
        plt.xlabel("X Axis [m]")
        plt.ylabel("Y Axis [m]")
        fig = plt.gcf()
        # plt.show()
        fig.savefig(saved_file_name)
        print ("Done")

    def set_3D_plot_name(self, name):
        self._3D_plot_name = name


    def drawResult3D(self, *target_files_csv):

        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(111, projection='3d')

        gt_x = self.gt_xyz[:,0]
        gt_y = self.gt_xyz[:,1]
        gt_z = self.gt_xyz[:,2]
        self.ax1.plot(gt_x, gt_y, gt_z, 'k', linestyle = '--', label = 'GT')

        for i, csv in enumerate(target_files_csv):
            predicted_xyz = np.loadtxt(csv, delimiter = ',')
            # print (predicted_xyz)
            predicted_x = predicted_xyz[:,0]
            predicted_y = predicted_xyz[:,1]
            predicted_z = predicted_xyz[:,2]

            # predicted_x = self.getRefinedData( predicted_x, self.args.data_interval)
            # predicted_y = self.getRefinedData( predicted_y, self.args.data_interval)
            # predicted_z = self.getRefinedData( predicted_z, self.args.data_interval)
            #
            # predicted_x, predicted_y, predicted_z = self.getSmoothedData_3D(predicted_x, predicted_y, predicted_z)

            plt.plot(predicted_x, predicted_y, predicted_z, color = self.color_set[i], #marker= marker,
                            linestyle = LINE[i],label = self.label[i])
        plt.legend()

        # self.ax1.scatter(X_list, Y_list, Z_list, c=c)
        self.ax1.set_zlim(0, 1.0)
        self.ax1.set_xlim(-0.75, 1.25)
        self.ax1.set_ylim(-1.0, 1.0)
        self.ax1.set_xlabel('X axis')
        self.ax1.set_ylabel('Y axis')
        self.ax1.set_zlabel('Z axis')
        self.fig = plt.gcf()
        self.fig.savefig(self._3D_plot_name)



if __name__ == "__main__":
    def drawResult3D(X_list, Y_list, Z_list, c):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')
        ax1.plot(X_list, Y_list, Z_list, c=c )
    def randrange(n, vmin, vmax):
        return (vmax - vmin)*np.random.rand(n) + vmin

    viz = Visualization(args)
    viz.set_3D_plot_name("hi.png")
    viz.drawResult3D()
    # test = np.loadtxt("train_yz3D.csv", delimiter= ',')
    # n = 10
    # for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    #     xs = randrange(n, 23, 32)
    #     ys = randrange(n, 0, 100)
    #     zs = randrange(n, zlow, zhigh)
    #     drawResult3D(xs, ys, zs, c)
    # plt.show()
    # X = test[:, 4]
    # Y = test[:, 5]
    # Z = test[:, 6]
    # viz.drawResult3D(X, Y, Z)
    # input = np.loadtxt("./inputs/3D_path_spiral.csv", delimiter = ',')
    # input = np.loadtxt("./inputs/3D_path_poly.csv", delimiter = ',')
    # x = input[:, 4]
    # y = input[:, 5]
    # z = input[:, 6]
    # viz.drawResult3D(args.uni) #, args.bi, args.multimodal_uni, args.multimodal_bi)
    # viz.plotDistanceError3D(args.multimodal_bi)
    # viz.plotErrorPercent(args.multimodal_bi)
    # viz.plot2DTrajectory(args.unidirectional_LSTM_csv, args.gru_csv, args.bidirectional_LSTM_csv, args.stacked_bi_LSTM_csv)

