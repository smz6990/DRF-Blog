{% extends "email/base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
This is a reset password email.
{% endblock %}

{% block html %}
Please click <a href="${{secrets.SITE}}accounts/api/v1/reset/{{token}}/" >here</a> to redirect to reset password page.
{% endblock %}