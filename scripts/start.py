from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
import numpy as np
import os,sys
from time import time as t
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import argparse
import tensorflow as tf
import time


import hashlib
import json
from urllib.parse import urlparse
from uuid import uuid4
from pymongo import MongoClient
import urllib.request,json
from bson import json_util
from flask_cors import CORS


def init_db(result):
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['firexitdb']
    collection = db['exit1']
    serverstatus = db.command("serverStatus")
    if (result=="blocked"):
        db.exit1.replace_one({"status":"unblocked"},{"status":"blocked"})
    else:
        db.exit1.replace_one({"status":"blocked"},{"status":"unblocked"})
    
def firebase_initialize():
    cred = credentials.Certificate("auth.json")
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://emergencyexit-18356.firebaseio.com'
    })
    #ref = db.reference('users')

# labeling image
def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

# Global Variables


      
# Global Variables
def conf():
      file_name = "frame.png"
      model_file = "tf/retrained_graph.pb"
      label_file = "tf/retrained_labels.txt"
      input_height = 224
      input_width = 224
      input_mean = 128
      input_std = 128
      input_layer = "input"
      output_layer = "final_result"
      
      '''''
      parser = argparse.ArgumentParser()
      parser.add_argument("--image", help="image to be processed")
      parser.add_argument("--graph", help="graph/model to be executed")
      parser.add_argument("--labels", help="name of file containing labels")
      parser.add_argument("--input_height", type=int, help="input height")
      parser.add_argument("--input_width", type=int, help="input width")
      parser.add_argument("--input_mean", type=int, help="input mean")
      parser.add_argument("--input_std", type=int, help="input std")
      parser.add_argument("--input_layer", help="name of input layer")
      parser.add_argument("--output_layer", help="name of output layer")
      args = parser.parse_args()
    
      if args.graph:
        model_file = args.graph
      if args.image:
        file_name = args.image
      if args.labels:
        label_file = args.labels
      if args.input_height:
        input_height = args.input_height
      if args.input_width:
        input_width = args.input_width
      if args.input_mean:
        input_mean = args.input_mean
      if args.input_std:
        input_std = args.input_std
      if args.input_layer:
        input_layer = args.input_layer
      if args.output_layer:
        output_layer = args.output_layer
      '''''
      graph = load_graph(model_file)
      t = read_tensor_from_image_file(file_name,
                                      input_height=input_height,
                                      input_width=input_width,
                                      input_mean=input_mean,
                                      input_std=input_std)
    
      input_name = "import/" + input_layer
      output_name = "import/" + output_layer
      input_operation = graph.get_operation_by_name(input_name);
      output_operation = graph.get_operation_by_name(output_name);
    
      with tf.Session(graph=graph) as sess:
        start = time.time()
        results = sess.run(output_operation.outputs[0],
                          {input_operation.outputs[0]: t})
        end=time.time()
      results = np.squeeze(results)
    
      top_k = results.argsort()[-5:][::-1]
      labels = load_labels(label_file)
      #print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
    
      #for i in top_k:
      #  print(labels[i], results[i])
      return (labels[2],results[2])
      


# In[3]:


if __name__ == "__main__":
  i=0
  firebase_initialize()
  cap = cv2.VideoCapture('rtmp://192.168.0.7:1935/flash/11:admin:admin1')
  #cap = cv2.VideoCapture(0)
  flag = False
  while(True):
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('rtmp://192.168.0.7:1935/flash/11:admin:admin1')
    ret, frame = cap.read()
    if ret==True:
        cv2.imshow('frame',frame)
        cv2.imwrite("frame.png",frame)
        #os.system('python3 scripts/label_image.py --graph=tf/retrained_graph.pb')
        label,value = conf()
        i+=1
        if(value<0.70):
            if (flag == False):
                flag = True
                start = t()
            elif((flag==True) & ((t()-start) >= 30)): 
                print('Blocked!')
                #db.reference().child('exit1').child('status').set('blocked')
                init_db("blocked")
                print('DB updated')
                flag = False
        else:
            if(flag==True):
                if((t()-start) >= 30):
                    #db.reference().child('exit1').child('status').set('Not blocked')
                    init_db("unblocked")
                    print('DB updated')
                    flag = False
        cap.release()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

