---
layout: page
permalink: /publications/
title: Publications
description:
years: [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009]
nav: true
nav_order: 3
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<!-- Year Pagination -->
<div class="year-pagination">
  <button id="prev-year" class="btn btn-outline-primary btn-sm">Previous Year</button>
  <span id="current-year-display" class="mx-2">2025</span>
  <button id="next-year" class="btn btn-outline-primary btn-sm">Next Year</button>
</div>

<div class="publications">

{% bibliography %}

</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const years = {{ page.years | jsonify }};
  let currentIndex = 0;

  const prevButton = document.getElementById('prev-year');
  const nextButton = document.getElementById('next-year');
  const display = document.getElementById('current-year-display');

  function updateButtons() {
    prevButton.disabled = currentIndex === years.length - 1;
    nextButton.disabled = currentIndex === 0;
  }

  function showYear(index) {
    const currentYear = years[index];
    const publicationsDiv = document.querySelector('.publications');

    // Hide all children
    Array.from(publicationsDiv.children).forEach(child => {
      child.style.display = 'none';
    });

    // Find and show the h2 and its following elements until next h2
    const children = Array.from(publicationsDiv.children);
    let showing = false;
    for (let i = 0; i < children.length; i++) {
      const child = children[i];
      if (child.tagName === 'H2' && child.textContent.trim() === currentYear.toString()) {
        showing = true;
        child.style.display = 'block';
      } else if (child.tagName === 'H2') {
        showing = false;
      } else if (showing) {
        child.style.display = 'block';
      }
    }

    display.textContent = currentYear;
    updateButtons();
  }

  prevButton.addEventListener('click', function() {
    if (currentIndex < years.length - 1) {
      currentIndex++;
      showYear(currentIndex);
    }
  });

  nextButton.addEventListener('click', function() {
    if (currentIndex > 0) {
      currentIndex--;
      showYear(currentIndex);
    }
  });

  // Initially show the first year
  showYear(currentIndex);
});
</script>
