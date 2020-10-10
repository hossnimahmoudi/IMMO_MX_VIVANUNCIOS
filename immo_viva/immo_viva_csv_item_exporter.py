from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
import csv

from scrapy.exporters import CsvItemExporter


class QuoteAllDialect(csv.excel):
    quoting = csv.QUOTE_ALL

class immo_vivaCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        fields_to_export = settings.get('FEED_EXPORT_FIELDS', [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export
        kwargs.update({'dialect': QuoteAllDialect})

        super(immo_vivaCsvItemExporter, self).__init__(*args, **kwargs)




