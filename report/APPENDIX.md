# Appendix: all research areas and subtopics

NeurIPS 2026: 9,110 papers in 20 areas and 150 subtopics. Shares are % of all papers of that year; 2025 (5,859 papers) is mapped onto the 2026 subtopics. ★ = orals + spotlights in 2026.

## LLM Behavior & Safety — 943 papers (10.4%, 2025: 9.1%)

Interpretability, evaluation, sycophancy, hallucination, jailbreaks, unlearning, knowledge editing, steering and watermarking of language models, plus diffusion LMs, audio LMs and recommendation.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| LLM Self-Explanation and Hidden Computation | These papers probe what computations transformers perform internally, such as in-context learning, copying, belief states and hidden reasoning over filler tokens. | 102 | 1.18% → 1.12% | 4 |
| LLM Benchmarking and LLM-as-a-Judge | These papers study how LLMs are evaluated, covering benchmark design and reliability, judge bias, leaderboard rankings and AI peer review. | 99 | 0.87% → 1.09% | 8 |
| LLM Behavioral Tendencies and Evaluation Awareness | Evaluating LLM behaviors such as sycophancy, deception, confirmation bias, moral reasoning, risk attitudes and evaluation awareness. | 96 | 0.68% → 1.05% | 3 |
| Decoding for Diffusion Language Models | These papers develop masked and discrete diffusion language models, focusing on parallel decoding, speculative sampling, unmasking strategies and RL post-training. | 91 | 0.55% → 1.00% | 6 |
| Speech and Audio Language Models | Large audio language models, speech recognition, speech enhancement, audio generation and sign language recognition. | 91 | 0.97% → 1.00% | 3 |
| Jailbreak and Red-Teaming Attacks | Designs, scales and detects jailbreak and red-teaming attacks on LLMs, multimodal and diffusion language models, along with safety defenses. | 77 | 0.92% → 0.85% | 5 |
| Robustness of LLM Safety Alignment | These papers study how safety alignment and refusal behavior in LLMs and multimodal models hold up, break under jailbreaks or fine-tuning, and can be made more robust. | 68 | 0.58% → 0.75% | 3 |
| LLM Hallucination Detection and Mitigation | Detecting and reducing hallucinations in LLMs and vision-language models using uncertainty, token-level signals and training. | 56 | 0.60% → 0.61% | 0 |
| LLM Personas, Sycophancy and Cultural Bias | These papers measure how LLMs simulate personas and opinions and how they show sycophancy, stereotypes and cultural or value biases. | 55 | 0.29% → 0.60% | 2 |
| LLM Knowledge Editing and Forgetting | These papers update or edit the factual knowledge stored in LLMs and study the forgetting and memorization that happen during continual post-training. | 51 | 0.79% → 0.56% | 2 |
| Sequential and Generative Recommendation | These papers model user preferences for sequential, multimodal and generative recommendation, increasingly with LLMs and diffusion models. | 45 | 0.44% → 0.49% | 0 |
| Machine Unlearning in LLMs | These papers remove the influence of specific training data from models, mainly LLMs, while preserving utility and resisting relearning. | 40 | 0.55% → 0.44% | 2 |
| Activation Steering of LLMs | Controlling language model behaviour at inference time by editing internal activations with steering vectors or subspace interventions. | 36 | 0.19% → 0.40% | 3 |
| Watermarking Generative Model Outputs | Embedding and detecting watermarks in LLM text, images and audio to trace AI-generated content. | 36 | 0.49% → 0.40% | 0 |

Orals: [ALTER: An Allen's Algebra-Based Evaluation Framework for Temporal Reasoning of LLMs](https://neurips.cc/virtual/2026/poster/139265); [Benchmark Health Index: A Systematic Framework for Benchmarking the Benchmarks of LLMs](https://neurips.cc/virtual/2026/poster/138960); [Catch-Only-One: Non-Transferable Examples for Model-Specific Authorization](https://neurips.cc/virtual/2026/poster/151014); [CLIOPATRA: Extracting Private Information from LLM Insights](https://neurips.cc/virtual/2026/poster/152543); [CURE: Counterfactual Unsafe-token Re-masking for Diffusion Large Language Model Test-time Alignment](https://neurips.cc/virtual/2026/poster/151876); [Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing](https://neurips.cc/virtual/2026/poster/152494); [HearSayBench: Can LLMs Navigate from Abstract Human Rights to Lived Lives?](https://neurips.cc/virtual/2026/poster/139278); [Leaderboard Hacking: Preference-Based Model Evaluations are Vulnerable to Manipulation](https://neurips.cc/virtual/2026/poster/152085); [Learning to Audit ML Models with Theory of Mind](https://neurips.cc/virtual/2026/poster/155783); [LittleLearner: Language Models Under Pedagogically-Controlled Knowledge Exposure](https://neurips.cc/virtual/2026/poster/148220); [LoRAcles: Self-Supervised Weight-Space Interpretability at Scale](https://neurips.cc/virtual/2026/poster/154333); [Neural Chameleons: Language Models Can Learn to Hide Their Thoughts from Unseen Activation Monitors](https://neurips.cc/virtual/2026/poster/148241); [The Attacker in the Mirror: Breaking Self-Consistency in Safety via Anchored Bipolicy Self-Play](https://neurips.cc/virtual/2026/poster/151513); [We Should Distinguish Unlearning From Untraining](https://neurips.cc/virtual/2026/poster/140062)

## 3D Vision & Perception — 781 papers (8.6%, 2025: 10.4%)

Feed-forward and Gaussian-splatting 3D reconstruction, 3D scene grounding, LiDAR perception, medical imaging, restoration, anomaly and OOD detection, and image forensics.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Feed-Forward Multi-View Geometry Transformers | Builds and accelerates feed-forward and streaming multi-view geometry transformers for 3D reconstruction, camera pose, depth and panoramic geometry estimation. | 103 | 1.25% → 1.13% | 6 |
| Medical Imaging and Pathology Models | Segmentation, representation learning and vision-language models for radiology, CT and whole-slide pathology images. | 93 | 0.94% → 1.02% | 3 |
| Image Restoration and Inverse Problems | Denoising, super-resolution, image fusion and plug-and-play or diffusion-based restoration of degraded images. | 93 | 1.28% → 1.02% | 2 |
| Object Detection and OOD Detection | Develops open-world, domain-adaptive and long-tailed object detectors and methods for detecting out-of-distribution inputs in vision models. | 74 | 0.87% → 0.81% | 2 |
| LiDAR and Radar Perception for Driving | These papers handle LiDAR, radar and multi-sensor data for localization, point-cloud registration, scene flow and HD map construction in driving and UAV settings. | 71 | 0.73% → 0.78% | 1 |
| 3D Gaussian Splatting | These papers improve 3D Gaussian splatting and neural rendering for novel view synthesis, including feed-forward reconstruction, compression and densification. | 66 | 0.99% → 0.72% | 2 |
| Language-Grounded 3D Scene Understanding | These papers ground language in 3D scenes for open-vocabulary understanding, spatial reasoning, affordances and localization using point clouds, multi-view images and 3D-LLMs. | 64 | 0.99% → 0.70% | 6 |
| Anomaly Detection Across Modalities | These papers detect anomalies in industrial images, time series, graphs, video and audio, including zero-shot and few-shot settings. | 57 | 0.67% → 0.63% | 0 |
| 4D Reconstruction from Monocular Video | Recovering dynamic 3D geometry, motion and human or object animation from monocular or multi-view video. | 54 | 0.85% → 0.59% | 5 |
| AI-Generated Image and Deepfake Detection | Detecting and localizing AI-generated images, deepfake videos and image tampering for media forensics. | 45 | 0.61% → 0.49% | 5 |
| Domain Adaptation and Generalization | These papers transfer models across distribution shifts through unsupervised, source-free and graph domain adaptation and domain generalization. | 34 | 0.67% → 0.37% | 0 |
| Multi-View Clustering and Person Re-ID | Learns fused representations across multiple views or modalities for multi-view clustering, incomplete multi-view learning and person or object re-identification. | 27 | 0.55% → 0.30% | 3 |

Orals: [BEAST3D: animal behavioral analysis and neural encoding from multi-view video via Gaussian splatting](https://neurips.cc/virtual/2026/poster/149762); [Certifiably Optimal Robust Angular Synchronization](https://neurips.cc/virtual/2026/poster/153331); [Consistent 3D Surface Flow Model with Global State](https://neurips.cc/virtual/2026/poster/148758); [Déjà View: Looping Transformers for Multi-View 3D Reconstruction](https://neurips.cc/virtual/2026/poster/154303); [Non-Colliding Biometric Identities for Digital Entities: Geometry, Capacity, and Million-Scale Virtual Identity Provisioning](https://neurips.cc/virtual/2026/poster/153119); [Releasing Anchors from Cross-View Correspondence: Probabilistic Multi-View Anchor Graph Clustering](https://neurips.cc/virtual/2026/poster/154593); [SAM 3D Animal: Promptable Animal 3D Reconstruction from Images in the Wild](https://neurips.cc/virtual/2026/poster/155674); [Trellis4D: Complex 4D Mesh Generation](https://neurips.cc/virtual/2026/poster/153899); [Video Forensic Self-Descriptions: Leveraging Temporally Distributed Forensic Microstructures for Zero-Shot Detection of AI-Generated Videos](https://neurips.cc/virtual/2026/poster/149484)

## LLM Agents — 700 papers (7.7%, 2025: 3.5%)

Benchmarks, memory, skills, safety, multi-agent coordination and multi-turn training for tool-using and coding LLM agents, plus human oversight of AI decisions.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Tool-Use, Web and GUI Agent Benchmarks | Benchmarks and evaluation suites for tool-using, web, GUI and professional-workflow language agents. | 113 | 0.38% → 1.24% | 3 |
| LLM Agent Reliability and Efficiency | Making LLM agents more reliable, safe and cost-efficient through tool-call decisions, failure prediction, abstention and resource control. | 88 | 0.29% → 0.97% | 6 |
| Human-AI Collaboration and Oversight | Position and empirical papers on human oversight, AI-assisted decisions, governance and how AI systems should be evaluated with people. | 80 | 0.63% → 0.88% | 11 |
| LLM Agent Safety and Prompt Injection | Benchmarks and defends LLM, computer-use and multi-agent systems against prompt injection, unsafe actions, sabotage and scheming. | 76 | 0.32% → 0.83% | 2 |
| LLM Multi-Agent Systems | Designing, training and evaluating teams of collaborating or debating LLM agents, including coordination and orchestration. | 73 | 0.41% → 0.80% | 3 |
| Long-Term Memory for LLM Agents | These papers build and benchmark memory systems that let LLM agents store, retrieve and update past experience over long dialogues and tasks. | 66 | 0.12% → 0.72% | 1 |
| Skill Libraries for LLM Agents | LLM agents that discover, store, reuse and evolve skills to solve long-horizon web, embodied and tool-use tasks. | 58 | 0.31% → 0.64% | 3 |
| Coding Agents and SWE Benchmarks | These papers benchmark and train LLM coding agents on repository-level software engineering, long-horizon development and debugging tasks. | 55 | 0.20% → 0.60% | 1 |
| Multi-Turn LLM Dialogue and Agent RL | Reinforcement learning, credit assignment and evaluation for LLMs in multi-turn conversations and interactive agent tasks. | 48 | 0.43% → 0.53% | 2 |
| Multimodal Agents for Search and Deep Research | These papers evaluate and train multimodal LLM agents for web search, deep research, tool use and embodied decision-making, mostly through new benchmarks. | 43 | 0.44% → 0.47% | 2 |

Orals: [AgentAbstain: Do LLM Agents Know When Not to Act?](https://neurips.cc/virtual/2026/poster/139558); [Agent Security is a Systems Problem](https://neurips.cc/virtual/2026/poster/140106); [APS: Bias-Controlled Adaptive Prototype Simulation for Population-Scale LLM Agents](https://neurips.cc/virtual/2026/poster/149524); [ExComm: Exploration-Stage Communication for Error-Resilient Agentic Test-Time Scaling](https://neurips.cc/virtual/2026/poster/154319); [GenAI Evaluation Results are Largely Artifacts of Evaluation Design Choices: Evidence from Audit Studies of Resume Screening](https://neurips.cc/virtual/2026/poster/138976); [HeMeR: Heterogeneous Memory Reconciliation for Embodied Agents via Structured KV Reuse](https://neurips.cc/virtual/2026/poster/148497); [LITMUS: Benchmarking Behavioral Jailbreaks of LLM Agents in Real OS Environments](https://neurips.cc/virtual/2026/poster/150415); [MLS-Bench: A Holistic and Rigorous Assessment of AI Systems on Building Better AI](https://neurips.cc/virtual/2026/poster/139626); [Offloading Score: Measuring AI Reliance through Counterfactual Workflows](https://neurips.cc/virtual/2026/poster/139388); [Resilience Matters for Embodied Agents System: New Metrics, Systematic Evaluation, and Optimization](https://neurips.cc/virtual/2026/poster/148940); [SMART: Scalable Multi-Agent Role-conditioned Teaming via LLM-free Tree Search](https://neurips.cc/virtual/2026/poster/149874); [Soteria: Formally Verified Planning with Runtime Enforcement for Safe LLM Agents](https://neurips.cc/virtual/2026/poster/154927)

## DL Theory & Neuroscience — 691 papers (7.6%, 2025: 8.1%)

Learning dynamics and generalization theory, representation geometry, attribution and sparse autoencoders, plus brain decoding, spiking networks, quantum ML, verification and neural combinatorial optimization.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Deep Network Theory and Learning Dynamics | These papers analyse ReLU and residual networks theoretically, covering implicit bias, incremental learning, parameter symmetries, identifiability and feature learning. | 114 | 1.43% → 1.25% | 10 |
| Geometry of Learned Representations | Analyzes and designs embedding spaces using manifold, hyperbolic, Riemannian, spherical and topological structure for representation learning. | 69 | 0.73% → 0.76% | 6 |
| Grokking, Memorization and Generalization Theory | Explains why overparameterized networks generalize, covering grokking, double descent, memorization versus generalization and compression-based bounds. | 68 | 0.63% → 0.75% | 4 |
| Shapley Values and Feature Attribution | These papers develop and critique post-hoc explanation methods such as Shapley values, integrated gradients and causal attributions for model predictions. | 62 | 0.82% → 0.68% | 5 |
| Recurrent Network Dynamics in Neuroscience | Analyzes learning and dynamics in low-rank RNNs, Hopfield networks and reservoirs as models of neural circuits and memory. | 57 | 0.65% → 0.63% | 6 |
| Neural Combinatorial Optimization | Learned solvers, often diffusion or RL based, for routing, SAT, MILP and other constraint satisfaction problems. | 56 | 0.97% → 0.61% | 3 |
| Quantum Machine Learning | Applies machine learning to quantum systems and studies quantum neural networks, circuits, kernels, tomography and neural quantum states. | 42 | 0.22% → 0.46% | 0 |
| Brain Encoding and Neural Recording Analysis | Models fMRI, EEG and spiking recordings with encoding models, connectivity estimation and neural data tokenizers, plus connectomics benchmarks. | 42 | 0.97% → 0.46% | 4 |
| EEG and Physiological Foundation Models | Foundation models, benchmarks and datasets for EEG, ECG and other physiological signals in clinical and brain-computer interface settings. | 41 | 0.29% → 0.45% | 2 |
| Spiking Neural Networks | These papers train and analyse spiking neural networks for energy-efficient neuromorphic computing, using learnable delays, neuron models and plasticity rules. | 37 | 0.44% → 0.41% | 1 |
| Neural Network Verification and Backdoors | Formal verification and certified robustness of neural networks, plus backdoor attacks and provable defenses. | 37 | 0.43% → 0.41% | 2 |
| Neural Decoding from Brain Recordings | These papers decode speech, images and intentions from brain recordings and build brain foundation models and datasets for brain-computer interfaces. | 33 | 0.32% → 0.36% | 3 |
| Sparse Autoencoders for Interpretability | Building, evaluating and stress-testing sparse autoencoders and dictionary learning to extract interpretable features from model activations. | 33 | 0.15% → 0.36% | 1 |

Orals: [BrainWorld: A Structural-Prior-Conditioned Generative Model for Whole-Brain 4D fMRI Dynamics](https://neurips.cc/virtual/2026/poster/155412); [DD-CAM: Minimal Sufficient Explanations for Vision Models Using Delta Debugging](https://neurips.cc/virtual/2026/poster/151520); [Decomposing Earth Embeddings with Sparse Autoencoders](https://neurips.cc/virtual/2026/poster/150168); [Evaluating Neural Data Tokenizers: A Framework for Assessing Learned Representations of Spiking Activity](https://neurips.cc/virtual/2026/poster/139125); [Exact Gaussian Moment Matching for Residual Networks: a Second-Order Method](https://neurips.cc/virtual/2026/poster/155943); [Geometry-Aware Similarity Metrics for Neural Representations on Riemannian and Statistical Manifolds](https://neurips.cc/virtual/2026/poster/150840); [IDEA: Unwrapping Visual Black-box Models by Interaction Decomposition](https://neurips.cc/virtual/2026/poster/151393); [Learning interpretable Schur forms of recurrent weight matrices](https://neurips.cc/virtual/2026/poster/155071); [Learning Reveals Invisible Structure in Low-Rank RNNs](https://neurips.cc/virtual/2026/poster/152289); [Learning Sparse Semantic-Cortical Atoms for Multisubject Naturalistic fMRI Encoding](https://neurips.cc/virtual/2026/poster/151712); [MindAlign: Bridging EEG, Vision, and Language for Zero-Shot Visual Decoding](https://neurips.cc/virtual/2026/poster/149255); [Neural population tuning statistics as priors for multitask generalization](https://neurips.cc/virtual/2026/poster/153194); [The Dead Salmons of AI Interpretability: The Need for a Statistical Inference Perspective](https://neurips.cc/virtual/2026/poster/140002); [The Sign Code: The Hidden Binary Nature of Deep Networks](https://neurips.cc/virtual/2026/poster/155585); [UECO: A Unified Encoder with Structure-Aware Attention Mixture via Iterative Edge Evolving for Neural Combinatorial Optimization](https://neurips.cc/virtual/2026/poster/153347); [Uniform-in-Time Weak Propagation of Chaos in Shallow Neural Networks](https://neurips.cc/virtual/2026/poster/154794); [Unlocking Volition: Proactive Intention Decoding via Interpretable Graph Learning of Multi-Region ECoG](https://neurips.cc/virtual/2026/poster/153824)

## Efficient LLMs & Architectures — 680 papers (7.5%, 2025: 7.9%)

Transformer theory, sparse attention, KV cache, quantization, pruning, speculative decoding, PEFT, model merging, scaling laws and LLM-written GPU kernels.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Transformer Mechanisms and Expressivity Theory | These papers analyze how transformers compute, covering in-context learning theory, looped transformers, attention sinks, massive activations and length generalization. | 125 | 1.69% → 1.37% | 4 |
| LLM Pruning and MoE Compression | Structured pruning, layer removal and mixture-of-experts compression to make large language models cheaper to store and serve. | 95 | 0.97% → 1.04% | 2 |
| LoRA and Parameter-Efficient Fine-Tuning | Proposes low-rank, sparse, orthogonal and zeroth-order adapter variants and optimizers for fine-tuning large language models with less memory and compute. | 82 | 1.31% → 0.90% | 2 |
| Long-Context Sparse and Linear Attention | These papers make long-context language models efficient through sparse attention, linear RNNs and state-space models, and positional encodings that extend context length. | 77 | 0.94% → 0.85% | 3 |
| Low-Bit LLM Quantization | These papers compress LLM weights and activations to low bit-widths through post-training quantization, quantization-aware training and mixed-precision search. | 66 | 0.51% → 0.72% | 1 |
| KV Cache Compression and Eviction | These papers shrink the memory cost of LLM inference by evicting, quantizing, pruning or reusing key-value cache entries. | 53 | 0.53% → 0.58% | 1 |
| Speculative Decoding for LLM Inference | Speeds up LLM generation and serving with draft-and-verify speculative decoding, tree drafting, self-speculation and scheduling. | 47 | 0.63% → 0.52% | 2 |
| Neural Scaling Laws for Pretraining | These papers fit, explain and extrapolate power-law scaling laws that relate loss to model size, data and compute, and derive compute-optimal training recipes. | 43 | 0.61% → 0.47% | 3 |
| LLM-Generated GPU Kernels and Systems | Using LLMs and agents to write and tune CUDA or Triton kernels, plus benchmarks for HPC and ML systems code. | 40 | 0.17% → 0.44% | 1 |
| Model Merging and LoRA Fusion | Combining fine-tuned models, task vectors or LoRA adapters into a single model without retraining. | 29 | 0.26% → 0.32% | 1 |
| Diffusion Transformer Quantization and Sparsity | These papers speed up image and video diffusion transformers with post-training or quantization-aware quantization and trainable sparse attention. | 23 | 0.27% → 0.25% | 0 |

Orals: [Bridging Compute- and Data-Optimal Pretraining](https://neurips.cc/virtual/2026/poster/155350); [Compact SO(3) Equivariant Atomistic Foundation Models via Structural Pruning](https://neurips.cc/virtual/2026/poster/154865); [Felid: A Flexible and Efficient Design for Transformer Fine-Tuning over Encrypted Data](https://neurips.cc/virtual/2026/poster/148321); [Fractional State Space Transition for Long Sequence Modeling](https://neurips.cc/virtual/2026/poster/150427); [Pruning and Distilling Mixture-of-Experts into Dense Language Models](https://neurips.cc/virtual/2026/poster/150472)

## Trustworthy & Statistical ML — 611 papers (6.7%, 2025: 7.8%)

Federated learning, differential privacy, fairness, conformal prediction, calibration, causal effect estimation, noisy labels, PAC theory, clustering and tabular foundation models.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Federated Learning under Heterogeneity | These papers train models across distributed clients with non-IID data, covering aggregation, personalization, federated LoRA, robustness and privacy. | 84 | 1.31% → 0.92% | 0 |
| Model Selection and Evaluation Pitfalls | Data-centric studies of benchmarks, model selection, cascades and evaluation pitfalls in how model behavior is measured. | 76 | 0.38% → 0.83% | 3 |
| Performative Prediction and Decision-Focused Learning | These papers study predictions that feed into decisions, including performative prediction, predict-then-optimize, recalibration and learning-augmented algorithms. | 52 | 0.38% → 0.57% | 3 |
| Learning with Noisy and Weak Labels | These papers handle imperfect supervision such as label noise, partial and positive-unlabeled labels, class imbalance and active learning, along with surrogate-loss theory. | 48 | 1.11% → 0.53% | 4 |
| PAC Learning and Sample Complexity | These papers prove sample-complexity and lower bounds for PAC, online and agnostic learning, especially of halfspaces and concept classes with VC or Littlestone dimension. | 48 | 0.79% → 0.53% | 8 |
| Clustering Coresets and Nearest Neighbor Search | Algorithms and guarantees for coresets, k-means and k-center clustering, metric spaces and approximate nearest neighbor search. | 48 | 0.58% → 0.53% | 0 |
| Treatment Effect Estimation and Causal Inference | These papers estimate heterogeneous and average treatment effects and counterfactual outcomes from observational, experimental and survival data. | 45 | 0.63% → 0.49% | 1 |
| Privacy Auditing and Membership Inference | These papers design differentially private training and accounting mechanisms, and audit privacy leakage with membership inference attacks. | 39 | 0.44% → 0.43% | 0 |
| Differentially Private Estimation Rates | Algorithms and optimal rates for statistical estimation, optimization and data analysis under central or local differential privacy. | 35 | 0.58% → 0.38% | 4 |
| Conformal Prediction Coverage Guarantees | Constructs conformal prediction sets and intervals with marginal, conditional or online coverage guarantees under shift, grouping and multivariate outputs. | 35 | 0.44% → 0.38% | 1 |
| Algorithmic Fairness and Group Constraints | Fair classification and regression, multigroup fairness, fairness audits and fairness-accuracy tradeoffs under sensitive attributes. | 34 | 0.51% → 0.37% | 1 |
| Tabular Foundation Models | In-context tabular foundation models such as TabPFN plus benchmarks, robustness, privacy and generation for tabular data. | 34 | 0.36% → 0.37% | 1 |
| Calibration and Prediction-Powered Inference | Studies post-hoc calibration, multicalibration and prediction-powered inference for reliable estimates and evaluation with few labels. | 33 | 0.29% → 0.36% | 3 |

Orals: [DD-Ranking: Rethinking the Evaluation of Dataset Distillation](https://neurips.cc/virtual/2026/poster/139355); [Filtered Conformal Ellipsoids for Graph-Native Time Series](https://neurips.cc/virtual/2026/poster/155800); [Impossibility of Distribution-Free Predictive Inference for Individual Treatment Effects](https://neurips.cc/virtual/2026/poster/149451); [LLM-Enhanced Random Forests in Orthogonal Hyperbolic Subspaces for Tabular Learning](https://neurips.cc/virtual/2026/poster/154957); [MaxSketch: Robust Distinct Counting in Streams via Random Projections](https://neurips.cc/virtual/2026/poster/155987); [Mitigating Confidence Miscalibration in Open-World Semi-Supervised Learning](https://neurips.cc/virtual/2026/poster/153397); [Position: Fair Representations Cannot Hold What They Promise](https://neurips.cc/virtual/2026/poster/140022); [Scale-Sensitive Shattering: Learnability and Evaluability at Optimal Scale](https://neurips.cc/virtual/2026/poster/149340); [Surprises in Proper Positive-Only Learning](https://neurips.cc/virtual/2026/poster/148778); [Testable and Actionable Calibration for Full Swap Regret](https://neurips.cc/virtual/2026/poster/148311); [The Aleatoric-Epistemic Dichotomy of Uncertainty is Meaningful and Indispensable for Machine Learning](https://neurips.cc/virtual/2026/poster/140101); [The Stability of Online Algorithms in Performative Prediction](https://neurips.cc/virtual/2026/poster/151725)

## LLM Reasoning & Retrieval — 523 papers (5.7%, 2025: 6.1%)

Efficient chain-of-thought, agentic reasoning, formal math and verified code, LLM-driven optimization modeling, clinical reasoning and retrieval-augmented generation.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Efficient Chain-of-Thought Reasoning | Analyzing reasoning traces and reducing overthinking in large reasoning models through pruning, early stopping and search. | 137 | 2.47% → 1.50% | 6 |
| LLMs for Optimization Modeling and Algorithm Design | These papers use LLMs, often with evolutionary search, to formulate optimization models, discover algorithms and generate engineering or combinatorial code, with benchmarks for each. | 83 | 0.89% → 0.91% | 3 |
| LLM Agentic Reasoning Strategies | These papers study how language-model agents choose and combine reasoning strategies for planning, abstraction and scientific problem solving, often with new benchmarks. | 63 | 0.65% → 0.69% | 0 |
| Clinical LLMs and Medical Benchmarks | These papers evaluate and build LLM agents for clinical reasoning, EHR tasks, medical QA and report generation, along with medical benchmarks. | 62 | 0.46% → 0.68% | 0 |
| Retriever and Long-Document Benchmarks | Builds benchmarks and pipelines for retrievers, embedding models, deep search and long-document understanding with evidence grounding. | 45 | 0.22% → 0.49% | 1 |
| LLM Theorem Proving and Formal Math | Using LLMs for formal theorem proving in Lean, autoformalization, proof grading and math reasoning benchmarks. | 44 | 0.49% → 0.48% | 1 |
| Verified Code and Software Security Benchmarks | Evaluates LLMs on formally verified code generation, proof writing, vulnerability detection, reverse engineering and cybersecurity tasks. | 34 | 0.29% → 0.37% | 0 |
| GraphRAG and RL-Trained Search Agents | Retrieval-augmented generation over knowledge graphs and RL-trained search agents for multi-hop question answering. | 29 | 0.22% → 0.32% | 0 |
| RAG Faithfulness and Knowledge Conflicts | Improving faithfulness, efficiency, privacy and knowledge-conflict handling in retrieval-augmented LLM generation. | 26 | 0.38% → 0.29% | 0 |

Orals: [Escaping the Cognitive Well: Efficient Competition Math with Off-the-Shelf Models](https://neurips.cc/virtual/2026/poster/150429); [Nemotron-Cascade: Scaling Cascaded Reinforcement Learning for General-Purpose Reasoning Models](https://neurips.cc/virtual/2026/poster/155022)

## Vision-Language Models — 459 papers (5.0%, 2025: 5.8%)

Visual reasoning, image-text alignment, multimodal fusion, domain-specific benchmarks and test-time adaptation for vision-language models.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Latent and Chain-of-Thought Visual Reasoning | These papers improve and diagnose how vision-language models reason over images, including latent visual reasoning, visual chain-of-thought and grounding. | 138 | 1.55% → 1.51% | 10 |
| CLIP-Style Image-Text Alignment | These papers improve image-text alignment in CLIP-style and vision-language models for compositional understanding, long captions and image retrieval. | 85 | 0.94% → 0.93% | 5 |
| Multimodal Fusion and Missing Modalities | These papers study how multimodal models combine modalities, addressing modality imbalance, missing modalities, cross-modal alignment and synergy. | 84 | 1.26% → 0.92% | 2 |
| Domain-Specific Vision Benchmarks for VLMs | Benchmarks probing multimodal models on specialised imagery such as remote sensing, medical scans, documents, try-on and image quality. | 77 | 0.80% → 0.85% | 4 |
| Test-Time and Few-Shot VLM Adaptation | Adapting, fine-tuning, distilling and robustifying CLIP-style vision-language models and vision transformers under distribution shift. | 75 | 1.19% → 0.82% | 0 |

Orals: [Binding Multiple Modalities via Multimodal Wasserstein Barycenter](https://neurips.cc/virtual/2026/poster/149098); [Clarification as Supervision: Reinforcement Learning for Vision-Language Interfaces](https://neurips.cc/virtual/2026/poster/152087); [GeoSym127K: Scalable Symbolically-verifiable Synthesis for Multimodal Geometric Reasoning](https://neurips.cc/virtual/2026/poster/139481); [Incentivizing Medical Vision Capabilities from Large-Scale Multimodal Pre-training](https://neurips.cc/virtual/2026/poster/156128); [They Can See It but not Say It: Iterative Self Knowledge Re-expression in Visual Reasoning Relative Pose Identification](https://neurips.cc/virtual/2026/poster/151372); [Thinking with Images as Continuous Policy: Numerical Visual Chain-of-Thought](https://neurips.cc/virtual/2026/poster/150085)

## Reinforcement Learning — 419 papers (4.6%, 2025: 4.8%)

Deep, offline, multi-agent, goal-conditioned and constrained RL, generative policies and convergence theory for MDPs.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Deep RL Representations and Multitask | General deep reinforcement learning methods covering representation learning, multitask, meta, transfer, safe and model-based RL. | 80 | 1.11% → 0.88% | 3 |
| Cooperative Multi-Agent RL | These papers train teams of agents to coordinate and explore in cooperative or mixed-motive multi-agent reinforcement learning and Markov games. | 69 | 0.73% → 0.76% | 3 |
| In-Context RL and Offline Policy Steering | These papers learn and adapt policies from fixed datasets, behavior foundation models and in-context RL, including safe offline RL and post-training policy steering. | 66 | 0.55% → 0.72% | 4 |
| Policy Gradient and MDP Convergence Theory | These papers prove convergence and sample-complexity results for policy gradient, value iteration and off-policy evaluation in discounted and average-reward MDPs. | 62 | 0.79% → 0.68% | 1 |
| Generative Policies for Offline RL | Offline and offline-to-online reinforcement learning using diffusion, flow-matching and generative policies trained on fixed datasets. | 42 | 0.60% → 0.46% | 0 |
| Constrained and Robust MDPs | These papers give provable algorithms for constrained, chance-constrained and robust Markov decision processes, often via primal-dual policy optimization. | 38 | 0.38% → 0.42% | 1 |
| Goal-Conditioned RL and Task Specifications | These papers train RL agents to reach goals or satisfy formal task specifications such as temporal logic and reward machines, often offline and with subgoal planning. | 33 | 0.56% → 0.36% | 1 |
| Flow and Diffusion Policy Optimization | Trains diffusion and flow-matching policies with policy gradients, Q-guidance and offline-to-online RL for multimodal continuous control. | 29 | 0.10% → 0.32% | 3 |

Orals: [Can In-Context Learning Support Intrinsic Curiosity?](https://neurips.cc/virtual/2026/poster/151481); [CIG: Exploration via Conditional Information Gain](https://neurips.cc/virtual/2026/poster/149190); [Coordination Connectivity: Shared Initialization Shapes the Joint-Policy Landscape in MARL](https://neurips.cc/virtual/2026/poster/154512); [Emergence of Physical Intelligence via Controllable Information Production](https://neurips.cc/virtual/2026/poster/152582); [Training Generalizable Collaborative Agents via Strategic Risk Aversion](https://neurips.cc/virtual/2026/poster/151685); [Unifying Goal-Conditioned RL and Unsupervised Skill Learning via Control-Maximization](https://neurips.cc/virtual/2026/poster/153300)

## Diffusion, Flows & Inference — 417 papers (4.6%, 2025: 3.9%)

Diffusion guidance and sampling, flow matching, diffusion theory, optimal transport, and variational and simulation-based Bayesian inference.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Diffusion Guidance and Reward Fine-Tuning | Improves how diffusion and flow models are guided and sampled, including classifier-free guidance, reward-guided and RL post-training, few-step generation and score-matching analysis. | 132 | 1.23% → 1.45% | 6 |
| Flow Matching Theory and Variants | New formulations, theory and constrained or distilled variants of flow matching and transport-based generative models. | 80 | 0.51% → 0.88% | 5 |
| MCMC, SMC and Posterior Samplers | These papers design and analyze samplers built on diffusion models, Langevin dynamics and sequential Monte Carlo, including posterior sampling for inverse problems. | 71 | 0.75% → 0.78% | 1 |
| Variational and Simulation-Based Bayesian Inference | Develops variational inference, neural posterior estimation, Gaussian process and Laplace methods for scalable and robust Bayesian inference. | 60 | 0.85% → 0.66% | 5 |
| Statistical Theory of Diffusion Models | Theoretical and statistical work on score-based diffusion models, density estimation, denoising and posterior inference for inverse problems. | 41 | 0.29% → 0.45% | 3 |
| Optimal Transport Algorithms and Theory | These papers propose solvers and estimation theory for optimal transport, including Gromov-Wasserstein, sliced, unbalanced and barycenter problems. | 33 | 0.31% → 0.36% | 1 |

Orals: [Free Decompression with Algebraic Spectral Curves](https://neurips.cc/virtual/2026/poster/155558); [Generative Modeling via Drifting](https://neurips.cc/virtual/2026/poster/154240); [ParetoSlider: Diffusion Models Post-Training for Continuous Reward Control](https://neurips.cc/virtual/2026/poster/154172); [Query Lower Bounds for Diffusion Sampling](https://neurips.cc/virtual/2026/poster/151581); [Representation Fréchet Loss for Visual Generation](https://neurips.cc/virtual/2026/poster/154990); [Shaping Useful Noise: Energy Distributions Predict Visual Pretraining Quality](https://neurips.cc/virtual/2026/poster/153569); [Strong Stochastic Flow Maps](https://neurips.cc/virtual/2026/poster/149475); [Tessellations of Semi-Discrete Flow Matching](https://neurips.cc/virtual/2026/poster/153677)

## Robotics & Embodied AI — 405 papers (4.4%, 2025: 3.7%)

Vision-language-action policies, dexterous and humanoid manipulation, autonomous driving, world models for planning and embodied spatial reasoning.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Vision-Language-Action Robot Policies | Training, fine-tuning, analysing and evaluating vision-language-action models for robotic manipulation. | 94 | 0.60% → 1.03% | 3 |
| Dexterous and Humanoid Robot Manipulation | These papers learn dexterous hand-object interaction, humanoid loco-manipulation and contact-rich control, often from egocentric human videos and tactile or force signals. | 76 | 0.92% → 0.83% | 4 |
| End-to-End Autonomous Driving | End-to-end driving planners, driving VLA models, world models and benchmarks for autonomous vehicles. | 64 | 0.56% → 0.70% | 0 |
| Embodied Spatial Reasoning in VLMs | Benchmarks and agentic methods for 3D and embodied spatial reasoning in vision-language models. | 60 | 0.70% → 0.66% | 3 |
| Latent World Models for Planning | Latent and symbolic world models that let robots and LLM agents predict outcomes and plan actions. | 58 | 0.53% → 0.64% | 0 |
| Action-Conditioned Video World Models | These papers build interactive, action-conditioned video world models for robots, games and embodied agents, sometimes combined with vision-language-action policies. | 53 | 0.39% → 0.58% | 4 |

Orals: [HABIT: Human-Aware Behavior and Interaction Training Dataset for Robot Manipulation](https://neurips.cc/virtual/2026/poster/139828); [Language-Conditioned World Modeling for Visual Navigation](https://neurips.cc/virtual/2026/poster/154464); [SyncWorld: Visual Calibration Enables World Models as Zero-Shot Simulators](https://neurips.cc/virtual/2026/poster/149981)

## Image & 3D Generation — 375 papers (4.1%, 2025: 5.6%)

Text-to-image generation and evaluation, efficient high-resolution diffusion, image editing, unified multimodal models, part-level 3D assets and concept erasure.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Efficient High-Resolution Image Diffusion | These papers make image diffusion models faster and higher-resolution through feature caching, few-step distillation, pixel-space diffusion and diffusion-based super-resolution. | 90 | 1.33% → 0.99% | 6 |
| Text-to-Image Generation and Evaluation | Improving and evaluating text-to-image models via reward models, compositional control, aesthetics and bias analysis. | 76 | 0.84% → 0.83% | 2 |
| Part-Level 3D Asset Generation | Generating structured, part-decomposed or articulated 3D objects and scenes from images or text. | 64 | 1.11% → 0.70% | 1 |
| Unified Multimodal Understanding and Generation | Builds single models and visual tokenizers that both understand and generate images, including autoregressive and representation-autoencoder approaches. | 61 | 1.02% → 0.67% | 3 |
| Instruction-Based Image Editing | Builds datasets, guidance schemes and RL training for editing images from text instructions, exemplars or drag inputs while preserving unedited content. | 50 | 0.53% → 0.55% | 2 |
| Concept Erasure in Text-to-Image Diffusion | Removing unsafe concepts or styles from text-to-image diffusion models, plus adversarial attacks and defenses on vision-language models. | 34 | 0.79% → 0.37% | 1 |

Orals: [Can We Model the Artifacts Explicitly? Disentangle Artifacts via Pairwise Edit Relations for Image Manipulation Localization](https://neurips.cc/virtual/2026/poster/155638); [EntiRE: Invariant Learning for Robust Concept Erasure in Text-to-Image Generative Models](https://neurips.cc/virtual/2026/poster/151144)

## Video Generation & Understanding — 370 papers (4.1%, 2025: 4.0%)

Long and controllable video generation, physical plausibility, long-video QA, temporal grounding and human motion generation.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Long-Video Understanding with MLLMs | These papers help multimodal LLMs answer questions over long and streaming videos via frame selection, token allocation, KV-cache memory and agentic pipelines. | 88 | 1.21% → 0.97% | 1 |
| Autoregressive Long Video Generation | These papers extend video diffusion models to long or streaming generation with autoregressive rollout, memory for consistency, and distillation for real-time speed. | 68 | 0.55% → 0.75% | 1 |
| Video Temporal Grounding and Segmentation | These papers localize actions, moments and objects in time and space in video, covering temporal grounding, video object segmentation and video reasoning segmentation. | 65 | 0.73% → 0.71% | 1 |
| Physical Plausibility in Video Generation | Evaluating and improving physical consistency, motion realism and world modeling in text-to-video generators. | 54 | 0.43% → 0.59% | 3 |
| Controllable Video Generation and Editing | These papers generate and edit videos with control over subjects, motion, identity and lighting, often by turning image editors into video editors. | 52 | 0.48% → 0.57% | 0 |
| Human Motion and Gesture Generation | Generating, predicting and recognizing human motion, dance, gestures, gait and sign from text, scenes or video. | 43 | 0.60% → 0.47% | 1 |

Orals: [Behavioral Geometric Supervision Aligns Video Foundation Models with Human Social Perception](https://neurips.cc/virtual/2026/poster/149277)

## Biomolecules & Causal Discovery — 345 papers (3.8%, 2025: 3.5%)

Single-cell, protein, molecule and chemistry models alongside causal discovery and structural causal models.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Single-Cell and Spatial Transcriptomics Models | Builds foundation models and generative methods for single-cell gene expression, spatial transcriptomics from histology, perturbation response and genomic sequences. | 63 | 0.39% → 0.69% | 0 |
| Protein Language Models and Structure | Protein language models, structure prediction, docking and fitness prediction for biomolecules and drug discovery. | 62 | 0.63% → 0.68% | 6 |
| Chemical Reactions and Interatomic Potentials | These papers build models and benchmarks for chemistry tasks such as reaction prediction, retrosynthesis, mass-spectrometry retrieval and machine-learned interatomic potentials. | 57 | 0.70% → 0.63% | 2 |
| 3D Molecule and Material Generation | These papers generate 3D molecules, crystals, proteins and materials with equivariant diffusion, flow and autoregressive models, including structure-based drug design. | 53 | 0.65% → 0.58% | 2 |
| Causal Identifiability and Latent-Variable Models | Learning causal graphs and identifying causal effects with structural causal models, interventions and latent variables. | 51 | 0.41% → 0.56% | 2 |
| Protein, Antibody and RNA Design | Generative models and optimization for designing proteins, antibodies, peptides, RNA and DNA sequences. | 37 | 0.34% → 0.41% | 1 |
| Amortized and LLM-Informed Causal Discovery | Recovers causal graphs from observational, interventional or time-series data, including amortized foundation models and LLM-informed priors. | 22 | 0.34% → 0.24% | 1 |

Orals: [C3P: Contrastive promoter-protein pretraining yields representations capturing bacterial gene regulation](https://neurips.cc/virtual/2026/poster/156046); [CausalBind: Causal Modeling and Learning for Protein-Molecule Virtual Screening](https://neurips.cc/virtual/2026/poster/151296)

## LLM Post-Training — 335 papers (3.7%, 2025: 3.1%)

RL with verifiable rewards, preference optimization, reward models, on-policy distillation and continual learning for language models.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Off-Policy Stability in LLM RL | Off-policy corrections, importance ratios, entropy control and credit assignment for stable reinforcement learning post-training of LLMs. | 87 | 0.67% → 0.95% | 1 |
| GRPO-Style RL with Verifiable Rewards | Studies reinforcement learning with verifiable rewards for reasoning models, focusing on GRPO-style advantage estimation, rollout efficiency and training stability. | 65 | 0.32% → 0.71% | 1 |
| Preference Optimization for LLM Alignment | DPO-style and RLHF objectives, data selection and robustness methods for aligning LLMs with human preferences. | 52 | 0.97% → 0.57% | 1 |
| Class-Incremental Continual Learning | These papers learn new classes or tasks one after another without forgetting old ones, often with LoRA adapters, merging or optimizers built for stability and plasticity. | 50 | 0.75% → 0.55% | 2 |
| On-Policy Distillation for LLM Reasoning | Teacher-student distillation where reasoning LLMs learn from teacher feedback on their own generated trajectories. | 49 | 0.29% → 0.54% | 3 |
| Reward Models and Human Behavior Modeling | These papers mix reward and process-reward modeling for LLMs, including reward hacking, with computational models of human and animal decision-making behavior. | 32 | 0.12% → 0.35% | 2 |

Orals: [The Algorithm Is Not the Behavior: Learned Priors Override Look-Ahead in a Chess-Playing Neural Network](https://neurips.cc/virtual/2026/poster/152268)

## Optimization & Statistics — 280 papers (3.1%, 2025: 3.5%)

Optimizer design such as Muon and Adam, stochastic and convex convergence theory, robust regression and Bayesian optimization.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Muon, Adam and Sign-Based Optimizers | These papers analyse and design neural-network optimizers such as Muon, Adam, Lion and SignSGD, covering orthogonalized updates, momentum and edge-of-stability dynamics. | 88 | 0.92% → 0.97% | 6 |
| Stochastic and Convex Optimization Theory | Convergence rates for stochastic, decentralized, minimax and nonconvex gradient methods, including heavy-tailed noise and step-size schedules. | 85 | 1.08% → 0.93% | 1 |
| Robust Regression and Statistical Inference | Statistical theory for linear regression, covariance estimation and inference under heavy tails, corruption and high dimensions. | 70 | 1.01% → 0.77% | 2 |
| Bayesian and Multi-Objective Optimization | Sample-efficient black-box optimization with Gaussian process surrogates, acquisition functions and multi-objective Pareto search. | 37 | 0.46% → 0.41% | 0 |

## Bandits, Games & Mechanisms — 234 papers (2.6%, 2025: 3.0%)

Bandit regret and best-arm identification, online convex optimization, equilibrium learning in games, and mechanism design and social choice.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Mechanism Design, Auctions and Social Choice | Designs and analyzes auctions, pricing, resource allocation, persuasion and voting rules for strategic agents, often with learning-augmented guarantees. | 72 | 0.90% → 0.79% | 5 |
| Regret Bounds for Stochastic and Contextual Bandits | Regret bounds and algorithms for stochastic, linear, contextual, dueling and cascading bandit problems. | 64 | 1.08% → 0.70% | 1 |
| Learning Equilibria in Games | Learning dynamics and sample complexity for reaching Nash or correlated equilibria in zero-sum, Markov and potential games. | 44 | 0.53% → 0.48% | 1 |
| Online Convex Optimization Regret Bounds | Derives regret guarantees for online convex and non-convex optimization under delays, switching costs, memory and bandit feedback. | 31 | 0.32% → 0.34% | 1 |
| Best-Arm Identification in Bandits | Gives sample-complexity bounds and algorithms for fixed-confidence and fixed-budget best-arm identification and pure exploration in bandits. | 23 | 0.12% → 0.25% | 1 |

Orals: [Follow the Regularized Leader Does Not Converge in Constrained Optimization](https://neurips.cc/virtual/2026/poster/150986); [The Power of a Random Sample in Online Algorithms](https://neurips.cc/virtual/2026/poster/152757)

## Time Series & Forecasting — 219 papers (2.4%, 2025: 2.2%)

Time series forecasting models, irregular and continuous-time sequences, weather and climate prediction, and urban mobility.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Time Series Forecasting Models | Forecasting architectures and time series foundation models for multivariate, long-horizon and non-stationary data. | 82 | 0.97% → 0.90% | 7 |
| Irregular and Continuous-Time Sequences | Models irregularly sampled and continuous-time sequences with neural CDEs, state-space models and point processes, often for EHR, ECG, sleep and wearable data. | 61 | 0.41% → 0.67% | 0 |
| Weather, Climate and Air Quality Forecasting | These papers forecast weather, air quality, cyclones and other environmental and energy quantities with ML models and new benchmarks. | 42 | 0.44% → 0.46% | 2 |
| Urban Mobility and Trajectory Generation | Generates and forecasts vehicle and human trajectories, traffic and spatio-temporal events in cities, including cross-city transfer and benchmarks. | 34 | 0.38% → 0.37% | 2 |

Orals: [MOVEBENCH: A Benchmark for Global-Scale Wildlife Movement Forecasting](https://neurips.cc/virtual/2026/poster/139749); [Spectral Energy Allocation Enables Source-Free Domain Adaptation in Time Series Forecasting](https://neurips.cc/virtual/2026/poster/154914); [TiRex-2: Generalizing TiRex to Multivariate Data and Streaming](https://neurips.cc/virtual/2026/poster/151700)

## PDEs & Dynamical Systems — 173 papers (1.9%, 2025: 1.5%)

Neural operators, physics-informed networks and data-driven identification of dynamical systems.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Neural Operator Surrogates for PDEs | Neural operator and transformer surrogates that learn to solve partial differential equations for physical simulation and forecasting. | 70 | 0.44% → 0.77% | 2 |
| Learning Dynamical Systems from Data | Identifies latent and chaotic dynamical systems from observations using Koopman operators, neural ODEs/SDEs, switching models and equation discovery. | 56 | 0.41% → 0.61% | 2 |
| Physics-Informed Networks and PDE Foundation Models | These papers solve partial differential equations with physics-informed networks, neural surrogates, PDE foundation models and generative inverse solvers. | 47 | 0.67% → 0.52% | 2 |

Orals: [Breakeven complexity: A new perspective on neural partial differential equation solvers](https://neurips.cc/virtual/2026/poster/148644); [DIAGNO: Diagonal Spherical Neural Operators for Heterogeneous Earth Dynamics Modeling](https://neurips.cc/virtual/2026/poster/154008); [Mechanism-Aware Ensemble Conditioning for Data-Limited Emulation of Extreme Events](https://neurips.cc/virtual/2026/poster/151389)

## Graph Learning — 150 papers (1.6%, 2025: 2.6%)

Graph neural network architectures, graph foundation models and generative models for graphs and hypergraphs.

| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |
|---|---|---|---|---|
| Graph Neural Networks and Foundation Models | GNN architectures, graph contrastive learning, temporal graphs and graph foundation models for node, link and graph tasks. | 130 | 2.49% → 1.43% | 4 |
| Graph and Hypergraph Generation | These papers propose diffusion, flow-matching, autoencoder and sequence models that generate graphs and hypergraphs at scale. | 20 | 0.09% → 0.22% | 0 |
