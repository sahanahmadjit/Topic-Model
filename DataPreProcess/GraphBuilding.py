import csv
import networkx as nx

mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"

G= nx.DiGraph()
def building_graph_from_text_data():
  for itaration in range(2):
    with open(linux_data_directory + 'GraphData/GraphInputData_Test.txt') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter='|')
      for line in csv_reader:
        if itaration==0:
          G.add_node(line[0])
          continue
        else:
          for i in range(1,len(line),2): # 1:Starting from 2nd term {first term is source}, stop, increment by 2
            G.add_edge(line[0],line[i],weight=line[i+1])

def print_Graph():
  print(G.edges(data='weight'))

def export_Graph_to_Gephi_format():
  nx.write_gexf(G,linux_data_directory+"GraphData/gephi_format_graph_test.gexf")


building_graph_from_text_data()

def main_Graph_Building_function():
  building_graph_from_text_data()
  print_Graph()
  export_Graph_to_Gephi_format()


main_Graph_Building_function()
