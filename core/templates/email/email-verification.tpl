{% extends "email/base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
This is a verification email.
{% endblock %}

{% block html %}
Please click <a href="${{secrets.SITE}}accounts/verify-email/{{token}}/" >here</a> to verify you accounts.
{% endblock %}