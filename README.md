# Django-Contact
A simple contact form.

# About
Simple contact form app.

# Install
* Add to INSTALLED_APPS 'contacts',
* Add to urls.py url(r'^contacts/', include('contacts.urls')),
* manage.py syncdb
* Add this line to you head block

```html
<link rel='stylesheet' href='/static/css/contacts.css' type='text/css'>
```


# Fow to use
Just use...

# Futures
Create settings for contacts data
Add parameters to offices
ParameterType:
* Name
* Slug
Parameter:
* ParameterType
* Value

Regions
* Countries
* State
* City
* Regions
<!--city = models.ForeignKey(Region, verbose_name=_('City'), limit_choices_to={'region_type': 'city'})-->


# ChangeLog
## 2012.11.04
* Rename model, make translations

## 2012.10.25
* Rename to contacts

## 2012.10.23
* Start develop