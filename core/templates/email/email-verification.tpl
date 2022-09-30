{% extends "base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
This is a verification email for you.
{% endblock %}

{% block html %}
Please click <a href="">here</a> to verify you accounts.
{% endblock %}