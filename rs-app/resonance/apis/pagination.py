from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination


class LecturePageNumberPagination(PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        
        pagination = OrderedDict([
             ('current_page', self.page.number),
             ('total_pages', self.page.paginator.count),
        ])
        d['subject_lectures']['lectures'] = data
        return d

      def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))