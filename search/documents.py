from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Index
from news.models import News

news = Index('news')
# See Elasticsearch Indices API reference for available settings
news.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
@news.document
class NewsDocument(Document):

    class Django:
        model = News
        fields = [
            'name',
            'short_txt',
            'picurl',
            'id',
            'writer',
            'date',
        ]