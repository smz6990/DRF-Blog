{% extends "email/base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
This is a reset password email.
{% endblock %}

{% block html %}
Please click <a href="http://127.0.0.1:8000/accounts/password-reset-done/{{token}}/" >here</a> to redirect to reset password page.
{% endblock %}