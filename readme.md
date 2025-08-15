# 📡 Sionna System-Level Wireless Network Simulator

A comprehensive, modular system-level simulator for wireless cellular networks built on NVIDIA's Sionna framework. This project provides a clean, maintainable architecture for simulating multi-cell wireless scenarios with advanced features like power control, scheduling, link adaptation, and channel modeling.

## 🚀 Features

- **🏗️ Modular Architecture**: Clean separation of concerns with organized package structure
- **📡 Multi-Cell Simulation**: Hexagonal grid topology with interference modeling
- **⚡ Advanced Power Control**: Downlink fair power allocation and uplink power control
- **📊 Link Adaptation**: Outer Loop Link Adaptation (OLLA) with MCS selection
- **🎯 Intelligent Scheduling**: Proportional Fair (PF) scheduling for SU-MIMO
- **📈 Comprehensive Analysis**: Built-in visualization and performance metrics
- **🔧 GPU Optimized**: Configured for high-performance GPU acceleration
- **🤖 ML/RL Ready**: Architecture designed for easy integration of machine learning algorithms

## 🏛️ Architecture

```
project_root/
├── config/                     # Configuration and parameters
│   ├── simulation_config.py    # All simulation parameters
│   └── __init__.py
├── models/                     # Core simulation models
│   ├── channel_matrix.py       # Channel modeling with fading
│   ├── system_simulator.py     # Main system-level simulator
│   └── __init__.py
├── utils/                      # Utility functions
│   ├── stream_management.py    # MIMO stream management
│   ├── sinr_utils.py          # SINR calculations
│   ├── results_utils.py       # Results processing
│   └── __init__.py
├── visualization/              # Plotting and analysis
│   ├── plots.py               # Performance visualization
│   └── __init__.py
├── simulation/                 # Simulation execution
│   ├── run_simulation.py      # Main simulation runner
│   └── __init__.py
└── main.py                    # Entry point
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended)
- TensorFlow 2.x

### Dependencies
```bash
pip install sionna
pip install tensorflow
pip install matplotlib
pip install numpy
```

### Quick Start
```bash
git clone https://github.com/yourusername/sionna-system-level-simulator.git
cd sionna-system-level-simulator
python main.py
```

## 📊 Simulation Scenarios

### Supported 3GPP Scenarios
- **UMi**: Urban Micro-cell
- **UMa**: Urban Macro-cell  
- **RMa**: Rural Macro-cell

### Key Parameters
- **Multi-cell topology**: Hexagonal grid with configurable rings
- **Users per sector**: Configurable (default: 10)
- **Carrier frequency**: 3.5 GHz (configurable)
- **Bandwidth**: Configurable OFDM parameters
- **Channel models**: 3GPP TR 38.901 compliant

## 🎯 Use Cases

### Research Applications
- **5G/6G Performance Analysis**: System-level performance evaluation
- **Algorithm Development**: Testing new power control, scheduling algorithms
- **Interference Studies**: Multi-cell interference analysis
- **ML/RL Integration**: Training ground for intelligent network optimization

### Educational Applications
- **Wireless Communications**: Hands-on learning of cellular concepts
- **System Design**: Understanding trade-offs in network design
- **Performance Analysis**: Learning about KPIs and optimization

## 📈 Performance Metrics

The simulator provides comprehensive performance analysis:

- **Throughput**: Per-user and system-wide data rates
- **Fairness**: Jain's fairness index and proportional fairness
- **Quality**: SINR, BLER, MCS distribution
- **Efficiency**: Power consumption and spectral efficiency
- **Mobility**: Support for user movement and handovers

## 🔧 Configuration

All simulation parameters are centralized in `config/simulation_config.py`:

```python
# Key configurable parameters
SCENARIO = 'umi'                    # 'umi', 'uma', 'rma'
DIRECTION = 'downlink'              # 'uplink', 'downlink'
NUM_RINGS = 1                       # Hexagonal grid rings
NUM_UT_PER_SECTOR = 10             # Users per sector
CARRIER_FREQUENCY = 3.5e9          # Hz
NUM_SLOTS = 1000                   # Simulation duration
```

## 📊 Example Results

The simulator generates comprehensive visualizations:
- CDF plots of key performance metrics
- Network topology visualization
- SINR vs MCS correlation analysis
- Power control effectiveness
- Scheduling fairness analysis

## 🤖 ML/RL Integration Ready

The modular architecture makes it easy to integrate machine learning:
- **Plug-in RL agents** for power control
- **Neural network schedulers** replacing traditional algorithms
- **Intelligent beam management** with deep learning
- **Predictive channel estimation** using ML

## 🔬 Research Extensions

This simulator serves as a foundation for:
- **Multi-agent reinforcement learning** for network optimization
- **Federated learning** in wireless networks
- **Digital twin** development for cellular networks
- **6G research** and beyond-5G technologies

## 📚 Documentation

### Key Components
- **SystemLevelSimulator**: Main simulation engine
- **ChannelMatrix**: Channel modeling with fading
- **Stream Management**: MIMO configuration
- **Power Control**: Fair allocation algorithms
- **Scheduling**: Proportional fair scheduling

### Extending the Simulator
The modular design allows easy extension:
1. Add new algorithms in respective modules
2. Extend configuration parameters
3. Add new visualization functions
4. Integrate ML/RL agents

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- New channel models
- Additional scheduling algorithms
- ML/RL integration examples
- Performance optimizations
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NVIDIA Sionna Team**: For the excellent Sionna framework
- **3GPP**: For standardized channel models and scenarios
- **Open Source Community**: For the foundational libraries

## 📞 Contact

For questions, suggestions, or collaborations:
- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for general questions

## 🏷️ Keywords

`sionna` `wireless-communications` `5g` `6g` `system-level-simulation` `tensorflow` `cellular-networks` `power-control` `scheduling` `link-adaptation` `machine-learning` `reinforcement-learning` `multi-cell` `mimo` `ofdm`

---

⭐ **Star this repository if you find it useful for your wireless communications research or learning!**
