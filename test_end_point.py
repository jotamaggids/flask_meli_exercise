import requests
import random
import time

start = time.time()


def create_single_column():
    x = 0
    dna_ch = ['A', 'C', 'G', 'T']
    dna_chain = []
    while 6 > x:
        random.shuffle(dna_ch)
        string_one = ''.join(dna_ch)
        if x == 5:
            dna_chain.append('A')
        else:
            dna_chain.append(string_one[0])
        x = x + 1

    one_chain = ''.join(dna_chain)
    return one_chain


def create_single_chain():
    i = 0
    dna_ch = ['A', 'C', 'G', 'T']
    dna_chain = []
    while 6 > i:
        random.shuffle(dna_ch)
        string_one = ''.join(dna_ch)
        dna_chain.append(string_one[0])
        i = i + 1

    one_chain = ''.join(dna_chain)
    return one_chain


def create_single_row(i):
  x = 0
  dna_chain = []
  dna_ch = ['A', 'C', 'G', 'T']
  if i == 4:
    dna_chain.append('TCCCAA')
  else:
    while 6>x:
      random.shuffle(dna_ch)
      string_one = ''.join(dna_ch)
      if x == 5:
        dna_chain.append('A')
      else:
        dna_chain.append(string_one[0])
      x = x + 1

  one_chain = ''.join(dna_chain)
  return one_chain

i = 0
while 100>i:
    z = 0
    dna_chain_complete_column = []
    while 6 > z:
        single_chain = create_single_chain()
        dna_chain_complete_column.append(single_chain)
        z = z + 1

    # api-endpoint
    URL = "http://134.209.126.163:5000/api/v1/resources/mutant"

    # defining a params dict for the parameters to be sent to the API

    r = requests.post(URL, json={"dna": dna_chain_complete_column})
    print(r.json())
    i = i + 1

end = time.time()
print(end - start)