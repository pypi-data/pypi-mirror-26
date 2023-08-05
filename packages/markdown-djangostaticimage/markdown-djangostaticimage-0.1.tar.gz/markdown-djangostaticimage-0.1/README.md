## Markdown extension for modifying local links to Django static links
Author: Melvin Koh

#### Installing DjangoStaticImage Markdown Extension
```
    pip install markdown-djangostaticimage
```

#### Basic Usage
``` python
from markdown import Markdown
from django_static_image import DjangoStaticImageExtension

text = """![profile_pic](images/profile_pic.png)"""

md = markdown.Markdown(extensions=[DjangoStaticImageExtension()])
html = md.convert(text)

print(html)

# Output
'<p><img alt="profile_pic" src="{% static 'images/profile_pic.png' %}" /></p>'

```
> Note that Markdown by default converts each line as a paragraph <p>


### Examples:
#### Input Markdown
```
    ![profile_picture](images/my_profile_picture.png)
```

#### Output without extension:
``` html
    <img alt="profile_picture" src="images/my_profile_picture.png" />
```

#### Output with this extension:
``` html
    <img alt="profile_picture" src={% static "images/my_profile_picture.png" %} />
```

#### Options:
1. Add Prefix before link:
``` html
    <img alt="profile_picture" src={% static "<prefix>/images/my_profile_picture.png" %} />
```
