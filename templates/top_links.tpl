<ul class="left">
    {% for key, value in links.items() %}
        <li><a href="{{ value }}" target="new">{{ key }}</a></li>
    {% endfor %}
</ul>