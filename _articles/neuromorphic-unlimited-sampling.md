---
layout: distill
title: "Neuromorphic Unlimited Sampling"
description: "Acquiring high-dynamic range signals with minimal oversampling."
date: 2024-04-18
last_updated: 2025-07-12
post_author: Abijith J. Kamath
authors:
  - name: Abijith J. Kamath
    url: "https://kamath-abhijith.github.io"
    affiliations:
      name: Indian Institute of Science
paper_url: https://ieeexplore.ieee.org/document/10447840
doi: 10.1109/ICASSP48485.2024.10447840
bibliography: 2024-04-18-nus.bib
thumbnail: assets/img/research-highlights/nus/nus-cover.jpeg
pretty_table: true

# Math Configuration (optional - defaults from _data/typography.yml)
# math_engine: mathjax    # Options: "mathjax", "katex", or false to disable
# math_font: mathjax-modern  # MathJax fonts: mathjax-modern, mathjax-stix2, mathjax-termes, mathjax-gyre, mathjax-fira
                            # KaTeX fonts: katex-main

toc: true
related_posts: true
---

{% include figure.liquid path="assets/img/research-highlights/nus/nus-banner.jpeg" alt="Neuromorphic Unlimited Sampling banner showing high-dynamic range signal acquisition" class="img-fluid rounded" width="auto" max-width="100%" %}

Unlimited sampling (US) is a computational sensing paradigm for high-dynamic range (HDR) acquisition of signals. The objective is to overcome the limitations in standard analog-to-digital converters (ADCs) where the dynamic range is fixed: signal that lies outside the fixed dynamic range saturates.
{: .text-justify}

Unlimited sampling is an important problem in addressing signal representation in practical systems and has applications in almost all imaging systems. We propose a new technique for unlimited sampling using a neuromorphic encoder. Our system is power efficient, simple to implement in practice, and most importantly, does not require oversampling.
{: .text-justify}

## Computational Modulo Sampling

Computational modulo sampling is a framework for unlimted sampling that uses a self-reset ADC (SR-ADC) as opposed to a standard ADC, where a continuous-time signal $$f(t)$$ is first folded using the continuous-domain modulo operator before acquisition. The idea of computational unlimited sampling was first proposed by [Dr Ayush Bhandari](http://alumni.media.mit.edu/~ayush/usf.html), currently at Imperial College London. The continuous-time modulo operator with parameter $$\lambda$$ is defined as
{: .text-justify}

<div style="text-align: center;">
$f\mapsto \mathcal{M}_{\lambda}\{f\} = 2\lambda\left[\frac{f}{2\lambda}+\frac{1}{2}\right]-\lambda,$
<br><br>
</div>

where $$[\cdot]$$ defines the fractional part of the argument. The modulo operator restricts the dynamic range to the interval $$[-\lambda,+\lambda]$$ and enables acquisition of high-dynamic range (in principle, unlimited) acquisition.
{: .text-justify}

{% include figure.liquid path="assets/img/research-highlights/nus/mod-encoder.png" class="img-fluid rounded" caption="Fig. 1: What happens in a computational unlimited sampling setup." %}

Reconstruction of the high-dynamic range signal from samples of $$\mathcal{M}_{\lambda}\{f\}$$ requires oversampling as compared to the Nyquist rate of $$f$$. Further, for practical deployment of unlimited sampling, specialised hardware is required. This can indeed be a practical bottleneck! Oversampling is expensive, and adds to the cost of replacing the existing standard ADC with a self-reset ADC. Our solution addresses this problem and is as simple as using a nonlinear filter before acquisition!
{: .text-justify}

## The **Neuromorphic Unlimited Sampling** Framework

At the heart of our solution is the neuromorphic encoder, which is a bio-inspired acquisition device that has been successfully deployed in making efficient video acquisition systems. For more on neuromorphic video acquisition, check out the work from the [Robotics and Perception Group](https://rpg.ifi.uzh.ch/index.html).
{: .text-justify}

Neuromorphic encoders are opportunistic devices that record signals as a stream of events that denote a change in the input by a constant. The signal is represented as a sequence of 2-tuples, each constituting the time instant and the polarity of change.
{: .text-justify}

{% include figure.liquid path="assets/img/research-highlights/nus/nus-encoder.jpeg" class="img-fluid rounded" caption="Fig. 2: Schematic of a neuromorphic encoder. The output is a sequence of 2-tuples characterising the time instant and polarity of change in the absolute-value of the signal by the dynamic-range of the ADC." %}

Neuromorphic encoders are of practical interest as they do not record any measurements when there is no significant change in the signal. The key observation for unlimited sampling is that the difference signal $$v(t)$$ is a folded version of the input signal $$f(t)$$, and is completely accommodated in the range $$[-\lambda, +\lambda]$$. In essence, the signal $$v(t)$$ is a polarity dependent modulo operator acting on the input signal as
{: .text-justify}

<div style="text-align: center;">
$f\mapsto v = \mathcal{F}_\lambda\{f\}.$
<br><br>
</div>

The in-built folding in the neuromorphic encoder along with its opportunistic nature makes it a perfect fit for unlimited sampling. 

{% include figure.liquid path="assets/img/research-highlights/nus/nus-schematic.jpeg" class="img-fluid rounded" caption="Fig. 3: Unlimited sampling using a neuromorphic encoder: The accompanying ADC operates at the Nyquist rate and at full precision. The error incurred due to folding is tracked using the neuromorphic encoder allowing real-time reconstruction." %}

Similar to modulo sampling, the error signal $$f(t)-v(t)$$ is a piecewise constant signal with amplitude quantised to multiples of $$\lambda$$. In computational modulo sampling, the error signal is estimated from _oversampled_ measurements of the folded signal using the repeated finite-difference algorithm. In neuromorphic unlimited sampling, the error signal is captured succinctly using the output of the neuromorphic encoder as
{: .text-justify}

<div style="text-align: center;">
$\eta_f(t) = \sum_m \lambda\mathcal{S}\{p_m\} 1_{[t_m,t_{m+1}]}(t),$
<br><br>
</div>


where $$\mathcal{S}$$ denotes the cumulative summation operator. Therefore, no oversampling is required! Uniform samples of the folded signal $$v$$ captures the high-dynamic-range information in the input signal, achieving unlimited sampling!
{: .text-justify}

Additional measurements are made using the neuromorphic encoder opportunistically, i.e., only when the signal goes beyond the dynamic range while consuming much less power than the ADC. We also show that the maximal rate of additional measurements that may be obtained decays with the dynamic range. Our perfect reconstruction strategy only requires addition of a residual signal constructed using the compressed representation of the error signal, which can be achieved in real time.
{: .text-justify}

{% include figure.liquid path="assets/img/research-highlights/nus/nus-demo.png" class="img-fluid rounded" caption="Fig. 4: Demonstration of neuromorphic sampling and perfect reconstruction." %}

Our patented unlimited sampling hardware using simple and cost-effective components in-house <d-cite key="kulur2024neuromorphic"></d-cite>. The neuromorphic unlimited sampling scheme is such that the neuromorphic encoder can be plugged into an existing acquisition system to achieve unlimited sampling, akin to a prefilter typically used in sampling, and does not require specialised hardware such as the self-reset ADC. In hardware, we demonstrate HDR acquisition and real-time reconstruction of synthetic signals. We show that neuromorphic unlimited sampling operates at the Nyquist rate of the signal, while opportunistically recording compressed measurements. Our demonstration was presented at the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) 2024, in Seoul Korea 2024, in the Show-and-tell Demos <d-cite key="kulur2024modulo"></d-cite>. A detailed theoretical exposition is available in our paper <d-cite key="kamath2024neuromorphic"></d-cite> which was also presented at IEEE ICASSP 2024. The extension of this theory to a larger class of signals including video signals is going to be presented at the IEEE ICASSP 2025 <d-cite key="kamath2025neuromorphic"></d-cite>.
{: .text-justify}

<!-- Video file not available -->
<!-- {% include video.liquid path="assets/video/nus-demo.mp4" class="img-fluid rounded z-depth-1" controls=true%} -->
<!-- <div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-5 mt-md-0">
        <div style="text-align: center;">
            {% include video.liquid path="https://www.youtube.com/embed/JdMvjfvdW38?si=g4B4d4JFXwwqvTs2" class="img-fluid rounded z-depth-1" controls=true width="100%"%}
        </div>
    </div>
</div> -->
<!-- <div class="caption">
    Watch our demo on YouTube!
</div> -->

The hardware contributions to this project are in collaboration with Shreyas, Shreyansh, Satyapreet and Dr Thakur at [NeuRonICS, Department of Electronic Systems Engineering](https://labs.dese.iisc.ac.in/neuronics/), IISc. Bengaluru.
{: .text-justify}