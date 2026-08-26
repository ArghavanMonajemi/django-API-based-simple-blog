{% extends "mail_templated/base.tpl" %}

{% block subject %}
user activation
{% endblock %}

{% block html %}
please click on this <a href="http://127.0.0.1:8000/account/api/v1/activation/{{token}}">link</a> to activate your account.
{% endblock %}