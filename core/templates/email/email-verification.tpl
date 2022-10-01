{% extends "email/base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
This is a verification email.
{% endblock %}

{% block html %}
Please click <a href="http://127.0.0.1:8000/accounts/verify-email/{{token}}/" >here</a> to verify you accounts.
{% endblock %}