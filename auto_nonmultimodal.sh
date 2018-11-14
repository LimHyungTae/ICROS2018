#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal2/" --lr 0.0009
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal2/" --lr 0.0009
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal3/" --epoch 1200
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal3/" --epoch 1200
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal4/"
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal4/"
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal5/" --decay_rate 0.8
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal5/" --decay_rate 0.8
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal6/" --decay_rate 0.78
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal6/" --decay_rate 0.78
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal7/" --decay_rate 0.9 --decay_step 7
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal7/" --decay_rate 0.9 --decay_step 7
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal8/" --decay_rate 0.9 --decay_step 7 --epoch 1200
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal8/" --decay_rate 0.9 --decay_step 7 --epoch 1200
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal9/" --decay_rate 0.95 --decay_step 8
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal9/" --decay_rate 0.95 --decay_step 8
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal10/" --lr 0.0008
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal10/" --lr 0.0008
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal11/" --lr 0.0008 --epoch 1200
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal11/" --lr 0.0008 --epoch 1200
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal12/" --lr 0.0008 --decay_step 4
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal12/" --lr 0.0008 --decay_step 4
#
python3 train_non_multimodal.py --save_dir "/home/shapelim/RONet/non_multimodal13/" --lr 0.0008 --decay_step 4 --epoch 1200
python3 test_non_multimodal.py --load_model_dir "/home/shapelim/RONet/non_multimodal13/" --lr 0.0008 --decay_step 4 --epoch 1200

