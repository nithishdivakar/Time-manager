import pprint
import re
import time

'''
Reads in a file. Build the sytax tree which is a ditionary 
having a hierarchy structure.

'''
TIME_FORMAT = "%Y-%b-%d %H:%M:%S"



def parse_time(raw_time_string):
  ''' 
  Parse  time in  whatever  format  that is  given and  convert it to 
  standard  format specified by `TIME_FORMAT`.  If values are missing 
  in the original raw string, then todays's value are taken.
  '''
  raw_time_string = raw_time_string.strip()
  from dateutil.parser import parse as parse_time_func

  time_struct = parse_time_func(raw_time_string)
  formated_time_string = time_struct.strftime(TIME_FORMAT)

  return formated_time_string

def add_task_to_node(Node,raw_task_data):
  '''
  Add a task to a node.
  Adds a pair tuple to the node. (payload,link). 'payload' is the raw
  task and 'link' is node that is child of 'Node'
  '''
  subtask_node = {}
  task = {}
  ETA = time.strptime("9998-Jan-01 00:00:00", TIME_FORMAT)
  '''
  The raw task data is a string which  contains many pairs of keys in 
  form `[ key : value ]` Just find all those things and add them as
  task details
  '''
  parsed_data = re.findall(
                  r"\[\s*(.*?)\s*:\s*(.*?)\s*\]",
		  raw_task_data
		)

  for key,value in parsed_data:
    if key in ['eta']:
      value = parse_time(value)
      ETA = time.strptime(value,TIME_FORMAT)

    task[key] = value

  '''
  We need a unique  key to index  this task  among all task  added to 
  this node. The best way to do that is to hash the task's data.
  '''
  unique_key = hash(raw_task_data)
  Node[unique_key] = (task,subtask_node,ETA)
  return subtask_node

def create_syntax_tree(file_path):
  syntax_tree = {}
  with open(file_path,'r') as f:
    roots_at_level = {}
    ''' 
    root at level 0 is the syntax tree itself
    '''
    roots_at_level[0] = syntax_tree

    for line in f.readlines():
      '''
      Get the  level of task.  Is it a main  task or a sub  task etc. 
      Level of a task is given  by its  indentation.  So count  no of 
      double spaces in the begining of the red line from the file.
      '''
      level = int((len(line) - len(line.lstrip(' ')))/2)
      '''
      Add the task as a child to the root at the level
      '''
      new_root = add_task_to_node(roots_at_level[level], line.strip()) 
      '''
      If the new task added was a child of previous task,  change the 
      root of the next level
      '''
      roots_at_level[level+1] = new_root
  return syntax_tree


def task_to_string(syntax_tree_node):
  task_subtask_node,eta = syntax_tree_node

### test code

def task_node_to_string(task,indent):
  string = ["  "*indent,]
  for key in task:
    #if key == 'title': continue
    string.append('[{} : {}]'.format(key,task[key]))
  return ''.join(string)

def syntax_tree_to_string(D,indent=0):
 KEYS = sorted(list(D.keys()),key = lambda k: D[k][2])
 string = []
 for key in KEYS:
   task,subtask,eta = D[key]
   string.append(task_node_to_string(task,indent))
   if subtask:
     string.append(
       syntax_tree_to_string(subtask,indent=indent+1)
     )
 return '\n'.join(string)

if __name__ == "__main__":
  import sys
  D = create_syntax_tree(sys.argv[1])
  print(syntax_tree_to_string(D))
