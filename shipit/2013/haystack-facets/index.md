Haystack Facets
================================================
UX Exploration & Improvements
------------------------------------------------

David Ray

July 19, 2013

Overview
------------------------------------------------

* Search in RapidSMS.org
* Borken/Missing Things :-(
* Fixed/New Things :-D
* What's Next?

----

Search in RapidSMS.org
-----------------------------------------------

* Solr backend
* Global Search
* Model Listings
* Facets!

----

Borken/Missing Things
------------------------------------------------

* Deactivating Facet(s)
* Facets and Pagination
* Facets and Search

----

Fixed/New Things -- Deactivating Facets
------------------------------------------------

**Problem:** Must mutate the querystring to remove the selected facet


    !python
    @register.simple_tag
    def remove_facet(request, facet_value):
        """"Returns a string that extracts the supplied facet_value's facect from
            the current querystring
        """
        params = {}
        for param in request.GET.lists():
            # reconstruct the non-selected_facets params
            if param[0] != 'selected_facets':
                for v in param[1]:
                    params[param[0]] = v
            else:
                for v in param[1]:
                    # exclude the selected_facet param that matches the supplied
                    # facet_value
                    if facet_value != v.split(':')[1]:
                        params[param[0]] = v
        qs = '?%s' % urlencode(params)
        return qs

----

Fixed/New Things -- Deactivating Facets
------------------------------------------------

    !html
    <h3>Refine Results</h3>
    <div id="reset-filters">
        <br>
        {% if filters %}
        <strong>Active Filters: </strong><br>
        {% for facet, value in filters %}
            <a class="facet_removal" href="{% remove_facet request value %}"><i class="icon-remove-sign"></i></a> {{ facet }}: {{ value }}<br />
        {% endfor %}
        <br>
        <a href="{{ request.path }}{% if query %}?q={{ query }}{% endif %}">Reset Filters</a>
        {% endif %}
    </div>

----


Fixed/New Things -- Facets and Pagination
------------------------------------------------

**Problem:** Default pagination documentation uses ```{{ query }}```

    !python
    @register.simple_tag
    def faceted_next_prev_querystring(request, page_number):
        """"Returns a string that provides the querystring required to paginate in
            search results while retaining the selected facets

            Example:
                {% load facet_tags %}
                {% faceted_next_prev_querystring request page_number %}

            Renders:
               ?q=text&page=N&selected_facets=facet:value
        """
        q_dict = request.GET.copy()
        q_dict['page'] = page_number
        qs = '?%s' % q_dict.urlencode()
        return qs

----

Fixed/New Things -- Facets and Pagination
------------------------------------------------

    !html
    <a href="{% faceted_next_prev_querystring request page.previous_page_number %}>

----

Fixed/New Things -- Facets and Pagination
------------------------------------------------

**Gotcha!** Have to override ```build_page``` and ```create_response```

    !python
    def build_page(self)
        ...
        try:
            page = paginator.page(page_no)
        except InvalidPage:
            # Redirect to page 1 of the
            path = self.request.path
            qs = self.request.GET.copy()
            qs['page'] = 1
            url = '%s?%s' % (path, qs.urlencode())
            return redirect(url)

        return (paginator, page)

----

Fixed/New Things -- Facets and Pagination
------------------------------------------------

**Gotcha!** Have to override ```build_page``` and ```create_response```

    !python
    def create_response(self)
        try:
            (paginator, page) = self.build_page()
        except ValueError:
            return self.build_page()
        ...
----

Fixed/New Things -- Facets and Search
------------------------------------------------

Undocumented, but easy to resolve!

Must use ```FacetedSearchForm```

    !html
    {% for facet in form.selected_facets %}
        <input type="hidden" name="selected_facets" value="{{ facet }}" />
    {% endfor %}


----

What's Next?
------------------------------------------------

* Submit Documentation patch to Haystack?
* Blog Post?
* Abstract bits into a package?
* All of the above?


----

Code
------------------------------------------------

https://github.com/rapidsms/rapidsms.org/
