# Differentiable Neural Computer, for Pytorch

[![Build Status](https://travis-ci.org/ixaxaar/pytorch-sublstm.svg?branch=master)](https://travis-ci.org/ixaxaar/pytorch-sublstm) [![PyPI version](https://badge.fury.io/py/sublstm.svg)](https://badge.fury.io/py/sublstm)

This is an implementation of subLSTM described in the paper [Cortical microcircuits as gated-recurrent neural networks, Rui Ponte Costa et al.](https://arxiv.org/abs/1711.02448)

## Install

```bash
pip install pytorch-sublstm
```


## Usage

**Parameters**:

Following are the constructor parameters:

| Argument | Default | Description |
| --- | --- | --- |
| input_size | `None` | Size of the input vectors |
| hidden_size | `None` | Size of hidden units |
| rnn_type | `'lstm'` | Type of recurrent cells used in the controller |
| num_layers | `1` | Number of layers of recurrent units in the controller |
| num_hidden_layers | `2` | Number of hidden layers per layer of the controller |
| bias | `True` | Bias |
| batch_first | `True` | Whether data is fed batch first |
| dropout | `0` | Dropout between layers in the controller |
| bidirectional | `False` | If the controller is bidirectional (Not yet implemented |
| nr_cells | `5` | Number of memory cells |
| read_heads | `2` | Number of read heads |
| cell_size | `10` | Size of each memory cell |
| nonlinearity | `'tanh'` | If using 'rnn' as `rnn_type`, non-linearity of the RNNs |
| gpu_id | `-1` | ID of the GPU, -1 for CPU |
| independent_linears | `False` | Whether to use independent linear units to derive interface vector |
| share_memory | `True` | Whether to share memory between controller layers |


### Example usage:

#### nn Interface
```python
import torch
from torch.autograd import Variable
from subLSTM.nn import SubLSTM

hidden_size = 20
input_size = 10
seq_len = 5
batch_size = 7
hidden = None

input = Variable(torch.randn(batch_size, seq_len, input_size))

rnn = SubLSTM(input_size, hidden_size, num_layers=2, bias=True, batch_first=True)

# forward pass
output, hidden = rnn(input, hidden)
```

#### Cell Interface

```python
import torch
from torch.autograd import Variable
from subLSTM.nn import SubLSTMCell

hidden_size = 20
input_size = 10
seq_len = 5
batch_size = 7
hidden = None

hx = Variable(torch.randn(batch_size, hidden_size))
cx = Variable(torch.randn(batch_size, hidden_size))

input = Variable(torch.randn(batch_size, input_size))

cell = SubLSTMCell(input_size, hidden_size, bias=True)
(hx, cx) = cell(input, (hx, cx))
```

Attributions:
A lot of the code is recycled from [pytorch](https://pytorch.org)


