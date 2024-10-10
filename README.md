# HTM

This repository contains an implementation of the Hierarchical Temporal Memory (HTM) model invented by Jeff Hawkins. The HTM model, inspired by the structure and function of the human neocortex, is a computational framework for machine learning tasks that involve sequence prediction, anomaly detection, and learning time-based patterns. This version includes basic building blocks for an HTM system, with modules for spatial and temporal memory processing.

## Project Structure

The repository includes the following key components:

- **`cathy_encoder.py`**: Custom encoder module that translates input data into a Sparse Distributed Representation (SDR) compatible with the HTM model.
- **`numeric_encoder.py`**: Provides encoding functions for numerical data, allowing data to be represented in an SDR format.
- **`spatial_pooler.py`**: Implements the Spatial Pooler algorithm, which converts encoded data into SDRs to enable robust pattern recognition and noise tolerance.
- **`spatial_pooler_neuron.py`**: Defines individual neurons and their properties within the Spatial Pooler component.
- **`temporal_memory_v3.py`**: Contains the Temporal Memory (TM) algorithm, enabling the model to learn and recall sequences of SDRs over time.
- **`segment.py`** and **`segment_ls.py`**: Define and manage synaptic segments, the structures connecting cells within the Temporal Memory, storing sequence-based information.
- **`synapse.py`**: Manages synaptic connections between neurons, defining learning and activation mechanisms.
- **`test.py`**: Unit testing module that verifies the functionality and integrity of the individual components.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/czhang29/Hierarchical-Temporal-Memory-model.git
   ```

2. **Install Dependencies**: Ensure you have Python installed, along with any dependencies listed in `requirements.txt`.

## Usage

You can run the individual modules or use `test.py` to validate the components:
```bash
python test.py
```

For more detailed usage and example applications, refer to the inline comments and function docstrings within each module.

## Contributing

We welcome contributions to improve this implementation of HTM. If you find any issues or have suggestions, please feel free to open an issue or submit a pull request.

---

This README provides an overview and guides for understanding and utilizing the key components of the HTM model in this repository. Let me know if you’d like additional sections, such as advanced usage or theoretical background!
