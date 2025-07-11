---
layout: page
permalink: /contactus/
title: contact
description:
nav: true
nav_order: 100
---

#### Campus Location

{{ site.data.contacts.lab_location.name }} is located in the {{ site.data.contacts.lab_location.department }} at the {{ site.data.contacts.lab_location.institution }}, {{ site.data.contacts.lab_location.city }}. Further information can be found [here]({{ site.data.contacts.lab_location.info_url }}), including campus maps and visitor information.

<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15548.853114231753!2d77.57168639507697!3d13.022086010938535!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae17101343e6af%3A0x80f1fdae32150d6a!2sSpectrum%20Lab!5e0!3m2!1sen!2sin!4v1752223407315!5m2!1sen!2sin" title="Indian Institute of Science Campus Map" width="100%" height="512" allowfullscreen="true" frameborder="0" scrolling="no"></iframe>


<!-- <iframe id="iiscmaps" src="" -->


#### Potential Collaborators/Industry Partners

Please reach out by e-mail directly.

#### Administrative Assistant

**{{ site.data.contacts.administrative_assistant.name }}**<br/>
Email: [{{ site.data.contacts.administrative_assistant.email }}](mailto:{{ site.data.contacts.administrative_assistant.email }})<br/>
Phone: {{ site.data.contacts.administrative_assistant.phone }}

#### Mailing Address

{{ site.data.contacts.mailing_address.line1 }}<br/>
{{ site.data.contacts.mailing_address.line2 }}<br/>
{{ site.data.contacts.mailing_address.line3 }}<br/>
{{ site.data.contacts.mailing_address.line4 }}

<div class="social">
    <div class="contact-icons">
    {% include social.liquid %}
    </div>
</div>
