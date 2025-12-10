---
layout: distill
title: "Neuromorphic Unlimited Sampling"
description: "Unlimited sampling via neuromorphic event-driven cameras."
date: 2025-07-12
last_updated: 2025-07-12
post_author: Abijith J. Kamath
authors:
  - name: Abijith J. Kamath
    url: "https://kamathabijithj.github.io"
    affiliations:
      name: Indian Institute of Science
paper_url: https://ieeexplore.ieee.org/document/10888893
doi: 10.1109/ICASSP49660.2025.10888893
bibliography: 2024-04-18-nus.bib
thumbnail: assets/img/research-highlights/nus/nus-banner.jpeg

toc: true
related_posts: false
---

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0 blog-ready">
        {% include figure.liquid path="assets/img/research-highlights/nus/nus-banner.jpeg" %}
    </div>
</div>

## Abstract

The unlimited sampling framework enables the reconstruction of bandlimited signals from measurements obtained using a self-resetting analog-to-digital converter (ADC). This ADC, called the modulo ADC, folds the signal modulo a threshold ($\lambda$) before sampling, thus addressing the issue of ADC saturation. On the other hand, event-driven cameras capture the temporal changes in the intensity of each pixel, and have been shown to reach a high dynamic range, thus providing an attractive solution to deal with saturation. In this paper, we explore a connection between neuromorphic sensing and unlimited sampling by showing that a variant of the integrate-and-fire model is equivalent to modulo sampling. This connection allows us to use well-established reconstruction algorithms for modulo sampling to recover signals from event camera measurements. We present the connection via simulated data.
{: .text-justify}

## Introduction

Analog-to-digital converters (ADCs) are ubiquitous in various signal processing systems, including imaging, audio, and communication systems. Since ADCs have a limited range, signals must be appropriately attenuated before digitization to avoid saturation. For example, in digital cameras, automatic gain control is typically applied to avoid saturation. For high-dynamic-range (HDR) imaging applications, this practice is undesirable because attenuating a signal causes a loss of information for all pixel locations, particularly in the darker parts of the scene, even if only a handful of pixels experience saturation. The unlimited sampling framework, first introduced in<d-cite key="bhandari2017unlimited"></d-cite>, addresses this issue by digitizing a folded version of the input signal and reconstructing the original signal from the folded samples.
{: .text-justify}

In image processing, the conventional way of dealing with saturation is via high-dynamic-range (HDR) imaging. In exposure bracketing, the standard approach to HDR imaging, the same scene is captured using multiple exposures, and a composite image is constructed from these images. Recently, event-driven cameras have emerged as an alternative to conventional cameras. Event cameras are bio-inspired sensors where each pixel triggers an event asynchronously whenever the change in the log intensity of that particular pixel crosses a threshold.
{: .text-justify}

Event cameras naturally exhibit high dynamic range (HDR), with each pixel independently sensing the scene's brightness changes, and they can do so at a high rate. The event threshold of an event camera is the smallest change in log intensity needed to trigger an event. The event threshold determines the accuracy and sensitivity of an event camera to small changes in intensity.
{: .text-justify}

## Modulo ADC and Unlimited Sampling

The modulo ADC is an architecture that enables an ADC to measure arbitrarily large voltages. Before quantization, a modulo ADC folds voltages outside the dynamic range $[-\lambda, \lambda]$ into the dynamic range. The folding, which is a non-linear operation, is described using the modulo operator (see figure):
{: .text-justify}

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0 blog-ready">
        {% include figure.liquid path="assets/img/research-highlights/nus/mod-encoder.png" %}
    </div>
</div>

$$
y(t) = \mathcal{M}_{\lambda}(f(t)) \triangleq \left(f(t) + \lambda \right) \mod 2\lambda - \lambda.
$$

The output of a modulo ADC for a bandlimited signal $f$ is a uniformly sampled version of $y(t)$. The unlimited sensing framework is concerned with the recovery of $f$ from samples of $y$. The reconstruction was shown to be possible under certain conditions on the sampling frequency and ADC threshold<d-cite key="bhandari2017unlimited"></d-cite>.
{: .text-justify}

## Neuromorphic Sensing via an Integrate-and-Fire Model

Neuromorphic sensors are characterized by their response to changes in intensity, as opposed to the response to intensity itself. The event-driven camera is one such neuromorphic sensor. An ideal event camera fires an event whenever the intensity crosses a fixed threshold. The integrate-and-fire model captures this behavior<d-cite key="lichtsteiner2008128"></d-cite>.
{: .text-justify}

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0 blog-ready">
        {% include figure.liquid path="assets/img/research-highlights/nus/nus-encoder.jpeg" %}
    </div>
</div>

The integrate-and-fire model is characterized by two operations: an integration of intensity from one event until the next, and a firing of an event and subsequent reset whenever the integral equals a threshold. Mathematically, this can be described as follows:
{: .text-justify}

An event is fired whenever the integral crosses a threshold:

$$\int_{t_{k-1}}^{t_{k}} f(s) \, ds = \kappa p_k,$$

where $t_{k-1}$ and $t_k$ are the timestamps of the $(k-1)$-th and $k$-th events respectively, $\kappa$ is the event threshold, and $p_k$ is the event polarity at time $t_k$.

## Neuromorphic Sensing Meets Unlimited Sampling

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0 blog-ready">
        {% include figure.liquid path="assets/img/research-highlights/nus/nus-schematic.jpeg" %}
    </div>
</div>

We establish a connection between the integrate-and-fire model and modulo sampling by considering a small modification to the measurement model described above. 
{: .text-justify}

In this modified model, we assume the input signal to be a bandlimited function. The polarity information and the time stamps of the integrate-and-fire model are first used to generate a piecewise-constant (PC) signal. The PC signal at any time $t$ is essentially the cumulative polarity up to time $t$, multiplied by the threshold $\kappa$. Thus, at any time $t$, the PC signal has a value in $\kappa \mathbb{Z}$. By definition, the value of the PC signal is constant in the interval $(t_k, t_{k+1})$ and is updated at each spike time $t_k$. 
{: .text-justify}

We call the resulting function the folded function, denoted by $g$ (see figure):

$$ g(t) = f(t) - r(t), $$

where $f$ is the input bandlimited signal and $r(t)$ is the cumulative polarity, which we call the residual function. After the sampling, using a standard uniform sampler, we get a set of samples of $g$.
{: .text-justify}

Given the samples of the folded function and the threshold $\kappa$, the problem of recovering the input is related to that of unlimited sampling. This is because the residual signal is a piecewise-constant signal and also takes values in $\kappa \mathbb{Z}$. A reconstruction is then possible using the algorithmic framework of the unlimited sampling methodology.
{: .text-justify}

## Neuromorphic Sensing Unlimited Sampling: Results

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0 blog-ready">
        {% include video.liquid path="https://www.youtube.com/embed/fU-qpYIWvjg?si=Aq0KgAu1DRZh3oPD" class="img-fluid rounded z-depth-1" autoplay="true" controls="true" %}
    </div>
</div>

<br>

In the video above, we show a toy example demonstrating the validity of the proposed equivalence. To this end, a bandlimited signal is passed through the integrate-and-fire model, and the resulting events are used to construct the folded signal. The folded signal is uniformly sampled, and the samples are used to recover the original signal using an unlimited sampling algorithm. The reconstruction quality is the same as that for samples of a modulo ADC. The video shows the reconstruction for different values of the event threshold $\kappa$.
{: .text-justify}
