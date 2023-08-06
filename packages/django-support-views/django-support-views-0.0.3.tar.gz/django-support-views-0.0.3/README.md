
# Django Support Views

Provides views for supporting your application.

Currently it just provides a view that you can post messages to and it will log them
We use this view with "slacker-log-handler" to post support messages in slack

The SupportLogView can take an image in data-url format and put that in slack too.


## Installation

install with pip `pip install django-support-views`

add it to your urls

    urlpatterns = patterns('',
        ...
        url('^support/', include("support_views.urls")),
        ...
    )

On your templates you can send support signals via jquery:

    $.ajax({
      url: "{% url 'support-log' %}",
      method: "post",
      data: {
        image: image
      }
    });

If you use something like html2canvas, you can get a screenshot too:

    html2canvas(document.body, {
      onrendered: function(canvas) {
        console.log("rendered");

        var image = null;
        try {
          image = canvas.toDataURL('image/jpeg', 0.1);
        } catch(ex) {
          image = "";
        }

        document.body.appendChild(canvas);
        $.ajax({
          url: "{% url 'support-log' %}",
          method: "post",
          data: {
            image: image
          }
        });
      }
    });

## settings

You can set an extra context function in the settings:

SUPPORT_EXTRA_CONTEXT


## testing

this app uses tox for testing: ```tox```
